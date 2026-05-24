"""
Seed script: Create a dummy tracked person with multi-source surveillance evidence.

Generates:
- 1 target person (Ahmet Yilmaz / codename "Kartal")
- 2 associated persons
- ~20 surveillance records from 6 different source types
- Placeholder evidence images (PNG with metadata overlay)

Usage:
    python seed_surveillance.py
"""
import os
import sys
import struct
import zlib
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.engine import SessionLocal, init_db
from db.models import Person, PersonAlias, PersonMeeting, SurveillanceRecord
from db.compat import make_point


# ── Minimal PNG generator (no PIL dependency) ─────────────
def _create_png(width, height, bg_color, text_lines, filepath):
    """Create a simple colored PNG with burned-in text overlay using pure Python."""

    def _make_chunk(chunk_type, data):
        chunk = chunk_type + data
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', zlib.crc32(chunk) & 0xffffffff)

    # Simple solid color image
    r, g, b = bg_color
    raw_rows = b''
    for y in range(height):
        raw_rows += b'\x00'  # filter byte
        for x in range(width):
            # Draw a darker band for text area in top portion
            if y < 18 * len(text_lines) + 10:
                raw_rows += bytes([max(0, r - 60), max(0, g - 60), max(0, b - 60)])
            else:
                raw_rows += bytes([r, g, b])

    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)  # 8-bit RGB
    compressed = zlib.compress(raw_rows)

    png = b'\x89PNG\r\n\x1a\n'
    png += _make_chunk(b'IHDR', ihdr)
    png += _make_chunk(b'IDAT', compressed)
    png += _make_chunk(b'IEND', b'')

    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(png)


def _create_evidence_image(source_type, record_id, description, filepath):
    """Create a placeholder evidence image with appropriate color coding."""
    colors = {
        'cctv':            (40, 60, 40),     # dark green (night vision feel)
        'satellite':       (20, 30, 60),     # dark blue (orbital)
        'license_plate':   (50, 50, 50),     # dark gray (camera)
        'phone_intercept': (60, 20, 20),     # dark red (classified)
        'signal_tracking': (20, 50, 50),     # teal (electronic)
        'drone':           (40, 40, 60),     # indigo (aerial)
    }
    color = colors.get(source_type, (50, 50, 50))
    lines = [
        f"[{source_type.upper()}] Evidence #{record_id}",
        description[:60],
    ]
    _create_png(160, 120, color, lines, filepath)


# ── Evidence directory ────────────────────────────────────
EVIDENCE_DIR = Path(__file__).parent / "static" / "evidence"


# ── Dummy Data ─────────────────────────────────────────────

BASE_DATE = datetime(2026, 3, 10, tzinfo=timezone.utc)

TARGET_PERSON = {
    "name": "Ahmet Yilmaz",
    "name_normalized": "ahmet yilmaz",
    "role": "Silah kaçakçısı / Ağ koordinatörü",
    "nationality": "Türk",
    "profile_notes": "Güneydoğu hattında aktif, birden fazla sahte kimlik kullanıyor. İstanbul-Gaziantep-Kilis koridorunda düzenli seyahat.",
    "is_turkey_related": True,
    "organization_affiliation": "Uluslararası silah tedarik ağı — Kod adı: 'Bozkurt Hattı'",
    "personality_traits": "Dikkatli, yüz yüze görüşme tercih ediyor, telefon kullanımı minimal. Araç sık değiştiriyor. Sabah erken saatlerde aktif.",
}

ALIASES = [
    {"alias_name": "Kartal", "alias_type": "codename", "notes": "Telsiz ve kurye iletişimlerinde kullanılan kod adı"},
    {"alias_name": "Mehmet Demir", "alias_type": "fake_id", "notes": "Sahte TC kimlik — Gaziantep'te kullanıldığı tespit edildi"},
    {"alias_name": "Abu Tarek", "alias_type": "aka", "notes": "Suriye tarafı temaslarda kullanılan isim"},
]

ASSOCIATE_1 = {
    "name": "Hasan Kaya",
    "name_normalized": "hasan kaya",
    "role": "Lojistik sorumlusu",
    "nationality": "Türk",
    "profile_notes": "Kamyon filosu sahibi, nakliye şirketini paravan olarak kullanıyor.",
}

ASSOCIATE_2 = {
    "name": "Dimitri Volkov",
    "name_normalized": "dimitri volkov",
    "role": "Tedarikçi",
    "nationality": "Ukraynalı",
    "profile_notes": "Odessa üzerinden malzeme sağlıyor, Türkiye'ye düzensiz girişler.",
}

