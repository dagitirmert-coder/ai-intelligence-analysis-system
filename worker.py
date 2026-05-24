"""
GEOINT Worker — APScheduler-based background task runner.
Channels:
  A: Data collection (RSS, earthquakes, Telegram)
  B: Deep analysis (LLM processing, threat recalculation)
  C: Intelligence (agents, daily briefs)
  sys: Maintenance (backup, cleanup)
"""
import logging
import time
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

import config
from db.engine import SessionLocal
from db.models import WorkerLog

# ── Logging ───────────────────────────────────────────────

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker")

file_handler = RotatingFileHandler(
    "data/worker.log", maxBytes=10 * 1024 * 1024, backupCount=5,
    encoding="utf-8",
)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
))
logger.addHandler(file_handler)


# ── Helper ────────────────────────────────────────────────

def _run_task(task_name: str, task_func, *args):
    """Execute a task with logging and error handling."""
    start = time.time()
    db = SessionLocal()

    log = WorkerLog(
        task_name=task_name,
        status="running",
        started_at=datetime.now(timezone.utc),
    )
    db.add(log)
    db.commit()

    try:
        result = task_func(db, *args)
        duration = time.time() - start

        log.status = "completed"
        log.duration_seconds = round(duration, 2)
        log.items_processed = result.get("processed", result.get("collected", 0))
        log.message = str(result)[:500]
        log.finished_at = datetime.now(timezone.utc)

        logger.info(f"[{task_name}] completed in {duration:.1f}s: {result}")

    except Exception as e:
        duration = time.time() - start
        log.status = "error"
        log.duration_seconds = round(duration, 2)
        log.message = str(e)[:500]
        log.finished_at = datetime.now(timezone.utc)
        logger.error(f"[{task_name}] failed after {duration:.1f}s: {e}")

    finally:
        db.commit()
        db.close()


# ── Channel A: Data Collection ────────────────────────────

def collect_news():
    from core.collectors.rss_collector import collect_rss_feeds
    _run_task("collect_news", collect_rss_feeds)


def collect_earthquakes():
    from core.collectors.earthquake_collector import collect_earthquakes as _collect
    _run_task("collect_earthquakes", _collect)


# ── Channel B: Deep Analysis ─────────────────────────────

def process_news():
    from core.processing.pipeline import process_news_batch
    _run_task("process_news", process_news_batch)


def recalculate_threats():
    from core.agents.risk_agent import _recalculate_all_risks
    _run_task("threat_recalculation", lambda db: {"processed": _recalculate_all_risks(db)})


# ── Channel C: Intelligence ──────────────────────────────

def run_agents():
    """Run ALL agents including predictive + meta_agent."""
    from core.agents.dispatcher import run_all_agents
    _run_task("agents", lambda db: {"processed": len(run_all_agents(db))})


def generate_daily_brief():
    from core.intelligence.report_generator import generate_daily_brief as _gen
    _run_task("daily_brief", lambda db: {"processed": 1, "id": _gen(db).id})


def run_behavioral_analysis():
    """Compute baselines and detect behavioral anomalies."""
    from core.intelligence.behavioral_analysis import run_behavioral_analysis as _run
    _run_task("behavioral_analysis", _run)


def run_predictive_cycle():
    """Run the full predictive intelligence cycle."""
    from core.services.predictive_engine import run_predictive_cycle as _run
    _run_task("predictive_cycle", _run)


# ── Channel sys: Maintenance ─────────────────────────────

# ── GEOINT: Satellite & OSM Tasks ────────────────────────

def scan_satellite_imagery():
    """Scan high-value entities for new Sentinel-2 imagery."""
    from core.services.satellite_downloader import scan_strategic_entities
    _run_task("satellite_scan", lambda db: scan_strategic_entities(db, min_strategic_score=7.0, days_back=14))


def generate_strategic_update():
    """Generate weekly Turkey-wide strategic intelligence update."""
    from core.intelligence.geoint_reporter import generate_strategic_update as _gen
    _run_task("strategic_update", lambda db: _gen(db, days=7))


def run_change_detection_sweep():
    """Run change detection on all registered image pairs."""
    from core.services.change_detection import find_image_pairs, run_change_detection
    from db.models import SatelliteImage

    def _sweep(db):
        images = db.query(SatelliteImage).order_by(SatelliteImage.acquired_at.desc()).limit(50).all()
        detected = 0
        for i, after_img in enumerate(images):
            for before_img in images[i + 1:]:
                if not after_img.acquired_at or not before_img.acquired_at:
                    continue
                days_apart = (after_img.acquired_at - before_img.acquired_at).days
                if 14 <= days_apart <= 90:
                    result = run_change_detection(before_img.id, after_img.id, db)
                    if result:
                        detected += 1
                    break
        return {"processed": len(images), "detected": detected}

    _run_task("change_detection_sweep", _sweep)


