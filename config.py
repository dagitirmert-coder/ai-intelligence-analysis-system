"""
GEOINT Platform Configuration
Military-grade geospatial intelligence system settings.
All values can be overridden via environment variables.
"""
import os

# ── Database ──────────────────────────────────────────────
DATABASE_URL = os.environ.get(
    "GEOINT_DATABASE_URL",
    "postgresql+psycopg2://geoint:geoint@localhost:5432/geointdb"
)

# ── API Security ──────────────────────────────────────────
API_KEY = os.environ.get("GEOINT_API_KEY", "")
SECRET_KEY = os.environ.get("GEOINT_SECRET_KEY", "geoint-dev-key-change-in-prod")

# ── Ollama LLM Models ────────────────────────────────────
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_LARGE_MODEL = os.environ.get("OLLAMA_LARGE_MODEL", "gemma3:12b")
OLLAMA_SMALL_MODEL = os.environ.get("OLLAMA_SMALL_MODEL", "gemma3:4b")
OLLAMA_TIMEOUT = int(os.environ.get("OLLAMA_TIMEOUT", "300"))  # 5 min for large model chunks

# ── CesiumJS ──────────────────────────────────────────────
CESIUM_ION_TOKEN = os.environ.get("CESIUM_ION_TOKEN", "")

# ── Risk & Threat Thresholds ─────────────────────────────
# Risk = Probability × Impact
# Threat levels derived from risk_score:
THREAT_LEVEL_THRESHOLDS = {
    "low": 0.0,       # 0.0 - 2.0
    "medium": 2.0,     # 2.0 - 4.0
    "high": 4.0,       # 4.0 - 7.0
    "critical": 7.0,   # 7.0 - 10.0
}

# Impact weight multipliers by entity type
ENTITY_IMPACT_WEIGHTS = {
    "military_base": 9.0,
    "command_center": 9.5,
    "nuclear_plant": 10.0,
    "dam": 9.0,
    "power_plant": 7.5,
    "power_grid_node": 7.0,
    "pipeline": 6.5,
    "refinery": 7.5,
    "fuel_depot": 7.0,
    "port": 6.5,
    "airport": 7.0,
    "bridge": 5.5,
    "tunnel": 5.0,
    "railway_hub": 5.5,
    "road_junction": 4.0,
    "comms_tower": 6.0,
    "radar_station": 8.0,
    "border_crossing": 5.0,
    "hospital": 4.5,
    "water_treatment": 5.5,
    "government_building": 6.0,
    "embassy": 5.5,
    "industrial_complex": 5.0,
    "ammunition_depot": 8.5,
    "air_defense": 9.0,
    "naval_base": 8.5,
    "cyber_center": 7.5,
    "intelligence_hq": 9.0,
}

# Cascade simulation
SCENARIO_MAX_CASCADE_DEPTH = 6
SCENARIO_ATTENUATION_FACTOR = 0.80  # 20% signal loss per hop
SCENARIO_MIN_IMPACT_THRESHOLD = 0.05

# ── Alert Thresholds ─────────────────────────────────────
ALERT_THRESHOLDS = {
    "risk_score_critical": 7.0,
    "risk_score_high": 4.0,
    "earthquake_magnitude": 5.5,
    "disaster_severity_critical": "red",
    "breaking_keywords": [
        "saldırı", "patlama", "savaş", "nükleer", "invasion",
        "attack", "explosion", "nuclear", "missile", "bombardment",
    ],
}

# ── Worker Intervals (minutes) ───────────────────────────
# Channel A - News Pipeline
COLLECT_INTERVAL = int(os.environ.get("COLLECT_INTERVAL", "10"))
PROCESS_INTERVAL = int(os.environ.get("PROCESS_INTERVAL", "5"))
DEDUP_INTERVAL = int(os.environ.get("DEDUP_INTERVAL", "60"))
COLLECT_MAX_WORKERS = int(os.environ.get("COLLECT_MAX_WORKERS", "6"))

# Channel B - Deep Analysis
THREAT_RECALC_INTERVAL = int(os.environ.get("THREAT_RECALC_INTERVAL", "30"))
RELATION_EXTRACT_INTERVAL = int(os.environ.get("RELATION_EXTRACT_INTERVAL", "60"))

# Channel C - Intelligence
INTELLIGENCE_INTERVAL = int(os.environ.get("INTELLIGENCE_INTERVAL", "360"))
AGENT_INTERVAL = int(os.environ.get("AGENT_INTERVAL", "15"))

# ── Data Collection ──────────────────────────────────────
NEWSAPI_KEYS = [k.strip() for k in os.environ.get("NEWSAPI_KEYS", "").split(",") if k.strip()]
GNEWS_KEY = os.environ.get("GNEWS_KEY", "")
ACLED_API_KEY = os.environ.get("ACLED_API_KEY", "")

# ── Deduplication ────────────────────────────────────────
DEDUP_HIGH_THRESHOLD = 0.75
DEDUP_LOW_THRESHOLD = 0.45
DEDUP_WINDOW_HOURS = 72

# ── Processing ───────────────────────────────────────────
PROCESS_MAX_ATTEMPTS = 3
PROCESS_BATCH_SIZE = 20

# ── Terrain Grid ─────────────────────────────────────────
GRID_RESOLUTION_DEG = 0.1  # ~11 km per cell at equator
TURKEY_BBOX = {
    "lat_min": 35.8, "lat_max": 42.2,
    "lon_min": 25.5, "lon_max": 44.8,
}

# ── RSS Feeds ────────────────────────────────────────────
TURKEY_RSS_FEEDS = [
    "https://www.aa.com.tr/tr/rss/default?cat=guncel",
    "https://www.hurriyet.com.tr/rss/gundem",
    "https://www.ntv.com.tr/gundem.rss",
    "https://www.trthaber.com/sondakika.rss",
    "https://www.cnnturk.com/feed/rss/all/news",
]

GLOBAL_RSS_FEEDS = [
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://feeds.reuters.com/reuters/worldNews",
    "https://www.aljazeera.com/xml/rss/all.xml",
]

TELEGRAM_CHANNELS = [
    "intelopenai", "livaboronka", "ryaboronka72",
    "osaboronka", "legitimniy", "ResijorDonbassa",
    "boris_rozhin", "vysokygovorit", "grey_zone",
]

# ── Keywords ─────────────────────────────────────────────
# ── GEOINT — Satellite & Tile Storage ──────────────────
CDSE_USERNAME = os.environ.get("CDSE_USERNAME", "")
CDSE_PASSWORD = os.environ.get("CDSE_PASSWORD", "")
GEOINT_TILE_CACHE = os.environ.get("GEOINT_TILE_CACHE", "data/tiles")
GEOINT_SATELLITE_DIR = os.environ.get("GEOINT_SATELLITE_DIR", "data/satellite")

# ── Keywords ─────────────────────────────────────────────
COLLECTION_KEYWORDS = [
    "Turkey military", "NATO", "conflict zone", "missile",
    "drone strike", "cyber attack", "energy crisis",
    "pipeline", "earthquake", "nuclear", "Türkiye",
    "Black Sea", "Mediterranean", "Middle East",
    "Syria", "Iraq", "defense", "intelligence",
]


def get_threat_level(risk_score: float) -> str:
    """Derive threat level from computed risk score."""
    if risk_score >= THREAT_LEVEL_THRESHOLDS["critical"]:
        return "critical"
    elif risk_score >= THREAT_LEVEL_THRESHOLDS["high"]:
        return "high"
    elif risk_score >= THREAT_LEVEL_THRESHOLDS["medium"]:
        return "medium"
    return "low"
