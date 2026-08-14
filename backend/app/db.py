"""
Neo4j / CognoDB driver management.

CognoDB speaks openCypher over Bolt, so the official `neo4j` Python driver is
used unmodified -- no custom SDK. We keep a single process-wide driver
instance (the driver already manages an internal connection pool; opening a
fresh driver per-request would exhaust CognoDB's free-tier 200 connection
cap under any real load).
"""

import logging
import socket
import ssl
import time
from urllib.parse import urlparse

from neo4j import GraphDatabase, Driver
from neo4j.exceptions import ServiceUnavailable, AuthError, Neo4jError

from app.config import get_settings

logger = logging.getLogger("skillroute.db")

_driver: Driver | None = None


def get_driver() -> Driver:
    global _driver

    if _driver is None:
        settings = get_settings()

        logger.info(
            "Creating CognoDB driver for %s",
            settings.neo4j_uri,
        )

        _driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(
                settings.neo4j_username,
                settings.neo4j_password,
            ),
            max_connection_pool_size=20,
            connection_acquisition_timeout=10,
            connection_timeout=10,
        )

    return _driver


def close_driver() -> None:
    global _driver

    if _driver is not None:
        _driver.close()
        _driver = None


def _debug_network_connection(uri: str) -> None:
    """
    Temporary diagnostic for Render -> CognoDB connectivity.

    Tests:
      1. DNS resolution
      2. TCP connection
      3. TLS handshake

    This does NOT authenticate or speak Bolt. It is only intended to determine
    whether the failure happens at the network/TLS layer before the Neo4j
    driver gets involved.
    """

    try:
        parsed = urlparse(uri)

        host = parsed.hostname
        port = parsed.port or 7687

        if not host:
            logger.warning(
                "DB DEBUG: Could not extract hostname from Neo4j URI"
            )
            return

        logger.warning(
            "DB DEBUG: Neo4j URI = %s",
            uri,
        )

        logger.warning(
            "DB DEBUG: host=%s port=%s",
            host,
            port,
        )

        # ---------------------------------------------------------------
        # DNS
        # ---------------------------------------------------------------
        try:
            addresses = socket.getaddrinfo(
                host,
                port,
                type=socket.SOCK_STREAM,
            )

            resolved = [
                (address[4][0], address[4][1])
                for address in addresses
            ]

            logger.warning(
                "DB DEBUG: DNS resolved to: %s",
                resolved,
            )

        except Exception as exc:
            logger.warning(
                "DB DEBUG: DNS FAILED: %s: %s",
                type(exc).__name__,
                exc,
            )
            return

        # ---------------------------------------------------------------
        # TCP
        # ---------------------------------------------------------------
        sock = None

        try:
            start = time.time()

            sock = socket.create_connection(
                (host, port),
                timeout=10,
            )

            elapsed = time.time() - start

            logger.warning(
                "DB DEBUG: TCP CONNECTED in %.2fs peer=%s",
                elapsed,
                sock.getpeername(),
            )

        except Exception as exc:
            logger.warning(
                "DB DEBUG: TCP CONNECTION FAILED: %s: %s",
                type(exc).__name__,
                exc,
            )

            if sock is not None:
                sock.close()

            return

        # ---------------------------------------------------------------
        # TLS
        # ---------------------------------------------------------------
        try:
            logger.warning(
                "DB DEBUG: Starting TLS handshake..."
            )

            context = ssl.create_default_context()

            tls_sock = context.wrap_socket(
                sock,
                server_hostname=host,
            )

            logger.warning(
                "DB DEBUG: TLS CONNECTED version=%s cipher=%s",
                tls_sock.version(),
                tls_sock.cipher(),
            )

            try:
                logger.warning(
                    "DB DEBUG: TLS peer certificate subject=%s",
                    tls_sock.getpeercert().get("subject"),
                )

            except Exception:
                pass

            tls_sock.close()

        except ssl.SSLCertVerificationError as exc:
            logger.warning(
                "DB DEBUG: TLS CERTIFICATE VERIFICATION FAILED: %s",
                exc,
            )

            try:
                sock.close()
            except Exception:
                pass

        except ssl.SSLError as exc:
            logger.warning(
                "DB DEBUG: TLS FAILED: %s: %s",
                type(exc).__name__,
                exc,
            )

            try:
                sock.close()
            except Exception:
                pass

        except Exception as exc:
            logger.warning(
                "DB DEBUG: TLS FAILED: %s: %s",
                type(exc).__name__,
                exc,
            )

            try:
                sock.close()
            except Exception:
                pass

    except Exception as exc:
        logger.warning(
            "DB DEBUG: Network diagnostic failed unexpectedly: %s: %s",
            type(exc).__name__,
            exc,
        )


def verify_connectivity() -> tuple[bool, str | None]:
    """Used at startup and by /health -- never raises, always reports."""

    settings = get_settings()

    # ------------------------------------------------------------------
    # Temporary Render/CognoDB network diagnostics.
    # ------------------------------------------------------------------
    _debug_network_connection(settings.neo4j_uri)

    # ------------------------------------------------------------------
    # Actual Neo4j driver connectivity test.
    # ------------------------------------------------------------------
    try:
        logger.warning(
            "DB DEBUG: Starting Neo4j verify_connectivity()..."
        )

        start = time.time()

        get_driver().verify_connectivity()

        elapsed = time.time() - start

        logger.warning(
            "DB DEBUG: Neo4j verify_connectivity() SUCCESS in %.2fs",
            elapsed,
        )

        return True, None

    except AuthError:
        logger.error(
            "DB DEBUG: Neo4j authentication failed"
        )

        return False, (
            "Authentication to the database failed. "
            "Check NEO4J_USERNAME/NEO4J_PASSWORD."
        )

    except ServiceUnavailable as exc:
        elapsed = time.time() - start

        logger.error(
            "DB DEBUG: Neo4j ServiceUnavailable after %.2fs: %s",
            elapsed,
            exc,
        )

        return False, f"Database is unreachable: {exc}"

    except Exception as exc:
        elapsed = time.time() - start

        logger.error(
            "DB DEBUG: Unexpected Neo4j error after %.2fs: %s: %s",
            elapsed,
            type(exc).__name__,
            exc,
        )

        return False, f"Unexpected database error: {exc}"


class DatabaseUnavailableError(Exception):
    """Raised by query helpers when CognoDB can't be reached, so routers can
    turn it into a clean 503 instead of a raw stack trace reaching the UI."""


def run_query(
    cypher: str,
    parameters: dict | None = None,
    database: str | None = None,
) -> list[dict]:
    """
    Run a single parameterised Cypher statement and return a list of plain
    dicts. All query modules go through this helper -- no router ever builds
    Cypher via string concatenation.
    """

    settings = get_settings()
    parameters = parameters or {}

    if settings.debug_log_queries:
        logger.info(
            "CYPHER %s | params=%s",
            " ".join(cypher.split()),
            parameters,
        )

    try:
        records, _summary, _keys = get_driver().execute_query(
            cypher,
            parameters,
            database_=database or settings.neo4j_database,
        )

        return [record.data() for record in records]

    except (ServiceUnavailable, AuthError) as exc:
        logger.error(
            "CognoDB unreachable: %s",
            exc,
        )

        raise DatabaseUnavailableError(str(exc)) from exc

    except Neo4jError as exc:
        # Query-level errors (bad Cypher, constraint violation, etc.) are
        # real bugs, not connectivity issues -- let them surface as 500s.
        logger.error(
            "Cypher error: %s",
            exc,
        )

        raise