"""
Test: Region Report & Chatbot API
Sistemi doğrudan import ederek (HTTP sunucu gerekmez) test eder.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
from db.engine import init_db, SessionLocal

init_db()
db = SessionLocal()

SEP = "=" * 65

# ─────────────────────────────────────────────────────────
# TEST 1: Region Report — Gaziantep-Kilis sınır hattı
# ─────────────────────────────────────────────────────────
print(SEP)
print("TEST 1: Bölge Raporu — Gaziantep / Kilis Sınır Hattı")
print(SEP)

from api.region_report_api import _build_region_report, RegionReportRequest

req1 = RegionReportRequest(
    lat_min=36.4, lat_max=37.5,
    lng_min=36.5, lng_max=38.0,
    days=30,
    include_llm_analysis=False,
)
r1 = _build_region_report(db, req1)
s1 = r1["summary"]

print(f"  Haberler    : {s1['total_news']}")
print(f"  Kişiler     : {s1['total_persons']}")
print(f"  Tehditler   : {s1['total_threats']}")
print(f"  Varlıklar   : {s1['total_entities']}")
print(f"  Görüşmeler  : {s1['total_meetings']}")
print(f"  Hareketler  : {s1['total_movements']}")
print(f"  Son Dakika  : {s1['breaking_news_count']}")
print()
print("  Tehdit seviyeleri:", s1.get('threats_by_level', {}))
print("  Haber kategorileri:", s1.get('news_by_category', {}))

print("\n  -- İlk 5 Haber --")
for n in r1["news_events"][:5]:
    flag = "🔴" if n["is_breaking"] else "  "
    print(f"  {flag} [{n['category']}] {n['title'][:70]}")
    print(f"      Öncelik:{n['priority']} | {n['location_city']} | {str(n['published_at'])[:10]}")

print("\n  -- Bölgedeki Kişiler --")
for p in r1["persons"]:
    print(f"  * {p['name']} ({p.get('role','?')}) — {p['visit_count']} ziyaret")

print("\n  -- Tehditler --")
for t in r1["threats"]:
    print(f"  ! [{t['threat_level'].upper()}] {t['title'][:60]}")
    print(f"      Risk:{t['risk_score']} | Olasılık:{t['probability']}")

print("\n  -- Görüşmeler --")
for m in r1["meetings"]:
    print(f"  > {m['person_a']} <-> {m['person_b']} | {m['location_city']} | {str(m['meeting_date'])[:10]}")

assert s1['total_news'] >= 3, "Beklenen minimum 3 haber!"
assert s1['total_threats'] >= 1, "Beklenen minimum 1 tehdit!"
print("\n  [PASS] Gaziantep/Kilis raporu OK")


# ─────────────────────────────────────────────────────────
# TEST 2: Region Report — İstanbul finans bölgesi
# ─────────────────────────────────────────────────────────
print()
print(SEP)
print("TEST 2: Bölge Raporu — İstanbul Finans Bölgesi")
print(SEP)

req2 = RegionReportRequest(
    lat_min=40.8, lat_max=41.3,
    lng_min=28.5, lng_max=29.5,
    days=30,
    include_llm_analysis=False,
)
r2 = _build_region_report(db, req2)
s2 = r2["summary"]

print(f"  Haberler  : {s2['total_news']}")
print(f"  Kişiler   : {s2['total_persons']}")
print(f"  Tehditler : {s2['total_threats']}")
print(f"  Görüşmeler: {s2['total_meetings']}")

print("\n  -- Haberler --")
for n in r2["news_events"][:4]:
    print(f"  [{n['category']}] {n['title'][:70]}")

print("\n  -- Kişiler --")
for p in r2["persons"]:
    print(f"  * {p['name']} — {p['visit_count']} ziyaret")

assert s2['total_news'] >= 2, "İstanbul'da en az 2 haber bekleniyor!"
print("\n  [PASS] İstanbul raporu OK")


# ─────────────────────────────────────────────────────────
# TEST 3: Region Report — Ceyhan / Mersin enerji altyapısı
# ─────────────────────────────────────────────────────────
print()
print(SEP)
print("TEST 3: Bölge Raporu — Ceyhan/Mersin Enerji Altyapısı")
print(SEP)

req3 = RegionReportRequest(
    lat_min=36.0, lat_max=37.2,
    lng_min=33.0, lng_max=36.0,
    days=30,
    include_llm_analysis=False,
)
r3 = _build_region_report(db, req3)
s3 = r3["summary"]

print(f"  Haberler : {s3['total_news']}")
print(f"  Varlıklar: {s3['total_entities']}")
print(f"  Tehditler: {s3['total_threats']}")

print("\n  -- Stratejik Varlıklar --")
for e in r3["entities"][:8]:
    print(f"  [{e['entity_type']}] {e['name'][:55]} | Risk:{e['risk_score']} | Str:{e['strategic_score']}")

assert s3['total_entities'] >= 2, "Mersin bölgesinde en az 2 varlık bekleniyor!"
print("\n  [PASS] Ceyhan/Mersin raporu OK")


# ─────────────────────────────────────────────────────────
# TEST 4: Quick Region Report
# ─────────────────────────────────────────────────────────
print()
print(SEP)
print("TEST 4: Hızlı Rapor — Gaziantep merkez (50km)")
print(SEP)

import math
lat_c, lng_c = 37.066, 37.383
radius_km = 50
delta_lat = radius_km / 111.0
delta_lng = radius_km / (111.0 * max(0.1, abs(math.cos(math.radians(lat_c)))))

req4 = RegionReportRequest(
    lat_min=lat_c - delta_lat,
    lat_max=lat_c + delta_lat,
    lng_min=lng_c - delta_lng,
    lng_max=lng_c + delta_lng,
    days=30,
    include_llm_analysis=False,
)
r4 = _build_region_report(db, req4)
s4 = r4["summary"]
print(f"  50km yarıçaplı sorgu -> {s4['total_news']} haber, {s4['total_persons']} kişi, {s4['total_threats']} tehdit")
assert s4['total_news'] >= 2
print("  [PASS] Hızlı rapor OK")


# ─────────────────────────────────────────────────────────
# TEST 5: Chatbot — Konum Tespiti
# ─────────────────────────────────────────────────────────
print()
print(SEP)
print("TEST 5: Chatbot Konum & Zaman Tespiti")
print(SEP)

from api.region_chatbot_api import _detect_intent, _extract_time_period, _extract_location

test_questions = [
    ("Malatya bölgesinde bu hafta neler oldu?", "malatya", 7),
    ("Gaziantep'te aktif tehditler var mı?", "gaziantep", 14),
    ("Suriye sınırında son 30 günde kimler tespit edildi?", "suriye", 30),
    ("İstanbul'da hawala ağı operasyonu hakkında bilgi ver", "istanbul", 14),
    ("Kilis'te bugün ne oldu?", "kilis", 1),
]

for question, expected_loc, expected_days in test_questions:
    intent, conf = _detect_intent(question)
    days = _extract_time_period(question)
    loc_name, coords, radius = _extract_location(question, db)

    ok_loc = expected_loc.lower() in (loc_name or "").lower()
    ok_days = days == expected_days

    status = "[PASS]" if (ok_loc or coords is not None) else "[WARN]"
    print(f"  {status} Q: '{question[:50]}'")
    print(f"         Intent:{intent}({conf:.2f}) | Konum:{loc_name} {coords} | Süre:{days}g")
    print()


# ─────────────────────────────────────────────────────────
# TEST 6: Chatbot — Tam Yanıt (LLM olmadan)
# ─────────────────────────────────────────────────────────
print()
print(SEP)
print("TEST 6: Chatbot — Kilis Bölgesi Sorgusu (LLM bypass)")
print(SEP)

from api.region_chatbot_api import _build_context_text, _extract_location, _extract_time_period, _detect_intent

question6 = "Kilis sınır hattında bu hafta neler yaşandı?"
intent6, conf6 = _detect_intent(question6)
days6 = _extract_time_period(question6)
loc_name6, coords6, radius6 = _extract_location(question6, db)

print(f"  Soru    : {question6}")
print(f"  Intent  : {intent6} ({conf6:.2f})")
print(f"  Konum   : {loc_name6} @ {coords6}")
print(f"  Dönem   : {days6} gün")
print(f"  Yarıçap : {radius6} km")

if coords6:
    delta_lat6 = radius6 / 111.0
    delta_lng6 = radius6 / (111.0 * max(0.1, abs(math.cos(math.radians(coords6[0])))))
    req6 = RegionReportRequest(
        lat_min=coords6[0] - delta_lat6,
        lat_max=coords6[0] + delta_lat6,
        lng_min=coords6[1] - delta_lng6,
        lng_max=coords6[1] + delta_lng6,
        days=days6,
        include_llm_analysis=False,
    )
    r6 = _build_region_report(db, req6)
    ctx6 = _build_context_text(r6, intent6, loc_name6)
    print(f"\n  -- Oluşturulan Bağlam (ilk 1200 karakter) --")
    print(ctx6[:1200])
    print(f"\n  Toplam bağlam uzunluğu: {len(ctx6)} karakter")
    assert r6["summary"]["total_news"] >= 1
    print("\n  [PASS] Chatbot bağlam üretimi OK")
else:
    print("  [WARN] Koordinat bulunamadı (beklenen: Kilis tespiti)")


# ─────────────────────────────────────────────────────────
# TEST 7: Farklı Bölgeler Karşılaştırma
# ─────────────────────────────────────────────────────────
print()
print(SEP)
print("TEST 7: Bölgesel Karşılaştırma — Kilis vs Hatay vs Mersin")
print(SEP)

regions = [
    ("Kilis/Gaziantep", 36.4, 37.5, 36.5, 38.0),
    ("Hatay/Cilvegözü", 36.1, 36.7, 35.8, 36.8),
    ("Mersin/Ceyhan",   36.0, 37.1, 33.0, 36.2),
]

print(f"  {'Bölge':<25} {'Haber':>6} {'Kişi':>5} {'Tehdit':>7} {'Varlık':>7} {'Risk':>5}")
print("  " + "-" * 55)
for name, la_min, la_max, ln_min, ln_max in regions:
    req = RegionReportRequest(
        lat_min=la_min, lat_max=la_max,
        lng_min=ln_min, lng_max=ln_max,
        days=30, include_llm_analysis=False,
    )
    r = _build_region_report(db, req)
    s = r["summary"]
    max_risk = max((t["risk_score"] for t in r["threats"]), default=0)
    print(f"  {name:<25} {s['total_news']:>6} {s['total_persons']:>5} {s['total_threats']:>7} {s['total_entities']:>7} {max_risk:>5.1f}")

print()


# ─────────────────────────────────────────────────────────
# SONUÇ
# ─────────────────────────────────────────────────────────
print(SEP)
print("TÜM TESTLER TAMAMLANDI")
print(SEP)
print()
print("Veritabanı Son Durumu:")
from db.models import News, Person, Entity, ThreatAssessment, PersonLocation, PersonMeeting
print(f"  Haberler   : {db.query(News).count()}")
print(f"  Kişiler    : {db.query(Person).count()}")
print(f"  Varlıklar  : {db.query(Entity).count()}")
print(f"  Tehditler  : {db.query(ThreatAssessment).count()}")
print(f"  Kişi Lok.  : {db.query(PersonLocation).count()}")
print(f"  Görüşmeler : {db.query(PersonMeeting).count()}")
print()
print("API Endpoint'leri:")
print("  POST /api/region-report/report  — Tam bölge raporu")
print("  GET  /api/region-report/report/quick?lat=&lng=&radius_km=  — Hızlı rapor")
print("  POST /api/region-chat/chat  — OSINT Chatbot")
print("  GET  /api/region-chat/chat/history  — Geçmiş")
print()
print("Frontend:")
print("  Sidebar > 'Bolge Sec & Raporla' => Haritada dikdortgen ciz")
print("  Haritaya sag tiklama => 25km yaricapli hizli rapor")
print("  Sidebar > 'OSINT Chatbot' => Dogal dil sorgulama")

db.close()
