"""
GEOINT Platform — FastAPI Application Entry Point
Military-grade geospatial intelligence system.
"""
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

import config
from db.engine import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and PostGIS extensions on startup."""
    init_db()
    yield


app = FastAPI(
    title="GEOINT Platform",
    description="Military-grade geospatial intelligence & decision support system",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── API Key Middleware ────────────────────────────────────
@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    if config.API_KEY and request.url.path.startswith("/api/"):
        if request.url.path != "/api/health":
            key = request.headers.get("X-API-Key", "")
            if key != config.API_KEY:
                return Response(
                    content='{"detail":"Unauthorized"}',
                    status_code=401,
                    media_type="application/json",
                )
    response = await call_next(request)
    return response


# ── Static Files & Templates ─────────────────────────────
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "v": int(time.time()),
    })


@app.get("/map")
async def map3d(request: Request):
    """Standalone sophisticated 3D map page."""
    return templates.TemplateResponse("map3d.html", {
        "request": request,
    })


# ── Router Registration ──────────────────────────────────
from api.health_api import router as health_router
from api.entity_api import router as entity_router
from api.threat_api import router as threat_router
from api.scenario_api import router as scenario_router
from api.search_api import router as search_router
from api.terrain_api import router as terrain_router
from api.map_api import router as map_router
from api.agent_api import router as agent_router
from api.news_api import router as news_router
from api.intel_api import router as intel_router
from api.dashboard_api import router as dashboard_router
from api.person_api import router as person_router
from api.events_api import router as events_router
from api.worker_api import router as worker_router
from api.los_api import router as los_router
from api.satellite_api import router as satellite_router
from api.risk_api import router as risk_router
from api.network_api import router as network_router
from api.simulation_api import router as simulation_router
from api.predictive_api import router as predictive_router
from api.fusion_api import router as fusion_router
# ── GEOINT Upgrade Routers ──────────────────────────────
from api.intelligence_api import router as intelligence_router
from api.osm_api import router as osm_router
from api.tile_api import router as tile_router
from api.geoint_api import router as geoint_router
from api.report_intel_api import router as report_intel_router
from api.surveillance_api import router as surveillance_router
from api.person_research_api import router as person_research_router
from api.satellite_imagery_api import router as sat_imagery_router
# ── HUMINT Management ────────────────────────────────
from api.humint_api import router as humint_router
# ── Operational Intelligence ─────────────────────────
from api.operations_api import router as operations_router
# ── Person Analysis (Dossier + AI Chat) ─────────────
from api.person_analysis_api import router as person_analysis_router
# ── Data Entry (Audio, Person CRUD, Photo) ──────────
from api.data_entry_api import router as data_entry_router
# ── Region Report & Chatbot ─────────────────────────
from api.region_report_api import router as region_report_router
from api.region_chatbot_api import router as region_chatbot_router
# ── Military Mode (COP) ──────────────────────────────────
from api.military_api import router as military_router

app.include_router(health_router, prefix="/api")
app.include_router(entity_router, prefix="/api/entities")
app.include_router(threat_router, prefix="/api/threats")
app.include_router(scenario_router, prefix="/api/scenarios")
app.include_router(search_router, prefix="/api/search")
app.include_router(terrain_router, prefix="/api/terrain")
app.include_router(map_router, prefix="/api/map")
app.include_router(agent_router, prefix="/api/agents")
app.include_router(news_router, prefix="/api/news")
app.include_router(intel_router, prefix="/api/intel")
app.include_router(dashboard_router, prefix="/api/dashboard")
app.include_router(person_router, prefix="/api/persons")
app.include_router(events_router, prefix="/api/events")
app.include_router(worker_router, prefix="/api/worker")
# ── Tier-1 Military Intelligence Features ────────────────
app.include_router(los_router, prefix="/api/los")
app.include_router(satellite_router, prefix="/api/satellite")
app.include_router(risk_router, prefix="/api/risk")
app.include_router(network_router, prefix="/api/network")
app.include_router(simulation_router, prefix="/api/simulation")
app.include_router(predictive_router, prefix="/api/predictive")
# ── Tier-2 Autonomous Decision-Support System ────────────
app.include_router(fusion_router, prefix="/api/fusion")
# ── GEOINT Upgrade: Intelligence, OSM, Tiles, Reports ───
app.include_router(intelligence_router, prefix="/api/intel")
app.include_router(osm_router, prefix="/api/osm")
app.include_router(tile_router, prefix="/api/tiles")
app.include_router(geoint_router, prefix="/api/geoint")
# ── Intelligence Report Parsing & Tracking ────────────────
app.include_router(report_intel_router, prefix="/api/report-intel")
# ── Multi-Source Surveillance Evidence ──────────────────
app.include_router(surveillance_router, prefix="/api/surveillance")
# ── Person Research & Profile Analysis ────────────────────
app.include_router(person_research_router, prefix="/api/person-research")
# ── Satellite Imagery Analysis ────────────────────────────
app.include_router(sat_imagery_router, prefix="/api/sat-imagery")
# ── HUMINT Management ────────────────────────────────
app.include_router(humint_router, prefix="/api/humint")
# ── Operational Intelligence ─────────────────────────
app.include_router(operations_router, prefix="/api/ops")
# ── Person Analysis (Dossier + AI Chat) ─────────────
app.include_router(person_analysis_router, prefix="/api/person-analysis")
# ── Data Entry (Audio Transcription, Person CRUD, Photo Upload) ──
app.include_router(data_entry_router, prefix="/api/data-entry")
# ── Region Report & Chatbot ──────────────────────────
app.include_router(region_report_router, prefix="/api/region-report")
app.include_router(region_chatbot_router, prefix="/api/region-chat")
# ── Military Mode (COP) ──────────────────────────────────
app.include_router(military_router, prefix="/api/military")


@app.get("/person-analysis")
async def person_analysis_page(request: Request):
    """Standalone person analysis & intelligence dossier page."""
    return templates.TemplateResponse("person_analysis.html", {
        "request": request,
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
