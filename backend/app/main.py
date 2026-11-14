"""PROJECT-EVOLVE API — main application entrypoint."""
from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.errors import RateLimitExceeded
    from slowapi.middleware import SlowAPIMiddleware
    from slowapi.util import get_remote_address
    HAVE_SLOWAPI = True
except ImportError:
    HAVE_SLOWAPI = False

from app.config import get_settings
from app.domains.admin.router import router as admin_router
from app.domains.assessments.router import router as assessments_router
from app.domains.auth.router import router as auth_router
from app.domains.companion.router import router as companion_router
from app.domains.disputes.router import router as disputes_router
from app.domains.genome.router import router as genome_router
from app.domains.goals.router import router as goals_router
from app.domains.missions.router import router as missions_router
from app.domains.profiles.router import router as profiles_router
from app.domains.reviews.router import router as reviews_router
from app.domains.roadmap.router import router as roadmap_router
from app.domains.twin.router import router as twin_router
from app.domains.users.router import router as users_router

settings = get_settings()

# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------
if HAVE_SLOWAPI:
    limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])
else:
    limiter = None


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
app = FastAPI(
    title="PROJECT-EVOLVE API",
    version="0.1.0",
    description=(
        "Evidence-based learner intelligence platform. "
        "Models what a learner demonstrably knows, finds gaps, "
        "and recommends the next action — always explainably."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# State (rate limiter)
# ---------------------------------------------------------------------------
if HAVE_SLOWAPI and limiter is not None:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]
    app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def secure_headers_middleware(request: Request, call_next):  # type: ignore[no-untyped-def]
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


# ---------------------------------------------------------------------------
# System routes
# ---------------------------------------------------------------------------
@app.get("/health", tags=["System"])
async def health_check() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok", "version": "0.1.0", "environment": settings.environment}


# ---------------------------------------------------------------------------
# Domain Routers (/api/v1/*)
# ---------------------------------------------------------------------------
API_V1_PREFIX = "/api/v1"

app.include_router(auth_router, prefix=API_V1_PREFIX)
app.include_router(users_router, prefix=API_V1_PREFIX)
app.include_router(profiles_router, prefix=API_V1_PREFIX)
app.include_router(goals_router, prefix=API_V1_PREFIX)
app.include_router(genome_router, prefix=API_V1_PREFIX)
app.include_router(assessments_router, prefix=API_V1_PREFIX)
app.include_router(twin_router, prefix=API_V1_PREFIX)
app.include_router(roadmap_router, prefix=API_V1_PREFIX)
app.include_router(missions_router, prefix=API_V1_PREFIX)
app.include_router(reviews_router, prefix=API_V1_PREFIX)
app.include_router(companion_router, prefix=API_V1_PREFIX)
app.include_router(disputes_router, prefix=API_V1_PREFIX)
app.include_router(admin_router, prefix=API_V1_PREFIX)