def cleanup_old_data():
    """Clean up old worker logs and read alerts."""
    from datetime import timedelta
    from db.models import Alert

    def _cleanup(db):
        cutoff = datetime.now(timezone.utc) - timedelta(days=30)
        deleted_logs = db.query(WorkerLog).filter(WorkerLog.started_at < cutoff).delete()
        deleted_alerts = db.query(Alert).filter(
            Alert.is_read == True, Alert.created_at < cutoff
        ).delete()
        return {"processed": deleted_logs + deleted_alerts}

    _run_task("cleanup", _cleanup)


# ── Full Pipeline ─────────────────────────────────────────

def update_intelligence_profiles():
    """
    Intelligence Pipeline Step 2: Deep person profile re-analysis.
    Runs after process_news — finds persons flagged with needs_profile_update=True
    and synthesizes all their news data into vulnerability/strength/prediction profiles.
    """
    from core.processing.pipeline import update_person_profiles
    _run_task("update_profiles", update_person_profiles)


def run_full_pipeline():
    """
    Intelligence Pipeline (sequential):
      collect → process → profile update → agents → satellite → intel

    Military Pipeline runs separately via tactical_parser on report ingestion.
    """
    logger.info("=== FULL PIPELINE START ===")
    collect_news()
    collect_earthquakes()
    process_news()
    update_intelligence_profiles()   # ← NEW: deep person profiling after extraction
    recalculate_threats()
    run_agents()
    scan_satellite_imagery()
    run_change_detection_sweep()
    logger.info("=== FULL PIPELINE END ===")


# ── Scheduler ─────────────────────────────────────────────

def main():
    # Ensure DB is initialized
    from db.engine import init_db
    init_db()

    scheduler = BlockingScheduler()

    # Channel A — Collection
    scheduler.add_job(collect_news, IntervalTrigger(minutes=config.COLLECT_INTERVAL),
                      id="collect_news", name="RSS Collection")
    scheduler.add_job(collect_earthquakes, IntervalTrigger(minutes=30),
                      id="collect_earthquakes", name="Earthquake Collection")

    # Channel B — Processing
    scheduler.add_job(process_news, IntervalTrigger(minutes=config.PROCESS_INTERVAL),
                      id="process_news", name="LLM Processing")
    scheduler.add_job(recalculate_threats, IntervalTrigger(minutes=config.THREAT_RECALC_INTERVAL),
                      id="threat_recalculation", name="Threat Recalculation")

    # Channel C — Intelligence
    scheduler.add_job(run_agents, IntervalTrigger(minutes=config.AGENT_INTERVAL),
                      id="run_agents", name="Agent Cycle")
    scheduler.add_job(generate_daily_brief, CronTrigger(hour=6, minute=0),
                      id="daily_brief", name="Daily Brief")

    # Channel C+ — Predictive Intelligence
    scheduler.add_job(run_behavioral_analysis, CronTrigger(hour=2, minute=0),
                      id="behavioral_analysis", name="Behavioral Analysis (daily)")
    scheduler.add_job(run_predictive_cycle, IntervalTrigger(minutes=60),
                      id="predictive_cycle", name="Predictive Cycle")

    # Channel sys — Maintenance
    scheduler.add_job(cleanup_old_data, CronTrigger(hour=3, minute=0),
                      id="cleanup", name="Cleanup")

    # GEOINT — Satellite & Change Detection
    scheduler.add_job(scan_satellite_imagery, IntervalTrigger(hours=6),
                      id="satellite_scan", name="Satellite Imagery Scan (6h)")
    scheduler.add_job(run_change_detection_sweep, IntervalTrigger(hours=12),
                      id="change_detection", name="Change Detection Sweep (12h)")
    scheduler.add_job(generate_strategic_update, CronTrigger(day_of_week="mon", hour=7, minute=0),
                      id="strategic_update", name="Weekly Strategic Update (Mon 07:00)")

    logger.info("GEOINT Worker started")
    logger.info(f"  Collect: every {config.COLLECT_INTERVAL}min")
    logger.info(f"  Process: every {config.PROCESS_INTERVAL}min")
    logger.info(f"  Agents:  every {config.AGENT_INTERVAL}min")
    logger.info(f"  Predictive: every 60min")
    logger.info(f"  Behavioral: daily 02:00 UTC")
    logger.info(f"  Daily brief: 06:00 UTC")
    logger.info(f"  Satellite scan: every 6h")
    logger.info(f"  Change detection: every 12h")
    logger.info(f"  Strategic update: Mon 07:00 UTC")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Worker stopped")


if __name__ == "__main__":
    main()