# Surveillance records: (source_type, city, country, lat, lng, hours_offset, evidence_subtype, description, metadata)
SURVEILLANCE_DATA = [
    # ── Istanbul Phase ──
    ("cctv", "İstanbul", "Türkiye", 41.0082, 28.9784, 0,
     "image", "Atatürk Havalimanı çıkış kapısı — hedef beyaz gömlek, siyah çanta",
     {"camera_id": "IST-AYE-042", "angle": "45°", "resolution": "1080p", "weather": "açık"}),

    ("license_plate", "İstanbul", "Türkiye", 41.0135, 28.9553, 1,
     "image", "34 ABC 7721 plakalı siyah VW Passat — E5 otoyolu Bakırköy mevkii",
     {"plate_number": "34 ABC 7721", "vehicle_type": "sedan", "color": "siyah", "make": "VW Passat", "direction": "doğu"}),

    ("phone_intercept", "İstanbul", "Türkiye", 41.0422, 29.0083, 3,
     "audio", "Hedef → bilinmeyen numara: 'Malzeme hazır, yarın yola çıkıyorum'",
     {"caller": "+90532XXXX41", "callee": "+90544XXXX98", "duration": 47, "imsi": "28601XXXXXXXXX", "cell_tower": "Kadıköy-T14"}),

    ("signal_tracking", "İstanbul", "Türkiye", 41.0391, 29.0198, 6,
     "signal_data", "IMEI yakalama — hedefin telefonu Üsküdar baz istasyonunda",
     {"frequency": "1800MHz", "signal_type": "LTE", "device_id": "Samsung A54", "imei": "35267XXXXXXXXX"}),

    ("cctv", "İstanbul", "Türkiye", 41.0251, 29.0132, 8,
     "image", "Kadıköy iskele kamerası — hedef Hasan Kaya ile buluşma",
     {"camera_id": "IST-KDK-018", "angle": "90°", "resolution": "4K", "weather": "bulutlu"}),

    ("satellite", "İstanbul", "Türkiye", 41.0049, 28.8563, 12,
     "image", "Uydu görüntüsü — Ambarlı Limanı, şüpheli konteyner yükleme operasyonu",
     {"satellite_name": "Göktürk-2", "resolution_m": 2.5, "band": "pankromatik", "cloud_cover": "15%"}),

    # ── Transit: Istanbul → Ankara ──
    ("license_plate", "Bolu", "Türkiye", 40.7317, 31.6061, 18,
     "image", "34 ABC 7721 — Bolu Dağı Tüneli gişe kamerası",
     {"plate_number": "34 ABC 7721", "vehicle_type": "sedan", "color": "siyah", "make": "VW Passat", "direction": "doğu"}),

    ("signal_tracking", "Ankara", "Türkiye", 39.9208, 32.8541, 24,
     "signal_data", "IMEI tespit — Kızılay baz istasyonu, 14:00",
     {"frequency": "2100MHz", "signal_type": "LTE", "device_id": "Samsung A54", "imei": "35267XXXXXXXXX"}),

    # ── Ankara Phase ──
    ("cctv", "Ankara", "Türkiye", 39.9255, 32.8662, 26,
     "image", "Ankara Garı önü — hedef taksiden iniyor",
     {"camera_id": "ANK-GAR-007", "angle": "60°", "resolution": "1080p", "weather": "yağmurlu"}),

    ("drone", "Ankara", "Türkiye", 39.9180, 32.8600, 28,
     "image", "İHA görüntüsü — hedef Ulus'ta bir depoya giriyor",
     {"altitude_m": 120, "operator": "MİT-TAK", "flight_id": "DRN-2026-0312"}),

    ("phone_intercept", "Ankara", "Türkiye", 39.9208, 32.8541, 30,
     "audio", "Hedef → 'Abu Tarek': 'Ankara'dayım, Kilis'e geçiş için araç lazım'",
     {"caller": "+90532XXXX41", "callee": "+963XXXXXX22", "duration": 93, "imsi": "28601XXXXXXXXX", "cell_tower": "Ankara-Kzl-08"}),

    # ── Transit: Ankara → Gaziantep ──
    ("license_plate", "Adana", "Türkiye", 37.0000, 35.3213, 40,
     "image", "06 DEF 9912 — Adana gişe (PLAKA DEĞİŞMİŞ!)",
     {"plate_number": "06 DEF 9912", "vehicle_type": "SUV", "color": "beyaz", "make": "Toyota RAV4", "direction": "doğu"}),

    ("signal_tracking", "Gaziantep", "Türkiye", 37.0662, 37.3833, 48,
     "signal_data", "Yeni SIM tespit — aynı IMEI, farklı numara. Gaziantep merkez",
     {"frequency": "1800MHz", "signal_type": "LTE", "device_id": "Samsung A54", "imei": "35267XXXXXXXXX"}),

    # ── Gaziantep Phase ──
    ("cctv", "Gaziantep", "Türkiye", 37.0585, 37.3800, 50,
     "image", "Şehitkamil Sanayi Sitesi — hedef bir depo önünde",
     {"camera_id": "GAZ-SNY-003", "angle": "30°", "resolution": "720p", "weather": "açık"}),

    ("satellite", "Gaziantep", "Türkiye", 37.0750, 37.3900, 52,
     "image", "Uydu — sanayi bölgesinde şüpheli araç hareketleri",
     {"satellite_name": "Göktürk-2", "resolution_m": 2.5, "band": "multispektral", "cloud_cover": "5%"}),

    ("cctv", "Gaziantep", "Türkiye", 37.0662, 37.3833, 54,
     "image", "Otel lobisi — hedef Dimitri Volkov ile buluşma",
     {"camera_id": "GAZ-HTL-LOBBY", "angle": "wide", "resolution": "1080p", "weather": "iç mekan"}),

    # ── Kilis / Border Phase ──
    ("drone", "Kilis", "Türkiye", 36.7184, 37.1212, 60,
     "image", "İHA — Kilis kırsalında şüpheli araç durağı (sınır hattı 2km)",
     {"altitude_m": 200, "operator": "TSK-İHA", "flight_id": "DRN-2026-0314"}),

    ("signal_tracking", "Kilis", "Türkiye", 36.7100, 37.1150, 62,
     "signal_data", "Hedefin telefonu Suriye operatörü sinyali aldı — roaming",
     {"frequency": "900MHz", "signal_type": "2G", "device_id": "Samsung A54", "imei": "35267XXXXXXXXX"}),

    ("cctv", "Kilis", "Türkiye", 36.7184, 37.1150, 63,
     "image", "Sınır karakolu kamerası — beyaz SUV sınıra yaklaşıyor",
     {"camera_id": "KLS-SNR-001", "angle": "180° panoramik", "resolution": "4K", "weather": "tozlu"}),

    ("satellite", "Kilis", "Türkiye", 36.7050, 37.1000, 66,
     "image", "Uydu — sınır bölgesinde gece termal aktivite tespit",
     {"satellite_name": "Göktürk-1", "resolution_m": 1.0, "band": "termal IR", "cloud_cover": "0%"}),
]

