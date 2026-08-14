import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.db import DatabaseUnavailableError, close_driver, verify_connectivity
from app.routers import careers, gap, people, roles, skills

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("skillroute")


@asynccontextmanager
async def lifespan(app: FastAPI):
    ok, detail = verify_connectivity()
    if ok:
        logger.info("Connected to CognoDB.")
    else:
        # Don't crash the process -- the API should come up and report a
        # clear "database unreachable" state rather than fail to boot.
        logger.warning("Starting without a working CognoDB connection: %s", detail)
    yield
    close_driver()


app = FastAPI(title="SkillRoute API", version="1.0.0", lifespan=lifespan)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.exception_handler(DatabaseUnavailableError)
async def database_unavailable_handler(request: Request, exc: DatabaseUnavailableError):
    return JSONResponse(
        status_code=503,
        content={
            "detail": "SkillRoute can't reach the graph database right now. "
            "Please try again in a moment.",
        },
    )


@app.get("/api/health")
def health():
    ok, detail = verify_connectivity()
    return {"status": "ok" if ok else "degraded", "database": "up" if ok else "down", "detail": detail}


app.include_router(roles.router)
app.include_router(skills.router)
app.include_router(people.router)
app.include_router(gap.router)
app.include_router(careers.router)
