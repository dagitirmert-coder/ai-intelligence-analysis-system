"""
Seed Data — Pre-populate the database with strategic entities for Turkey.
Includes military bases, energy infrastructure, transport nodes, and relations.
Run once: python seed_data.py
"""
import logging
from sqlalchemy import func
from db.engine import SessionLocal, init_db
from db.models import Entity, EntityRelation, TerrainCell
from core.services.terrain_generator import generate_turkey_grid
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STRATEGIC ENTITIES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SEED_ENTITIES = [
    # Military
    {"entity_type": "military_base", "name": "İncirlik Üssü", "lat": 37.002, "lng": 35.425,
     "country": "Turkey", "region": "Adana", "operator": "USAF / TurAF",
     "strategic_score": 9.5, "metadata": {"troops_capacity": 5000, "nato": True, "nuclear_capable": True}},
    {"entity_type": "military_base", "name": "Kürecik Radar Üssü", "lat": 38.333, "lng": 37.961,
     "country": "Turkey", "region": "Malatya", "operator": "NATO",
     "strategic_score": 9.0, "metadata": {"type": "AN/TPY-2 radar", "nato": True}},
    {"entity_type": "military_base", "name": "Akıncı Üssü", "lat": 40.078, "lng": 32.566,
     "country": "Turkey", "region": "Ankara", "operator": "TurAF",
     "strategic_score": 8.5, "metadata": {"type": "air_base", "f16_squadron": True}},
    {"entity_type": "command_center", "name": "TSK Karargahı", "lat": 39.931, "lng": 32.854,
     "country": "Turkey", "region": "Ankara", "operator": "TSK",
     "strategic_score": 10.0, "metadata": {"type": "joint_command"}},
    {"entity_type": "naval_base", "name": "Aksaz Deniz Üssü", "lat": 36.907, "lng": 28.224,
     "country": "Turkey", "region": "Muğla", "operator": "TDK",
     "strategic_score": 8.0, "metadata": {"fleet": "Mediterranean"}},
    {"entity_type": "air_defense", "name": "S-400 Bataryası Ankara", "lat": 39.85, "lng": 32.73,
     "country": "Turkey", "region": "Ankara", "operator": "TurAF",
     "strategic_score": 9.0, "metadata": {"system": "S-400", "range_km": 400}},
    {"entity_type": "radar_station", "name": "Diyarbakır Radar", "lat": 37.89, "lng": 40.20,
     "country": "Turkey", "region": "Diyarbakır", "operator": "TurAF",
     "strategic_score": 7.5},
    {"entity_type": "intelligence_hq", "name": "MİT Genel Merkezi", "lat": 39.87, "lng": 32.82,
     "country": "Turkey", "region": "Ankara", "operator": "MİT",
     "strategic_score": 9.5, "metadata": {"type": "signals_intelligence"}},
    {"entity_type": "ammunition_depot", "name": "Afyon Mühimmat Deposu", "lat": 38.73, "lng": 30.55,
     "country": "Turkey", "region": "Afyon", "operator": "TSK",
     "strategic_score": 7.0},

    # Energy
    {"entity_type": "nuclear_plant", "name": "Akkuyu NGS", "lat": 36.144, "lng": 33.526,
     "country": "Turkey", "region": "Mersin", "operator": "Rosatom/ANPP",
     "strategic_score": 9.5, "metadata": {"capacity": "4800 MW", "reactors": 4, "status": "construction"}},
    {"entity_type": "dam", "name": "Atatürk Barajı", "lat": 37.491, "lng": 38.316,
     "country": "Turkey", "region": "Şanlıurfa", "operator": "DSİ",
     "strategic_score": 9.0, "metadata": {"capacity": "2400 MW", "reservoir_km3": 48.7}},
    {"entity_type": "dam", "name": "Keban Barajı", "lat": 38.81, "lng": 38.74,
     "country": "Turkey", "region": "Elazığ", "operator": "DSİ",
     "strategic_score": 7.5, "metadata": {"capacity": "1330 MW"}},
    {"entity_type": "power_plant", "name": "Afşin-Elbistan Termik", "lat": 38.23, "lng": 36.56,
     "country": "Turkey", "region": "Kahramanmaraş", "operator": "EÜAŞ",
     "strategic_score": 7.0, "metadata": {"capacity": "2795 MW", "fuel": "lignite"}},
    {"entity_type": "pipeline", "name": "BTC Boru Hattı Ceyhan", "lat": 36.884, "lng": 35.929,
     "country": "Turkey", "region": "Adana", "operator": "BP/BTC",
     "strategic_score": 8.5, "metadata": {"capacity_bpd": 1000000, "route": "Baku-Tbilisi-Ceyhan"}},
    {"entity_type": "pipeline", "name": "TurkStream Giriş", "lat": 41.71, "lng": 28.00,
     "country": "Turkey", "region": "Kırklareli", "operator": "Gazprom/BOTAŞ",
     "strategic_score": 8.5, "metadata": {"capacity_bcm": 31.5, "type": "gas"}},
    {"entity_type": "refinery", "name": "İzmit Rafinerisi (Tüpraş)", "lat": 40.735, "lng": 29.756,
     "country": "Turkey", "region": "Kocaeli", "operator": "Tüpraş",
     "strategic_score": 8.0, "metadata": {"capacity_bpd": 226000}},
    {"entity_type": "refinery", "name": "Batman Rafinerisi", "lat": 37.88, "lng": 41.14,
     "country": "Turkey", "region": "Batman", "operator": "Tüpraş",
     "strategic_score": 6.5, "metadata": {"capacity_bpd": 22000}},

    # Transport
    {"entity_type": "airport", "name": "İstanbul Havalimanı", "lat": 41.262, "lng": 28.728,
     "country": "Turkey", "region": "İstanbul", "operator": "İGA",
     "strategic_score": 8.0, "metadata": {"iata": "IST", "capacity_pax": 200000000}},
    {"entity_type": "port", "name": "Mersin Limanı", "lat": 36.795, "lng": 34.631,
     "country": "Turkey", "region": "Mersin", "operator": "MIP/PSA",
     "strategic_score": 7.5, "metadata": {"capacity_teu": 2600000}},
    {"entity_type": "port", "name": "İskenderun Limanı", "lat": 36.59, "lng": 36.17,
     "country": "Turkey", "region": "Hatay", "operator": "Limak",
     "strategic_score": 7.0},
    {"entity_type": "bridge", "name": "Osmangazi Köprüsü", "lat": 40.725, "lng": 29.508,
     "country": "Turkey", "region": "Kocaeli", "operator": "OTOYOL A.Ş.",
     "strategic_score": 6.5, "metadata": {"length_m": 2682, "type": "suspension"}},
    {"entity_type": "bridge", "name": "15 Temmuz Şehitler Köprüsü", "lat": 41.045, "lng": 29.034,
     "country": "Turkey", "region": "İstanbul", "operator": "KGM",
     "strategic_score": 7.0, "metadata": {"length_m": 1510}},
    {"entity_type": "railway_hub", "name": "Ankara YHT İstasyonu", "lat": 39.937, "lng": 32.844,
     "country": "Turkey", "region": "Ankara",
     "strategic_score": 5.5},
    {"entity_type": "border_crossing", "name": "Habur Sınır Kapısı", "lat": 37.14, "lng": 42.78,
     "country": "Turkey", "region": "Şırnak",
     "strategic_score": 6.5, "metadata": {"border": "Iraq"}},

    # Comms
    {"entity_type": "comms_tower", "name": "Çamlıca Kulesi", "lat": 41.018, "lng": 29.068,
     "country": "Turkey", "region": "İstanbul", "operator": "KULE İstanbul",
     "strategic_score": 6.0},
    {"entity_type": "cyber_center", "name": "BTK Siber Güvenlik Merkezi", "lat": 39.94, "lng": 32.86,
     "country": "Turkey", "region": "Ankara", "operator": "BTK",
     "strategic_score": 7.5},

    # Infrastructure
    {"entity_type": "hospital", "name": "Ankara Şehir Hastanesi", "lat": 39.97, "lng": 32.67,
     "country": "Turkey", "region": "Ankara", "operator": "SB",
     "strategic_score": 4.0, "metadata": {"beds": 3704}},
    {"entity_type": "water_treatment", "name": "İSKİ İkitelli Arıtma", "lat": 41.065, "lng": 28.789,
     "country": "Turkey", "region": "İstanbul", "operator": "İSKİ",
     "strategic_score": 5.5, "metadata": {"capacity_m3_day": 860000}},
    {"entity_type": "government_building", "name": "Cumhurbaşkanlığı Külliyesi", "lat": 39.931, "lng": 32.799,
     "country": "Turkey", "region": "Ankara",
     "strategic_score": 9.0},
]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STRATEGIC RELATIONS (for cascade simulation)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SEED_RELATIONS = [
    # Energy cascades
    ("Atatürk Barajı", "Afşin-Elbistan Termik", "powers", 0.4),
    ("Atatürk Barajı", "İskenderun Limanı", "supplies", 0.3),
    ("Afşin-Elbistan Termik", "İncirlik Üssü", "powers", 0.7),
    ("Afşin-Elbistan Termik", "Ankara Şehir Hastanesi", "powers", 0.6),
    ("Akkuyu NGS", "Mersin Limanı", "powers", 0.5),
    ("Akkuyu NGS", "BTK Siber Güvenlik Merkezi", "powers", 0.3),
    ("BTC Boru Hattı Ceyhan", "İzmit Rafinerisi (Tüpraş)", "supplies", 0.8),
    ("İzmit Rafinerisi (Tüpraş)", "İstanbul Havalimanı", "supplies", 0.6),
    ("İzmit Rafinerisi (Tüpraş)", "İncirlik Üssü", "supplies", 0.5),
    ("TurkStream Giriş", "Afşin-Elbistan Termik", "supplies", 0.7),
    ("Keban Barajı", "Atatürk Barajı", "supplies", 0.5),

    # Military dependencies
    ("İncirlik Üssü", "Kürecik Radar Üssü", "controls", 0.6),
    ("TSK Karargahı", "İncirlik Üssü", "controls", 0.8),
    ("TSK Karargahı", "Akıncı Üssü", "controls", 0.8),
    ("TSK Karargahı", "S-400 Bataryası Ankara", "controls", 0.9),
    ("TSK Karargahı", "Aksaz Deniz Üssü", "controls", 0.7),
    ("MİT Genel Merkezi", "TSK Karargahı", "connected_to", 0.7),
    ("S-400 Bataryası Ankara", "İstanbul Havalimanı", "protects", 0.5),
    ("Diyarbakır Radar", "S-400 Bataryası Ankara", "connected_to", 0.6),

    # Transport dependencies
    ("Osmangazi Köprüsü", "İzmit Rafinerisi (Tüpraş)", "routes_through", 0.5),
    ("15 Temmuz Şehitler Köprüsü", "İstanbul Havalimanı", "routes_through", 0.4),
    ("Mersin Limanı", "İncirlik Üssü", "supplies", 0.4),
    ("Habur Sınır Kapısı", "Batman Rafinerisi", "routes_through", 0.6),

    # Comms dependencies
    ("Çamlıca Kulesi", "TSK Karargahı", "connected_to", 0.4),
    ("BTK Siber Güvenlik Merkezi", "Çamlıca Kulesi", "controls", 0.5),
    ("BTK Siber Güvenlik Merkezi", "MİT Genel Merkezi", "connected_to", 0.6),
]


