"""
Operational Intelligence Seed Data — Geofences, Link Analysis, PoL, Timeline, Red Team.
Run: python seed_operations.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timezone, timedelta
from db.engine import SessionLocal, init_db
from db.models import (
    Person, PersonLocation, PersonMeeting, PersonRelationship,
    SurveillanceRecord,
    Geofence, GeofenceEvent, PatternOfLife,
    LinkEntity, LinkConnection, ReconstructedTimeline,
    RedTeamAnalysis,
)
from db.compat import make_point


def utcnow():
    return datetime.now(timezone.utc)


def seed():
    init_db()
    db = SessionLocal()

    # Check if already seeded
    if db.query(Geofence).count() > 0:
        print("Operations data already seeded. Skipping.")
        db.close()
        return

    print("Seeding Operational Intelligence data...")

    # ── Ensure target persons exist ──────────────────────
    target = db.query(Person).filter(Person.name_normalized == "ali yilmaz").first()
    if not target:
        target = Person(
            name="Ali Yilmaz", name_normalized="ali yilmaz",
            role="Suspected Logistics Coordinator", nationality="TR",
            is_turkey_related=True,
        )
        db.add(target)
        db.flush()
        print("  [OK] Target person created: Ali Yilmaz")

    contact1 = db.query(Person).filter(Person.name_normalized == "hassan omar").first()
    if not contact1:
        contact1 = Person(
            name="Hassan Omar", name_normalized="hassan omar",
            role="Border Courier", nationality="SY",
        )
        db.add(contact1)
        db.flush()

    contact2 = db.query(Person).filter(Person.name_normalized == "dimitri volkov").first()
    if not contact2:
        contact2 = Person(
            name="Dimitri Volkov", name_normalized="dimitri volkov",
            role="Arms Dealer", nationality="RU",
        )
        db.add(contact2)
        db.flush()

    contact3 = db.query(Person).filter(Person.name_normalized == "fatima al-rashid").first()
    if not contact3:
        contact3 = Person(
            name="Fatima Al-Rashid", name_normalized="fatima al-rashid",
            role="Financial Facilitator", nationality="LB",
        )
        db.add(contact3)
        db.flush()
    db.commit()

    now = utcnow()

    # ── PERSON LOCATIONS (movement data for PoL & Timeline) ──
    # PersonLocation uses: geom (PortableGeometry), timestamp, location_type
    locations = [
        # Home base: Ankara Kizilay area
        PersonLocation(person_id=target.id, geom=make_point(32.86, 39.92),
                       city="Ankara", country="Turkey", location_type="event", timestamp=now - timedelta(days=60)),
        PersonLocation(person_id=target.id, geom=make_point(32.861, 39.921),
                       city="Ankara", country="Turkey", location_type="event", timestamp=now - timedelta(days=58)),
        PersonLocation(person_id=target.id, geom=make_point(32.859, 39.919),
                       city="Ankara", country="Turkey", location_type="event", timestamp=now - timedelta(days=55)),
        PersonLocation(person_id=target.id, geom=make_point(32.86, 39.92),
                       city="Ankara", country="Turkey", location_type="event", timestamp=now - timedelta(days=50)),
        # Travel corridor: Ankara -> Istanbul
        PersonLocation(person_id=target.id, geom=make_point(28.98, 41.01),
                       city="Istanbul", country="Turkey", location_type="event", timestamp=now - timedelta(days=45)),
        PersonLocation(person_id=target.id, geom=make_point(28.975, 41.015),
                       city="Istanbul", country="Turkey", location_type="event", timestamp=now - timedelta(days=44)),
        PersonLocation(person_id=target.id, geom=make_point(28.985, 41.008),
                       city="Istanbul", country="Turkey", location_type="event", timestamp=now - timedelta(days=43)),
        # Back to Ankara
        PersonLocation(person_id=target.id, geom=make_point(32.86, 39.92),
                       city="Ankara", country="Turkey", location_type="event", timestamp=now - timedelta(days=40)),
        # Travel corridor: Ankara -> Hatay (border area)
        PersonLocation(person_id=target.id, geom=make_point(36.16, 36.20),
                       city="Hatay", country="Turkey", location_type="event", timestamp=now - timedelta(days=30)),
        PersonLocation(person_id=target.id, geom=make_point(36.15, 36.21),
                       city="Hatay", country="Turkey", location_type="event", timestamp=now - timedelta(days=29)),
        PersonLocation(person_id=target.id, geom=make_point(36.17, 36.19),
                       city="Hatay", country="Turkey", location_type="event", timestamp=now - timedelta(days=28)),
        # Back to Ankara
        PersonLocation(person_id=target.id, geom=make_point(32.86, 39.92),
                       city="Ankara", country="Turkey", location_type="event", timestamp=now - timedelta(days=25)),
        # Suspicious trip: Ankara -> Gaziantep
        PersonLocation(person_id=target.id, geom=make_point(37.38, 37.06),
                       city="Gaziantep", country="Turkey", location_type="event", timestamp=now - timedelta(days=15)),
        PersonLocation(person_id=target.id, geom=make_point(37.375, 37.065),
                       city="Gaziantep", country="Turkey", location_type="event", timestamp=now - timedelta(days=14)),
        # Recent: back Ankara
        PersonLocation(person_id=target.id, geom=make_point(32.86, 39.92),
                       city="Ankara", country="Turkey", location_type="event", timestamp=now - timedelta(days=5)),
        PersonLocation(person_id=target.id, geom=make_point(32.862, 39.918),
                       city="Ankara", country="Turkey", location_type="event", timestamp=now - timedelta(days=2)),
    ]
    db.add_all(locations)
    db.flush()
    print(f"  [OK] {len(locations)} person locations")

    # ── SURVEILLANCE RECORDS ──
    # SurveillanceRecord uses: source_type, captured_at, latitude, longitude
    surveillances = [
        SurveillanceRecord(
            person_id=target.id, source_type="cctv",
            latitude=39.92, longitude=32.86, country="Turkey", city="Ankara",
            description="Hedef Kizilay'da bir kafede Hassan Omar ile bulustu. 45 dk gorusme, zarf degisimi.",
            captured_at=now - timedelta(days=50),
        ),
        SurveillanceRecord(
            person_id=target.id, source_type="phone_intercept",
            latitude=41.01, longitude=28.98, country="Turkey", city="Istanbul",
            description="Hedefin Istanbul'da sifrelenmis mesajlasma kullandigi tespit edildi. Signal uygulamasi.",
            captured_at=now - timedelta(days=44),
        ),
        SurveillanceRecord(
            person_id=target.id, source_type="cctv",
            latitude=36.20, longitude=36.16, country="Turkey", city="Hatay",
            description="Hedef Hatay sinir bolgesinde kimliksiz arac ile goruntulendu. Plaka takibi baslandi.",
            captured_at=now - timedelta(days=29),
        ),
        SurveillanceRecord(
            person_id=target.id, source_type="financial",
            latitude=39.92, longitude=32.86, country="Turkey", city="Ankara",
            description="Hedefin hesabina 50.000 USD kaynak belirsiz havale tespit edildi. Western Union.",
            captured_at=now - timedelta(days=20),
        ),
        SurveillanceRecord(
            person_id=target.id, source_type="phone_intercept",
            latitude=37.06, longitude=37.38, country="Turkey", city="Gaziantep",
            description="Hedefin Gaziantep'te Suriyeli numaralarla 12 telefon gorusmesi. Toplam 87 dakika.",
            captured_at=now - timedelta(days=14),
        ),
    ]
    db.add_all(surveillances)
    db.flush()
    print(f"  [OK] {len(surveillances)} surveillance records")

    # ── MEETINGS ──
    # PersonMeeting uses: geom, location_country, location_city, meeting_type, context
    meetings = [
        PersonMeeting(
            person_a_id=target.id, person_b_id=contact1.id,
            meeting_date=now - timedelta(days=50),
            geom=make_point(32.86, 39.92),
            location_country="Turkey", location_city="Ankara",
            meeting_type="face_to_face",
            context="Kizilay Kafe - Zarf degisimi gozlemlendi. 45 dakika surdu.",
        ),
        PersonMeeting(
            person_a_id=target.id, person_b_id=contact2.id,
            meeting_date=now - timedelta(days=43),
            geom=make_point(28.975, 41.015),
            location_country="Turkey", location_city="Istanbul",
            meeting_type="face_to_face",
            context="Beyoglu Otel - Istanbul'da otel lobisinde bulusma. Volkov 2 bavulla geldi.",
        ),
        PersonMeeting(
            person_a_id=target.id, person_b_id=contact3.id,
            meeting_date=now - timedelta(days=15),
            geom=make_point(37.38, 37.06),
            location_country="Turkey", location_city="Gaziantep",
            meeting_type="face_to_face",
            context="Gaziantep Restoran - Fatima ile gorusme. Mali dokuman alisverisi.",
        ),
    ]
    db.add_all(meetings)
    db.flush()
    print(f"  [OK] {len(meetings)} meetings")

    # ── RELATIONSHIPS ──
    # PersonRelationship uses: person_a_id, person_b_id, relation_type, source_summary
    rels = [
        PersonRelationship(
            person_a_id=target.id, person_b_id=contact1.id,
            relation_type="meeting", strength=0.8, evidence_count=3,
            source_summary="Hassan Omar ile duzenli temas. Sinir lojistigi baglantisi.",
        ),
        PersonRelationship(
            person_a_id=target.id, person_b_id=contact2.id,
            relation_type="meeting", strength=0.6, evidence_count=1,
            source_summary="Dimitri Volkov ile silah ticareti suphesi.",
        ),
        PersonRelationship(
            person_a_id=target.id, person_b_id=contact3.id,
            relation_type="meeting", strength=0.7, evidence_count=2,
            source_summary="Fatima Al-Rashid ile mali transferler.",
        ),
    ]
    db.add_all(rels)
    db.flush()
    print(f"  [OK] {len(rels)} relationships")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # GEOFENCES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Geofence uses: zone_type, geom (center POINT), trigger_on, severity, target_person_ids, category
    geofences = [
        Geofence(
            name="Ankara Kizilay Gozetim Bolgesi",
            description="Hedefin ev/ofis bolgesi. Giris-cikis takibi.",
            zone_type="circle",
            geom=make_point(32.86, 39.92), radius_km=2.0,
            country="Turkey", city="Ankara",
            trigger_on="both", severity="warning",
            status="active", created_by="Analist Mehmet",
            category="surveillance",
        ),
        Geofence(
            name="Hatay Sinir Bolgesi",
            description="Suriye siniri yakinlari. Kritik gecis noktasi.",
            zone_type="circle",
            geom=make_point(36.16, 36.20), radius_km=10.0,
            country="Turkey", city="Hatay",
            trigger_on="enter", severity="critical",
            status="active", created_by="Analist Ayse",
            target_person_ids=[target.id],
            category="border",
        ),
        Geofence(
            name="Istanbul Havalimani Bolgesi",
            description="IST ve SAW havalimanlari cevresinde.",
            zone_type="circle",
            geom=make_point(28.74, 41.26), radius_km=15.0,
            country="Turkey", city="Istanbul",
            trigger_on="both", severity="warning",
            status="active", created_by="Sistem",
            category="restricted",
        ),
        Geofence(
            name="Gaziantep Operasyon Alani",
            description="Gaziantep sehir merkezi ve cevresi.",
            zone_type="polygon",
            polygon_coords=[
                [37.35, 36.95], [37.40, 36.95],
                [37.40, 37.15], [37.35, 37.15],
            ],
            country="Turkey", city="Gaziantep",
            trigger_on="enter", severity="critical",
            status="active", created_by="Analist Mehmet",
            target_person_ids=[target.id, contact1.id],
            category="military",
        ),
        Geofence(
            name="Erbil KRG Bolgesi (Pasif)",
            description="KRG istihbarat hedefi. Su an pasif.",
            zone_type="circle",
            geom=make_point(44.01, 36.19), radius_km=20.0,
            country="Iraq", city="Erbil",
            trigger_on="enter", severity="warning",
            status="paused", created_by="Analist Ahmet",
            category="diplomatic",
        ),
    ]
    db.add_all(geofences)
    db.flush()
    print(f"  [OK] {len(geofences)} geofences")

    # ── GEOFENCE EVENTS ──
    # GeofenceEvent: detected_at, distance_from_center_km, trigger_source, source_description
    gf_events = [
        GeofenceEvent(
            geofence_id=geofences[0].id,
            person_id=target.id,
            event_type="enter",
            latitude=39.921, longitude=32.861,
            distance_from_center_km=0.12,
            trigger_source="surveillance",
            source_description="Eve donus, gozetim tespit",
            detected_at=now - timedelta(days=25),
        ),
        GeofenceEvent(
            geofence_id=geofences[1].id,
            person_id=target.id,
            event_type="enter",
            latitude=36.20, longitude=36.16,
            distance_from_center_km=0.05,
            trigger_source="surveillance",
            source_description="KRITIK: Sinir bolgesine giris tespit edildi",
            detected_at=now - timedelta(days=30),
        ),
        GeofenceEvent(
            geofence_id=geofences[1].id,
            person_id=target.id,
            event_type="exit",
            latitude=36.30, longitude=36.25,
            distance_from_center_km=12.5,
            trigger_source="surveillance",
            source_description="Sinir bolgesinden ayrildi",
            detected_at=now - timedelta(days=28),
        ),
        GeofenceEvent(
            geofence_id=geofences[3].id,
            person_id=target.id,
            event_type="enter",
            latitude=37.06, longitude=37.38,
            distance_from_center_km=0.0,
            trigger_source="surveillance",
            source_description="Gaziantep'e giris. Fatima ile bulusma bekleniyor.",
            detected_at=now - timedelta(days=15),
        ),
    ]
    db.add_all(gf_events)
    db.flush()
    print(f"  [OK] {len(gf_events)} geofence events")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # LINK ANALYSIS ENTITIES & CONNECTIONS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # LinkEntity: entity_label, entity_metadata (not label, metadata)
    link_entities = [
        LinkEntity(
            entity_type="phone", entity_value="+90-555-123-4567",
            entity_label="Ali Yilmaz Ana Hat", person_id=target.id,
            entity_metadata={"carrier": "Turkcell", "registered": True},
        ),
        LinkEntity(
            entity_type="phone", entity_value="+90-555-987-6543",
            entity_label="Ali Yilmaz Prepaid", person_id=target.id,
            entity_metadata={"carrier": "Vodafone", "registered": False, "note": "Tek kullanimlik"},
        ),
        LinkEntity(
            entity_type="phone", entity_value="+963-944-555-111",
            entity_label="Hassan Omar SY", person_id=contact1.id,
            entity_metadata={"carrier": "Syriatel"},
        ),
        LinkEntity(
            entity_type="email", entity_value="d.volkov@proton.me",
            entity_label="Dimitri Volkov Mail", person_id=contact2.id,
            entity_metadata={"encrypted": True},
        ),
        LinkEntity(
            entity_type="bank_account", entity_value="TR33-0006-1005-1978-0010-1234-56",
            entity_label="Ali Yilmaz IBAN", person_id=target.id,
            entity_metadata={"bank": "Halkbank", "type": "personal"},
        ),
        LinkEntity(
            entity_type="bank_account", entity_value="LB12-0999-0000-0001-0019-0012-345",
            entity_label="Fatima IBAN", person_id=contact3.id,
            entity_metadata={"bank": "Bank Audi", "type": "business"},
        ),
        LinkEntity(
            entity_type="crypto_wallet", entity_value="bc1q42lja79elem0anu8q860g3ez...",
            entity_label="Supheli Bitcoin Cuzdan",
            entity_metadata={"blockchain": "bitcoin", "first_seen": "2026-01-15"},
        ),
        LinkEntity(
            entity_type="vehicle", entity_value="06-ABC-789",
            entity_label="Ali Yilmaz Arac", person_id=target.id,
            entity_metadata={"make": "Toyota", "model": "Corolla", "year": 2023, "color": "beyaz"},
        ),
        LinkEntity(
            entity_type="address", entity_value="Kizilay Mah. Ataturk Blv. No:42 Ankara",
            entity_label="Ali Yilmaz Adres", person_id=target.id,
        ),
    ]
    db.add_all(link_entities)
    db.flush()
    print(f"  [OK] {len(link_entities)} link entities")

    # Connections
    # LinkConnection: first_observed, last_observed, evidence_summary, total_amount, currency
    link_connections = [
        # Phone calls
        LinkConnection(
            source_id=link_entities[0].id, target_id=link_entities[2].id,
            connection_type="call",
            strength=0.85, frequency=24,
            first_observed=now - timedelta(days=90), last_observed=now - timedelta(days=5),
            evidence_summary="24 gorusme, ort. 8dk, yogun saatler 22:00-01:00",
        ),
        LinkConnection(
            source_id=link_entities[1].id, target_id=link_entities[2].id,
            connection_type="call",
            strength=0.6, frequency=5, is_suspicious=True,
            first_observed=now - timedelta(days=30), last_observed=now - timedelta(days=14),
            evidence_summary="Prepaid hat ile sinir oncesi iletisim, ort. 3dk",
        ),
        # Email
        LinkConnection(
            source_id=link_entities[0].id, target_id=link_entities[3].id,
            connection_type="email",
            strength=0.5, frequency=8,
            first_observed=now - timedelta(days=60), last_observed=now - timedelta(days=43),
            evidence_summary="Sifrelenmis e-posta, konu: Business Inquiry",
        ),
        # Financial transfers
        LinkConnection(
            source_id=link_entities[4].id, target_id=link_entities[5].id,
            connection_type="transfer",
            strength=0.9, frequency=6, is_suspicious=True,
            total_amount=285000.0, currency="USD",
            first_observed=now - timedelta(days=120), last_observed=now - timedelta(days=20),
            evidence_summary="6 havale, toplam 285K USD, ort. 47.5K",
        ),
        # Crypto
        LinkConnection(
            source_id=link_entities[4].id, target_id=link_entities[6].id,
            connection_type="transaction",
            strength=0.7, frequency=3, is_suspicious=True,
            first_observed=now - timedelta(days=45), last_observed=now - timedelta(days=10),
            evidence_summary="IBAN -> kripto borsasi -> BTC cuzdan, toplam 2.8 BTC",
        ),
        # Same person links (Ali's entities)
        LinkConnection(
            source_id=link_entities[0].id, target_id=link_entities[4].id,
            connection_type="associate",
            strength=1.0, frequency=1,
            evidence_summary="Ayni kisi sahipligi (dogrulanmis)",
        ),
        LinkConnection(
            source_id=link_entities[0].id, target_id=link_entities[7].id,
            connection_type="associate",
            strength=1.0, frequency=1,
            evidence_summary="Ayni kisi sahipligi (dogrulanmis)",
        ),
        LinkConnection(
            source_id=link_entities[0].id, target_id=link_entities[8].id,
            connection_type="associate",
            strength=1.0, frequency=1,
            evidence_summary="Ayni kisi sahipligi (dogrulanmis)",
        ),
    ]
    db.add_all(link_connections)
    db.flush()
    print(f"  [OK] {len(link_connections)} link connections ({sum(1 for c in link_connections if c.is_suspicious)} suspicious)")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PATTERN OF LIFE (pre-generated)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PatternOfLife: data_points_count, analysis_start/end, primary_contacts, anomalies_detected, routine_score
    pol = PatternOfLife(
        person_id=target.id,
        analysis_start=now - timedelta(days=60),
        analysis_end=now,
        data_points_count=len(locations) + len(surveillances) + len(meetings),
        home_base={"lat": 39.92, "lng": 32.86, "city": "Ankara", "country": "Turkey", "confidence": 0.95},
        frequent_locations=[
            {"lat": 39.92, "lng": 32.86, "city": "Ankara", "country": "Turkey", "visit_count": 8, "avg_duration_hours": 12, "purpose": "Ev/Ofis"},
            {"lat": 41.01, "lng": 28.98, "city": "Istanbul", "country": "Turkey", "visit_count": 3, "avg_duration_hours": 48, "purpose": "Toplanti"},
            {"lat": 36.20, "lng": 36.16, "city": "Hatay", "country": "Turkey", "visit_count": 3, "avg_duration_hours": 72, "purpose": "Sinir operasyonu"},
            {"lat": 37.06, "lng": 37.38, "city": "Gaziantep", "country": "Turkey", "visit_count": 2, "avg_duration_hours": 24, "purpose": "Bulusma"},
        ],
        travel_corridors=[
            {"from_city": "Ankara", "to_city": "Istanbul", "frequency": 3, "usual_transport": "Ucak/Kara", "avg_travel_hours": 5},
            {"from_city": "Ankara", "to_city": "Hatay", "frequency": 2, "usual_transport": "Kara", "avg_travel_hours": 8},
            {"from_city": "Ankara", "to_city": "Gaziantep", "frequency": 2, "usual_transport": "Kara", "avg_travel_hours": 7},
        ],
        active_hours={"start": "09:00", "end": "23:00", "timezone": "Europe/Istanbul"},
        weekly_pattern={
            "monday": [{"time": "09:00-18:00", "activity": "Ofis", "location": "Ankara"}],
            "friday": [{"time": "18:00-20:00", "activity": "Seyahate cikis", "location": "Ankara"}],
        },
        routine_score=0.72,
        primary_contacts=[
            {"name": "Hassan Omar", "person_id": contact1.id, "frequency": 3, "relationship": "associate", "last_contact": (now - timedelta(days=5)).isoformat()},
            {"name": "Dimitri Volkov", "person_id": contact2.id, "frequency": 1, "relationship": "business", "last_contact": (now - timedelta(days=43)).isoformat()},
            {"name": "Fatima Al-Rashid", "person_id": contact3.id, "frequency": 2, "relationship": "financial", "last_contact": (now - timedelta(days=15)).isoformat()},
        ],
        communication_windows=[
            {"day": "daily", "time_start": "22:00", "time_end": "01:00", "channel": "Signal", "contacts": ["Hassan Omar"]},
        ],
        anomalies_detected=[
            {"type": "unusual_travel", "description": "Hatay sinir bolgesine duzensiz ziyaretler", "severity": "high", "baseline_deviation": 0.8},
            {"type": "communication", "description": "Gece saatlerinde sifrelenmis iletisim", "severity": "medium", "baseline_deviation": 0.5},
            {"type": "financial", "description": "50.000 USD kaynagi belirsiz havale", "severity": "critical", "baseline_deviation": 0.95},
        ],
        predictability_score=0.72,
        vulnerability_windows=[
            {"day": "Cuma", "time": "18:00-20:00", "location": "Ankara cikis", "exposure_level": "high", "opportunity": "Seyahate cikis"},
            {"day": "Hafta sonu", "time": "tum gun", "location": "Hatay", "exposure_level": "medium", "opportunity": "Gozetim zor"},
        ],
        generated_by="system",
    )
    db.add(pol)
    db.flush()
    print("  [OK] 1 Pattern of Life analysis")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # RECONSTRUCTED TIMELINE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ReconstructedTimeline: title, time_start/end, total_events, source_breakdown, subject_name
    timeline = ReconstructedTimeline(
        person_id=target.id,
        title="Ali Yilmaz - 60 Gunluk Hareket Zaman Cigisi",
        subject_name="Ali Yilmaz",
        time_start=now - timedelta(days=60),
        time_end=now,
        total_events=12,
        events=[
            {"ts": (now - timedelta(days=60)).isoformat(), "type": "location", "source": "surveillance",
             "title": "Ankara Kizilay'da goruntulendi", "lat": 39.92, "lng": 32.86},
            {"ts": (now - timedelta(days=50)).isoformat(), "type": "meeting", "source": "surveillance",
             "title": "Hassan Omar ile bulusma (zarf degisimi)", "lat": 39.92, "lng": 32.86,
             "details": "Kizilay kafede 45 dk gorusme"},
            {"ts": (now - timedelta(days=45)).isoformat(), "type": "travel", "source": "passport_control",
             "title": "Istanbul'a seyahat", "lat": 41.01, "lng": 28.98},
            {"ts": (now - timedelta(days=44)).isoformat(), "type": "surveillance", "source": "electronic",
             "title": "Istanbul'da sifrelenmis iletisim tespit", "lat": 41.01, "lng": 28.98},
            {"ts": (now - timedelta(days=43)).isoformat(), "type": "meeting", "source": "surveillance",
             "title": "Dimitri Volkov ile otel bulusmasi", "lat": 41.015, "lng": 28.975,
             "details": "Volkov 2 bavulla geldi"},
            {"ts": (now - timedelta(days=40)).isoformat(), "type": "location", "source": "surveillance",
             "title": "Ankara'ya donus", "lat": 39.92, "lng": 32.86},
            {"ts": (now - timedelta(days=30)).isoformat(), "type": "geofence", "source": "phone_intercept",
             "title": "KRITIK: Hatay sinir bolgesine giris", "lat": 36.20, "lng": 36.16,
             "details": "Sinir bolgesi geofence tetiklendi"},
            {"ts": (now - timedelta(days=29)).isoformat(), "type": "surveillance", "source": "physical",
             "title": "Hatay'da kimliksiz arac ile goruntulendi", "lat": 36.20, "lng": 36.16},
            {"ts": (now - timedelta(days=20)).isoformat(), "type": "financial", "source": "financial",
             "title": "50.000 USD supheli havale", "lat": 39.92, "lng": 32.86,
             "details": "Western Union, kaynak belirsiz"},
            {"ts": (now - timedelta(days=15)).isoformat(), "type": "meeting", "source": "traffic_camera",
             "title": "Fatima Al-Rashid ile Gaziantep bulusmasi", "lat": 37.06, "lng": 37.38,
             "details": "Mali dokuman alisverisi"},
            {"ts": (now - timedelta(days=14)).isoformat(), "type": "surveillance", "source": "electronic",
             "title": "Gaziantep'te Suriyeli numaralarla 12 gorusme (87 dk)", "lat": 37.06, "lng": 37.38},
            {"ts": (now - timedelta(days=5)).isoformat(), "type": "location", "source": "surveillance",
             "title": "Ankara Kizilay'da goruntulendi", "lat": 39.92, "lng": 32.86},
        ],
        key_moments=[
            {"ts": (now - timedelta(days=50)).isoformat(), "title": "Hassan Omar ile zarf degisimi", "significance": "critical"},
            {"ts": (now - timedelta(days=43)).isoformat(), "title": "Volkov ile otel bulusmasi (silah?)", "significance": "critical"},
            {"ts": (now - timedelta(days=30)).isoformat(), "title": "Sinir bolgesi gecisi", "significance": "critical"},
            {"ts": (now - timedelta(days=20)).isoformat(), "title": "50K USD supheli havale", "significance": "high"},
            {"ts": (now - timedelta(days=15)).isoformat(), "title": "Fatima ile mali dokuman alisverisi", "significance": "high"},
        ],
        gaps=[
            {"from": (now - timedelta(days=40)).isoformat(), "to": (now - timedelta(days=30)).isoformat(),
             "duration_hours": 240, "note": "Ankara'dan Hatay'a arasi 10 gun kayip"},
        ],
        source_breakdown={"location": 5, "surveillance": 4, "meeting": 3, "geofence": 1, "financial": 1},
        generated_by="system",
    )
    db.add(timeline)
    db.flush()
    print("  [OK] 1 reconstructed timeline (12 events, 5 key moments)")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # RED TEAM ANALYSIS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    rta = RedTeamAnalysis(
        target_type="person", target_id=target.id,
        target_name="Ali Yilmaz",
        model_used="gemma3:12b",
        generated_by="ai",
        executive_summary=(
            "Ali Yilmaz, sinir otesi lojistik koordinasyonu suphelisi olarak yuksek oncelikli hedef. "
            "Ankara merkezli, Istanbul-Hatay-Gaziantep ucgeninde aktif. "
            "Mali, iletisim ve fiziksel gozetim aciklari mevcut. "
            "En kritik zafiyet: sinir bolgesindeki gozetim boslugu ve sifrelenmis iletisim."
        ),
        vulnerabilities=[
            {"title": "Duzensiz sinir seyahati", "description": "Hatay sinir bolgesine ongorilemez ziyaretler. Gozetim kaybi.", "severity": "critical", "exploitability": "high"},
            {"title": "Sifrelenmis iletisim", "description": "Signal kullanimi. Icerik takibi yapilamiyor.", "severity": "high", "exploitability": "moderate"},
            {"title": "Kaynak belirsiz mali akislar", "description": "50K USD ve kripto cuzdan baglantisi.", "severity": "critical", "exploitability": "high"},
            {"title": "Genis temas agi", "description": "3 farkli ulke vatandasi ile aktif iliski.", "severity": "high", "exploitability": "high"},
        ],
        attack_vectors=[
            {"name": "Mali kanal takibi", "description": "IBAN-kripto baglantisi uzerinden ag haritalama", "probability": "high", "impact": "critical", "prerequisites": "Mali istihbarat erisimi", "countermeasures": "Hedef kripto kullanmaya gecebilir"},
            {"name": "Iletisim dinleme", "description": "Signal metadata analizi + baz istasyonu triangulasyonu", "probability": "medium", "impact": "high", "prerequisites": "Teknik istihbarat", "countermeasures": "Cihaz degistirme riski"},
            {"name": "Cevre kaynagi devshirme", "description": "Hassan Omar veya Fatima uzerinden HUMINT", "probability": "medium", "impact": "high", "prerequisites": "HUMINT handler", "countermeasures": "Sadakat/korku faktoru"},
        ],
        exploitation_scenarios=[
            {"title": "Senaryo 1: Mali Tuzak", "description": "Sahte mali islem ile agdaki diger akterleri tespit", "likelihood": "medium"},
            {"title": "Senaryo 2: Sinir Operasyonu", "description": "Hatay ziyaretinde kontolu sinir gecis izleme", "likelihood": "high"},
        ],
        countermeasures=[
            {"measure": "7/24 gozetim sinir bolgesinde", "priority": "critical", "effectiveness": "high"},
            {"measure": "Mali istihbarat birimlerine bildirim", "priority": "critical", "effectiveness": "high"},
            {"measure": "Kripto cuzdan blockchain analizi", "priority": "high", "effectiveness": "medium"},
            {"measure": "Temas agindaki kisilere ayri gozetim", "priority": "high", "effectiveness": "medium"},
        ],
        detection_gaps=[
            {"gap": "Hatay-sinir bolgesinde 48-72 saat gozetim kaybi", "risk": "Sinir otesi faaliyet tespitsiz kalabilir", "recommendation": "Sinir bolgesinde sabit gozetim noktasi"},
            {"gap": "Sifrelenmis iletisim icerigi okunamiyor", "risk": "Operasyon planlama tespit edilemiyor", "recommendation": "Metadata + davranissal analiz guclendirme"},
            {"gap": "Kripto islemler tam izlenemiyor", "risk": "Fonlama agi eksik", "recommendation": "Blockchain analiz araci entegrasyonu"},
        ],
        overall_risk_level="critical",
        is_reviewed=True,
        reviewed_by="Albay Yildirim",
        analyst_review="Analiz tutarli ve kapsamli. Sinir bolgesi gozetim boslugu oncelikli olarak kapatilmali. Mali izleme MASAK ile koordine edilecek.",
    )
    db.add(rta)
    db.flush()
    print("  [OK] 1 Red Team analysis (reviewed)")

    db.commit()
    db.close()

    print("\n--- Operational Intelligence Seed Summary ---")
    print(f"  Persons:        4 (1 target + 3 contacts)")
    print(f"  Locations:      {len(locations)}")
    print(f"  Surveillances:  {len(surveillances)}")
    print(f"  Meetings:       {len(meetings)}")
    print(f"  Relationships:  {len(rels)}")
    print(f"  Geofences:      {len(geofences)}")
    print(f"  GF Events:      {len(gf_events)}")
    print(f"  Link Entities:  {len(link_entities)}")
    print(f"  Link Connections: {len(link_connections)}")
    print(f"  PoL Analyses:   1")
    print(f"  Timelines:      1")
    print(f"  Red Team:       1")
    print("Operational seed complete!")


if __name__ == "__main__":
    seed()