MEETINGS = [
    {
        "associate": "Hasan Kaya",
        "date_offset_hours": 8,
        "city": "İstanbul", "country": "Türkiye",
        "lat": 41.0251, "lng": 29.0132,
        "meeting_type": "coordination",
        "context": "Kadıköy iskelede lojistik planlama görüşmesi — nakliye rotası belirlendi",
    },
    {
        "associate": "Dimitri Volkov",
        "date_offset_hours": 54,
        "city": "Gaziantep", "country": "Türkiye",
        "lat": 37.0662, "lng": 37.3833,
        "meeting_type": "negotiation",
        "context": "Otel lobisinde tedarik görüşmesi — fiyat ve teslimat tarihi konuşuldu",
    },
]


def seed():
    # Skip init_db() — tables already created by server startup
    # init_db()
    db = SessionLocal()

    try:
        # Check if already seeded
        existing = db.query(Person).filter(Person.name_normalized == "ahmet yilmaz").first()
        if existing:
            print(f"[!] Target person already exists (id={existing.id}). Deleting and re-seeding...")
            # Delete surveillance records
            db.query(SurveillanceRecord).filter(SurveillanceRecord.person_id == existing.id).delete()
            db.query(PersonAlias).filter(PersonAlias.person_id == existing.id).delete()
            db.delete(existing)
            db.commit()

        # ── Create target person ──
        target = Person(**TARGET_PERSON)
        target.first_seen = BASE_DATE
        target.last_seen = BASE_DATE + timedelta(hours=66)
        target.last_known_city = "Kilis"
        target.last_known_country = "Türkiye"
        target.mention_count = len(SURVEILLANCE_DATA)
        db.add(target)
        db.flush()
        print(f"[+] Created target: {target.name} (id={target.id})")

        # ── Aliases ──
        for a in ALIASES:
            alias = PersonAlias(person_id=target.id, first_seen_at=BASE_DATE, **a)
            db.add(alias)
        print(f"[+] Added {len(ALIASES)} aliases")

        # ── Associates ──
        assoc1 = db.query(Person).filter(Person.name_normalized == "hasan kaya").first()
        if not assoc1:
            assoc1 = Person(**ASSOCIATE_1, first_seen=BASE_DATE, last_seen=BASE_DATE + timedelta(hours=10))
            db.add(assoc1)
            db.flush()
            print(f"[+] Created associate: {assoc1.name} (id={assoc1.id})")

        assoc2 = db.query(Person).filter(Person.name_normalized == "dimitri volkov").first()
        if not assoc2:
            assoc2 = Person(**ASSOCIATE_2, first_seen=BASE_DATE + timedelta(hours=50), last_seen=BASE_DATE + timedelta(hours=56))
            db.add(assoc2)
            db.flush()
            print(f"[+] Created associate: {assoc2.name} (id={assoc2.id})")

        assoc_map = {"Hasan Kaya": assoc1, "Dimitri Volkov": assoc2}

        # ── Meetings ──
        for m in MEETINGS:
            assoc = assoc_map[m["associate"]]
            pm = PersonMeeting(
                person_a_id=target.id,
                person_b_id=assoc.id,
                meeting_date=BASE_DATE + timedelta(hours=m["date_offset_hours"]),
                location_country=m["country"],
                location_city=m["city"],
                geom=make_point(m["lng"], m["lat"]),
                meeting_type=m["meeting_type"],
                context=m["context"],
            )
            db.add(pm)
        print(f"[+] Added {len(MEETINGS)} meetings")

        # ── Surveillance Records + Evidence Images ──
        for i, (src_type, city, country, lat, lng, hrs, ev_type, desc, meta) in enumerate(SURVEILLANCE_DATA, 1):
            # Build evidence path
            fname = f"{src_type}_{i:03d}.png"
            ev_path = f"evidence/{src_type}/{fname}"
            full_path = EVIDENCE_DIR / src_type / fname

            # Create placeholder image
            _create_evidence_image(src_type, i, desc, full_path)

            rec = SurveillanceRecord(
                person_id=target.id,
                source_type=src_type,
                source_name=meta.get("camera_id") or meta.get("satellite_name") or meta.get("flight_id") or f"{src_type}-{i}",
                source_id=f"SRV-2026-{i:04d}",
                latitude=lat,
                longitude=lng,
                country=country,
                city=city,
                address=desc.split("—")[0].strip() if "—" in desc else "",
                captured_at=BASE_DATE + timedelta(hours=hrs),
                duration_seconds=meta.get("duration"),
                evidence_type=ev_type,
                evidence_path=ev_path,
                thumbnail_path=ev_path,  # same for now
                description=desc,
                confidence=0.85 if src_type in ("cctv", "satellite") else 0.7,
                metadata_json=meta,
                is_verified=(i % 3 == 0),  # every 3rd is verified
            )
            db.add(rec)

        db.commit()
        print(f"[+] Created {len(SURVEILLANCE_DATA)} surveillance records with evidence images")
        print()
        print("=" * 60)
        print(f"  TARGET: {target.name} (id={target.id})")
        print(f"  Aliases: {', '.join(a['alias_name'] for a in ALIASES)}")
        print(f"  Evidence folder: {EVIDENCE_DIR}")
        print(f"  Records: {len(SURVEILLANCE_DATA)} from 6 source types")
        print("=" * 60)
        print()
        print("Görüntü dosyaları oluşturuldu. Gerçek görüntülerle değiştirmek için:")
        print()
        for src_type in ["cctv", "satellite", "license_plate", "phone_intercept", "signal_tracking", "drone"]:
            p = EVIDENCE_DIR / src_type
            files = list(p.glob("*.png"))
            if files:
                print(f"  {p}/")
                for f in sorted(files):
                    print(f"    └── {f.name}")
        print()
        print("Bu dosyaları istediğiniz gerçek görüntülerle değiştirin — sistem otomatik gösterecek.")

    except Exception as e:
        db.rollback()
        print(f"[!] Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
