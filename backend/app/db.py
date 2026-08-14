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
import time

from neo4j import GraphDatabase, Driver
from neo4j.exceptions import ServiceUnavailable, AuthError, Neo4jError

from app.config import get_settings

logger = logging.getLogger("skillroute.db")

_driver: Driver | None = None


def get_driver() -> Driver:
    global _driver
    if _driver is None:
        settings = get_settings()
        _driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_username, settings.neo4j_password),
            max_connection_pool_size=20,
            connection_acquisition_timeout=10,
        )
    return _driver


def close_driver() -> None:
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None


def verify_connectivity() -> tuple[bool, str | None]:
    """Used at startup and by /health -- never raises, always reports."""
    settings = get_settings()

    # Temporary network diagnostics for Render/CognoDB connectivity.
    try:
        uri = settings.neo4j_uri
        logger.warning("DB DEBUG: Neo4j URI = %s", uri)

        # Extract hostname from the URI without logging credentials.
        from urllib.parse import urlparse

        parsed = urlparse(uri)
        host = parsed.hostname
        port = parsed.port or 7687

        logger.warning("DB DEBUG: host=%s port=%s", host, port)

        # DNS resolution
        addresses = socket.getaddrinfo(
            host,
            port,
            type=socket.SOCK_STREAM,
        )

        logger.warning(
            "DB DEBUG: DNS resolved to: %s",
            [(a[4][0], a[4][1]) for a in addresses],
        )

        # Raw TCP connection
        start = time.time()

        sock = socket.create_connection(
            (host, port),
            timeout=10,
        )

        logger.warning(
            "DB DEBUG: TCP CONNECTED in %.2fs peer=%s",
            time.time() - start,
            sock.getpeername(),
        )

        # See whether the server sends anything back.
        sock.settimeout(5)

        try:
            data = sock.recv(1024)
            logger.warning(
                "DB DEBUG: server sent %d bytes: %r",
                len(data),
                data,
            )
        except socket.timeout:
            logger.warning(
                "DB DEBUG: server sent NOTHING within 5 seconds"
            )
        except Exception as exc:
            logger.warning(
                "DB DEBUG: raw recv failed: %s: %s",
                type(exc).__name__,
                exc,
            )
        finally:
            sock.close()

    except Exception as exc:
        logger.warning(
            "DB DEBUG: raw network test FAILED: %s: %s",
            type(exc).__name__,
            exc,
        )

    # Now test the actual Neo4j driver.
    try:
        logger.warning("DB DEBUG: starting Neo4j verify_connectivity()")

        get_driver().verify_connectivity()

        logger.warning("DB DEBUG: Neo4j verify_connectivity() SUCCESS")

        return True, None

    except AuthError:
        return False, (
            "Authentication to the database failed. "
            "Check NEO4J_USERNAME/NEO4J_PASSWORD."
        )

    except ServiceUnavailable as exc:
        logger.error(
            "DB DEBUG: Neo4j ServiceUnavailable: %s",
            exc,
        )
        return False, f"Database is unreachable: {exc}"

    except Exception as exc:  # noqa: BLE001
        logger.error(
            "DB DEBUG: unexpected Neo4j error: %s: %s",
            type(exc).__name__,
            exc,
        )
        return False, f"Unexpected database error: {exc}"

class DatabaseUnavailableError(Exception):
    """Raised by query helpers when CognoDB can't be reached, so routers can
    turn it into a clean 503 instead of a raw stack trace reaching the UI."""


def run_query(cypher: str, parameters: dict | None = None, database: str | None = None) -> list[dict]:
    """
    Run a single parameterised Cypher statement and return a list of plain
    dicts. All query modules go through this helper -- no router ever builds
    Cypher via string concatenation.
    """
    settings = get_settings()
    parameters = parameters or {}
    if settings.debug_log_queries:
        logger.info("CYPHER %s | params=%s", " ".join(cypher.split()), parameters)
    try:
        records, _summary, _keys = get_driver().execute_query(
            cypher,
            parameters,
            database_=database or settings.neo4j_database,
        )
        return [record.data() for record in records]
    except (ServiceUnavailable, AuthError) as exc:
        logger.error("CognoDB unreachable: %s", exc)
        raise DatabaseUnavailableError(str(exc)) from exc
    except Neo4jError as exc:
        # Query-level errors (bad Cypher, constraint violation, etc.) are
        # real bugs, not connectivity issues -- let them surface as 500s.
        logger.error("Cypher error: %s", exc)
        raise