def seed_entities(db):
    existing = db.query(func.count(Entity.id)).scalar()
    if existing > 0:
        logger.info(f"Entities already seeded ({existing}). Skipping.")
        return

    entity_map = {}
    for data in SEED_ENTITIES:
        e = Entity(
            entity_type=data["entity_type"],
            name=data["name"],
            name_normalized=data["name"].lower().strip(),
            country=data.get("country", "Turkey"),
            region=data.get("region"),
            operator=data.get("operator"),
            geom=func.ST_SetSRID(func.ST_MakePoint(data["lng"], data["lat"]), 4326),
            strategic_score=data.get("strategic_score", 5.0),
            meta=data.get("metadata", {}),
            status="active",
            source="seed",
        )
        db.add(e)
        db.flush()
        entity_map[data["name"]] = e.id
        logger.info(f"  Entity: {data['name']} (id={e.id})")

    # Relations
    for from_name, to_name, rel_type, strength in SEED_RELATIONS:
        from_id = entity_map.get(from_name)
        to_id = entity_map.get(to_name)
        if from_id and to_id:
            r = EntityRelation(
                from_entity_id=from_id,
                to_entity_id=to_id,
                relation_type=rel_type,
                strength=strength,
            )
            db.add(r)
            logger.info(f"  Relation: {from_name} --[{rel_type}]--> {to_name}")

    db.commit()
    logger.info(f"Seeded {len(SEED_ENTITIES)} entities and {len(SEED_RELATIONS)} relations")


def seed_terrain_grid(db):
    result = generate_turkey_grid(db)
    logger.info(f"Terrain grid: {result}")


def main():
    init_db()
    db = SessionLocal()
    try:
        logger.info("=== Seeding GEOINT Database ===")
        seed_entities(db)
        seed_terrain_grid(db)
        logger.info("=== Seed Complete ===")
    finally:
        db.close()


if __name__ == "__main__":
    main()
