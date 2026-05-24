"""
Seed Intelligence Data — Gerçekçi OSINT test verisi.

Mevcut hikaye arkı:
  - Türkiye-Suriye sınır hattında faaliyet gösteren kaçakçılık/silah ağı
  - Gaziantep (hub), Kilis (sınır), Adana (lojistik), İstanbul (finans)
  - Mevcut kişiler: Mehmet Karaca (lider), Elif Demir (finans),
    Ahmet Yilmaz (silah), Ali Yilmaz (lojistik), Hassan Omar (kurye)

Bu script mevcut veriye bağlı YENİ veriler ekler:
  - Stratejik varlıklar (Entity): sınır kapıları, askeri üsler, enerji altyapısı
  - Tehdit değerlendirmeleri (ThreatAssessment)
  - Kapsamlı haber serisi (News) — mevcut haberlerin devamı
  - Yeni kişi hareketleri (PersonLocation)
  - Yeni görüşmeler (PersonMeeting)
  - 2 yeni kişi: Suriyeli irtibat + Lübnan finans köprüsü

Çalıştırma: python seed_intelligence_data.py
"""
import sys
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from db.engine import init_db, SessionLocal
from db.models import (
    News, Person, PersonAlias, PersonLocation, PersonMeeting,
    Entity, ThreatAssessment, Organization, news_person, news_entity,
)
from db.compat import make_point, USING_POSTGRESQL

init_db()
db = SessionLocal()


def utc(days_ago=0, hour=10, minute=0):
    return datetime.now(timezone.utc) - timedelta(days=days_ago, hours=-hour, minutes=-minute)


def pt(lng, lat):
    """Make WKT/PostGIS point."""
    return make_point(lng, lat)


def add_commit(obj):
    db.add(obj)
    db.flush()
    return obj


print("=" * 60)
print("GEOINT SEED DATA — Başlıyor")
print("=" * 60)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. MEVCUT KİŞİLERİ GETİR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
persons = {p.id: p for p in db.query(Person).all()}
print(f"\n✓ Mevcut kişiler yüklendi: {len(persons)} kişi")

# ID'lere göre erişim kolaylığı için isim haritası
pid = {}
for p in persons.values():
    key = p.name.lower().replace(" ", "_")
    pid[key] = p.id

# İsimlerle eşle
ali_id = next((p.id for p in persons.values() if "Ali Yilmaz" in p.name), None)
hassan_id = next((p.id for p in persons.values() if "Hassan Omar" in p.name), None)
fatima_id = next((p.id for p in persons.values() if "Fatima" in p.name), None)
mehmet_id = next((p.id for p in persons.values() if "Mehmet Karaca" in p.name), None)
ibrahim_id = next((p.id for p in persons.values() if "Ibrahim Yildirim" in p.name), None)
elif_id = next((p.id for p in persons.values() if "Elif Demir" in p.name), None)
ahmet_id = next((p.id for p in persons.values() if "Ahmet Yilmaz" in p.name), None)
hasan_id = next((p.id for p in persons.values() if "Hasan Kaya" in p.name), None)

print(f"  Ali Yilmaz: {ali_id}")
print(f"  Hassan Omar: {hassan_id}")
print(f"  Fatima Al-Rashid: {fatima_id}")
print(f"  Mehmet Karaca: {mehmet_id}")
print(f"  Ibrahim Yildirim: {ibrahim_id}")
print(f"  Elif Demir: {elif_id}")
print(f"  Ahmet Yilmaz: {ahmet_id}")
print(f"  Hasan Kaya: {hasan_id}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. YENİ KİŞİLER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n--- Yeni Kişiler Ekleniyor ---")

# Mevcut mi kontrol et
def get_or_create_person(name, **kwargs):
    existing = db.query(Person).filter(Person.name == name).first()
    if existing:
        print(f"  (zaten var) {name}")
        return existing
    p = Person(name=name, **kwargs)
    db.add(p)
    db.flush()
    print(f"  + Eklendi: {name} [id={p.id}]")
    return p


# Kişi A: Suriyeli irtibat — Halep merkezli, Kilis sınırını kullanan ara kademe
kareem = get_or_create_person(
    "Kareem Al-Nasir",
    role="Suriyeli silah tedarikçisi / sınır arabulucusu",
    nationality="SY",
    profile_notes=(
        "Halep doğumlu, Türkiye-Suriye sınır koridorunu kullanan silah ve kaçak mal tedarikçisi. "
        "Kilis/Azez ekseninde faaliyet göstermekte. Mehmet Karaca ağı ile doğrudan temas. "
        "2019'dan bu yana aktif. Kilis'te bir akrabasının evinde konaklamaktadır."
    ),
    last_known_country="SY",
    last_known_city="Azez",
    geom=pt(36.58, 36.59),
    mention_count=4,
    first_seen=utc(90),
    last_seen=utc(12),
)

# Kişi B: Lübnan finans köprüsü — İstanbul'daki hawala ağının Beirut ayağı
nadia = get_or_create_person(
    "Nadia Mansour",
    role="Hawala operatörü / Lübnan finans köprüsü",
    nationality="LB",
    profile_notes=(
        "Beirut merkezli finansal aracı. İstanbul ve Gaziantep kuyumculuk sektörü üzerinden "
        "para transferi koordinasyonu yapıyor. Fatima Al-Rashid ile birlikte çalışmakta. "
        "Yılda 3-4 kez İstanbul ziyareti. BKM finans ağlarıyla bağlantısı araştırılıyor."
    ),
    last_known_country="LB",
    last_known_city="Beirut",
    geom=pt(35.49, 33.89),
    mention_count=3,
    first_seen=utc(60),
    last_seen=utc(8),
)

kareem_id = kareem.id
nadia_id = nadia.id

# Alias ekle
for alias_data in [
    (kareem_id, "Abu Kareem", "codename"),
    (kareem_id, "The Syrian", "nickname"),
    (nadia_id, "Ümm Nadia", "aka"),
]:
    existing = db.query(PersonAlias).filter(
        PersonAlias.person_id == alias_data[0],
        PersonAlias.alias_name == alias_data[1]
    ).first()
    if not existing:
        db.add(PersonAlias(person_id=alias_data[0], alias_name=alias_data[1], alias_type=alias_data[2]))

db.commit()
print(f"  Alias'lar eklendi.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. STRATEJİK VARLIKLAR (Entity)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n--- Stratejik Varlıklar Ekleniyor ---")

def get_or_create_entity(name, entity_type, lng, lat, **kwargs):
    existing = db.query(Entity).filter(Entity.name == name).first()
    if existing:
        print(f"  (zaten var) {name}")
        return existing
    e = Entity(
        name=name,
        entity_type=entity_type,
        geom=pt(lng, lat),
        name_normalized=name.lower(),
        source="manual",
        **kwargs,
    )
    db.add(e)
    db.flush()
    print(f"  + Eklendi: {name} ({entity_type}) [id={e.id}]")
    return e


entities = {}

# Sınır kapıları
entities["kilis_kapisi"] = get_or_create_entity(
    "Kilis-Öncüpınar Sınır Kapısı", "border_crossing", 37.033, 36.668,
    country="TR", region="Güneydoğu Anadolu",
    description="Türkiye-Suriye sınır kapısı. Kilis iline bağlı ticari ve insani yardım geçiş noktası. Kaçakçılık faaliyetleri için yüksek risk bölgesi.",
    status="active", risk_score=7.5, strategic_score=8.0, threat_level="high",
)

entities["cilvegozu"] = get_or_create_entity(
    "Cilvegözü Sınır Kapısı", "border_crossing", 36.625, 36.394,
    country="TR", region="Hatay",
    description="Hatay-Bab el-Hawa sınır geçişi. Suriye insani yardım koridoru. İkincil kaçakçılık rotası.",
    status="active", risk_score=6.8, strategic_score=7.5, threat_level="high",
)

# Askeri
entities["gazi_ussu"] = get_or_create_entity(
    "Gaziantep Hava Meydanı / NATO Lojistik Merkezi", "military_base", 37.478, 37.086,
    country="TR", region="Güneydoğu Anadolu",
    description="Gaziantep Oğuzeli Havalimanı yakınındaki askeri tesis. Suriye operasyonları için destek üssü.",
    status="active", risk_score=5.0, strategic_score=8.5, threat_level="medium",
)

entities["iskenderun_deniz"] = get_or_create_entity(
    "İskenderun Deniz Üssü", "naval_base", 36.185, 36.580,
    country="TR", region="Akdeniz",
    description="Türk Deniz Kuvvetleri İskenderun Körfezi komuta merkezi. Doğu Akdeniz gözetleme.",
    status="active", risk_score=4.5, strategic_score=9.0, threat_level="medium",
)

entities["karatas_radar"] = get_or_create_entity(
    "Karataş Radar İstasyonu", "radar_station", 35.366, 36.567,
    country="TR", region="Adana",
    description="Adana yakınlarındaki hava savunma radar sistemi. Suriye hava sahasını izler.",
    status="active", risk_score=3.5, strategic_score=9.5, threat_level="low",
)

# Enerji
entities["btc_ceyhan"] = get_or_create_entity(
    "Ceyhan BTC Ham Petrol Terminali", "pipeline", 35.834, 36.845,
    country="TR", region="Adana",
    description="Bakü-Tiflis-Ceyhan boru hattı Akdeniz terminali. Günlük 1 milyon varil kapasite. Stratejik enerji altyapısı.",
    status="active", risk_score=8.0, strategic_score=10.0, threat_level="high",
    operator="BOTAŞ",
)

entities["akkuyu_ngs"] = get_or_create_entity(
    "Akkuyu Nükleer Güç Santrali", "nuclear_plant", 33.543, 36.144,
    country="TR", region="Mersin",
    description="Türkiye'nin ilk nükleer enerji santrali. Rosatom inşası devam ediyor. 2026 kısmi devreye alım planlanıyor.",
    status="under_construction", risk_score=9.5, strategic_score=10.0, threat_level="critical",
    operator="ROSATOM/AKKUYU NGS",
)

# Liman
entities["mersin_limani"] = get_or_create_entity(
    "Mersin Uluslararası Limanı", "port", 34.633, 36.801,
    country="TR", region="Akdeniz",
    description="Türkiye'nin en büyük limanı. Kaçak mal ve silah transferi için risk noktası. Güvenlik denetimleri artırıldı.",
    status="active", risk_score=7.0, strategic_score=8.5, threat_level="high",
    operator="MIP",
)

# İstihbarat merkezi
entities["ankara_mgh"] = get_or_create_entity(
    "MİT Genel Müdürlüğü", "intelligence_hq", 32.852, 39.932,
    country="TR", region="İç Anadolu",
    description="Millî İstihbarat Teşkilatı genel merkezi.",
    status="active", risk_score=2.0, strategic_score=10.0, threat_level="low",
)

# Komuta merkezi
entities["hatay_komuta"] = get_or_create_entity(
    "Hatay İl Jandarma Komutanlığı", "command_center", 36.166, 36.402,
    country="TR", region="Hatay",
    description="Suriye sınırı operasyonlarını koordine eden jandarma komutanlığı.",
    status="active", risk_score=4.0, strategic_score=7.0, threat_level="medium",
)

db.commit()
print(f"  Toplam {len(entities)} varlık eklendi/kontrol edildi.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. YENİ HABERLER — Mevcut hikayeyi devam ettirir
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n--- Haberler Ekleniyor ---")

news_data = [
    # ── Sınır & Kaçakçılık devamı ──
    {
        "title": "Kilis'te dev kaçakçılık operasyonu: 'Kara Hat' ağına darbe",
        "content": (
            "Emniyet ve jandarma birimlerinin ortak yürüttüğü operasyonda Kilis sınır "
            "hattında faaliyet gösteren 'Kara Hat' ağının 3 üyesi gözaltına alındı. "
            "Ele geçirilen belgeler, ağın Gaziantep merkezli yönetimi ve Suriye bağlantılarına "
            "işaret etmektedir. Operasyon kapsamında Öncüpınar sınır kapısı çevresinde "
            "yoğun güvenlik önlemleri uygulandı."
        ),
        "source": "AA",
        "category": "conflict",
        "location_city": "Kilis",
        "location_country": "TR",
        "lng": 37.033, "lat": 36.668,
        "days_ago": 10, "priority": 9.2, "is_breaking": True,
        "summary": "'Kara Hat' kaçakçılık ağına yönelik operasyon: 3 gözaltı, Kilis sınırında güvenlik artırıldı.",
        "sentiment": "negative",
        "threat_relevance": 0.95,
        "person_ids": [mehmet_id, ahmet_id],
        "entity_ids": [entities["kilis_kapisi"].id if entities["kilis_kapisi"] else None],
    },
    {
        "title": "Azez'den Kilis'e tünel güzergahı tespit edildi",
        "content": (
            "Suriye'nin Azez bölgesinden Türkiye'ye uzandığı değerlendirilen ve "
            "kaçak mal ile silah transferinde kullanıldığı düşünülen yeraltı güzergahı "
            "jandarma tarafından tespit edildi. Suriyeli bağlantılı bir arabulucunun "
            "bu güzergahı organize ettiği ileri sürülmektedir. MİT ve jandarma istihbarat "
            "birimleri konuya ilişkin inceleme başlattı."
        ),
        "source": "TRT Haber",
        "category": "conflict",
        "location_city": "Azez",
        "location_country": "SY",
        "lng": 36.995, "lat": 36.590,
        "days_ago": 8, "priority": 8.8, "is_breaking": True,
        "summary": "Azez-Kilis hattında yeraltı kaçakçılık güzergahı tespit edildi.",
        "sentiment": "negative",
        "threat_relevance": 0.90,
        "person_ids": [kareem_id, hassan_id],
        "entity_ids": [entities["kilis_kapisi"].id if entities["kilis_kapisi"] else None],
    },
    {
        "title": "Gaziantep'te silah deposu ele geçirildi: 'Kara Hat' bağlantısı araştırılıyor",
        "content": (
            "Gaziantep'in Şahinbey ilçesinde bir sanayi deposunda düzenlenen operasyonda "
            "çeşitli hafif silah ve mühimmat ele geçirildi. Depoda bulunan belgeler, daha "
            "önce gözaltına alınan Ahmet Yilmaz ile bağlantılara işaret ediyor. Savcılık "
            "soruşturması genişletildi; örgütün Adana-Mersin üzerinden çalışan lojistik "
            "ağıyla ilişkileri inceleniyor."
        ),
        "source": "Hürriyet",
        "category": "conflict",
        "location_city": "Gaziantep",
        "location_country": "TR",
        "lng": 37.375, "lat": 37.058,
        "days_ago": 6, "priority": 9.0, "is_breaking": False,
        "summary": "Gaziantep sanayi deposunda silah ele geçirildi; Kara Hat bağlantısı araştırılıyor.",
        "sentiment": "negative",
        "threat_relevance": 0.92,
        "person_ids": [ahmet_id, hasan_id, mehmet_id],
        "entity_ids": [],
    },
    {
        "title": "Adana'da 'Kara Hat' ağının lojistik koordinatörü yakalandı",
        "content": (
            "Adana'da düzenlenen jandarma operasyonunda, 'Kara Hat' örgütünün lojistik ağını "
            "yönettiği değerlendirilen Hasan Kaya gözaltına alındı. Kaya'nın "
            "Gaziantep-Adana-Mersin güzergahında araç ve rota yönetimi yaptığı tespit edildi. "
            "Organizasyonun finansman ayağına yönelik soruşturmanın İstanbul koluna da sıçraması "
            "bekleniyor."
        ),
        "source": "CNN Türk",
        "category": "conflict",
        "location_city": "Adana",
        "location_country": "TR",
        "lng": 35.321, "lat": 37.002,
        "days_ago": 5, "priority": 8.5, "is_breaking": False,
        "summary": "Adana'da 'Kara Hat' lojistik koordinatörü Hasan Kaya gözaltında.",
        "sentiment": "negative",
        "threat_relevance": 0.88,
        "person_ids": [hasan_id, mehmet_id, ahmet_id],
        "entity_ids": [],
    },
    # ── Finans / Hawala devamı ──
    {
        "title": "İstanbul'da MASAK operasyonu: Hawala ağında 12 şirket incelemede",
        "content": (
            "Mali Suçları Araştırma Kurulu (MASAK), İstanbul'da faaliyet gösteren ve "
            "Suriye-Lübnan bağlantılı havale ağıyla ilişkili olduğu şüphesiyle 12 şirketin "
            "hesaplarını incelemeye aldı. İnceleme kapsamındaki firmaların kuyumculuk ve "
            "tekstil sektörlerinde faaliyet gösterdiği öğrenildi. Elif Demir'in bu şirketlerden "
            "ikisiyle bağlantısı araştırılmaktadır."
        ),
        "source": "Bloomberg HT",
        "category": "economy",
        "location_city": "Istanbul",
        "location_country": "TR",
        "lng": 28.978, "lat": 41.008,
        "days_ago": 7, "priority": 8.0, "is_breaking": False,
        "summary": "MASAK, Suriye-Lübnan hawala bağlantılı 12 İstanbul şirketini inceliyor.",
        "sentiment": "negative",
        "threat_relevance": 0.80,
        "person_ids": [elif_id, nadia_id, fatima_id],
        "entity_ids": [],
    },
    {
        "title": "Beirut-İstanbul finans köprüsü: Lübnanlı operatör ağa dahil oldu",
        "content": (
            "INTERPOL verilerine dayanılarak hazırlanan istihbarat değerlendirmesine göre, "
            "Beirut merkezli bir hawala operatörünün İstanbul ve Gaziantep üzerinden para "
            "transferi yaptığı tespit edildi. Söz konusu kişinin Suriye kaynaklı geliri "
            "Türkiye kuyumculuk sektörü aracılığıyla aklamakta olduğu değerlendirilmektedir."
        ),
        "source": "Sabah",
        "category": "economy",
        "location_city": "Istanbul",
        "location_country": "TR",
        "lng": 28.982, "lat": 41.012,
        "days_ago": 9, "priority": 7.8, "is_breaking": False,
        "summary": "Lübnanlı hawala operatörü İstanbul-Gaziantep para akış ağına dahil.",
        "sentiment": "negative",
        "threat_relevance": 0.75,
        "person_ids": [nadia_id, fatima_id, elif_id],
        "entity_ids": [],
    },
    # ── Enerji / Altyapı ──
    {
        "title": "Ceyhan BTC Terminali yakınında drone tespit edildi",
        "content": (
            "Ceyhan BTC ham petrol terminalinin yakınlarında tespit edilen bilinmeyen bir "
            "insansız hava aracı, bölge güvenlik birimlerini alarma geçirdi. Terminalin "
            "hava savunma sistemleri aktive edilirken, drone'un koordinatları takip altına "
            "alındı. Terminal yakınında keşif faaliyeti değerlendirmesi yapıldığı bildirildi."
        ),
        "source": "Milliyet",
        "category": "military",
        "location_city": "Ceyhan",
        "location_country": "TR",
        "lng": 35.813, "lat": 36.836,
        "days_ago": 4, "priority": 9.5, "is_breaking": True,
        "summary": "Ceyhan BTC Terminali yakınında bilinmeyen drone tespit edildi; güvenlik alarma geçirildi.",
        "sentiment": "negative",
        "threat_relevance": 0.98,
        "person_ids": [],
        "entity_ids": [entities["btc_ceyhan"].id if entities["btc_ceyhan"] else None],
    },
    {
        "title": "Akkuyu NGS güzergahında Rus lojistik konvoyu kontrol altında",
        "content": (
            "Rusya'dan Mersin'deki Akkuyu NGS inşaat sahasına ulaşan nükleer ekipman konvoyunun "
            "Adana-Mersin otoyolu üzerindeki geçişi, yoğun güvenlik protokolleri eşliğinde "
            "tamamlandı. Konvoy güzergahında jandarma ve polis ekiplerinin yanı sıra elektronik "
            "istihbarat araçları da konuşlandırıldı."
        ),
        "source": "NTV",
        "category": "politics",
        "location_city": "Mersin",
        "location_country": "TR",
        "lng": 33.526, "lat": 36.144,
        "days_ago": 11, "priority": 7.5, "is_breaking": False,
        "summary": "Akkuyu NGS ekipman konvoyu güvenlik zırhı altında Mersin'e ulaştı.",
        "sentiment": "neutral",
        "threat_relevance": 0.60,
        "person_ids": [],
        "entity_ids": [entities["akkuyu_ngs"].id if entities["akkuyu_ngs"] else None],
    },
    # ── Suriye / Bölgesel ──
    {
        "title": "Azez'de silahlı grup çatışması: Türkiye destekli güçler konuşlandı",
        "content": (
            "Kuzey Suriye'nin Azez bölgesinde rakip silahlı gruplar arasında çıkan çatışmada "
            "en az 7 kişi hayatını kaybetti. Türkiye destekli Suriye Milli Ordusu birimleri "
            "bölgeye takviye güç sevk etti. Çatışmanın kaçakçılık güzergahı kontrolü üzerindeki "
            "anlaşmazlıktan kaynaklandığı değerlendiriliyor."
        ),
        "source": "Al Jazeera Türkçe",
        "category": "conflict",
        "location_city": "Azez",
        "location_country": "SY",
        "lng": 36.993, "lat": 36.583,
        "days_ago": 3, "priority": 9.3, "is_breaking": True,
        "summary": "Azez'de silahlı grup çatışması: 7 ölü, Türkiye destekli güçler bölgede.",
        "sentiment": "negative",
        "threat_relevance": 0.95,
        "person_ids": [kareem_id, hassan_id],
        "entity_ids": [],
    },
    {
        "title": "Hatay-Suriye hattında kaçakçılık önleme operasyonu",
        "content": (
            "Hatay İl Jandarma Komutanlığı koordinasyonunda yürütülen operasyonda Cilvegözü "
            "sınır bölgesinden geçiş yapan iki araçta yaklaşık 200 kg esrar maddesinin "
            "yanı sıra 15 adet tabanca ele geçirildi. Operasyonda yabancı uyruklu bir kişi "
            "dahil toplam 4 şüpheli yakalandı."
        ),
        "source": "Sabah",
        "category": "conflict",
        "location_city": "Hatay",
        "location_country": "TR",
        "lng": 36.166, "lat": 36.402,
        "days_ago": 13, "priority": 8.2, "is_breaking": False,
        "summary": "Hatay Cilvegözü'nde 200 kg esrar ve 15 silah ele geçirildi.",
        "sentiment": "negative",
        "threat_relevance": 0.85,
        "person_ids": [hassan_id],
        "entity_ids": [entities["cilvegozu"].id if entities["cilvegozu"] else None],
    },
    # ── Ankara / Politik bağlam ──
    {
        "title": "Güney sınırı güvenliğine ilişkin TBMM gizli oturumu gerçekleştirildi",
        "content": (
            "Güney sınırı boyunca artan kaçakçılık ve silahlı geçiş girişimlerine ilişkin "
            "gizli değerlendirme oturumu TBMM Milli Savunma Komisyonu'nda gerçekleştirildi. "
            "Oturumda İçişleri, Dışişleri ve MİT temsilcileri bilgi sundu. Kilis-Hatay "
            "hattında 6 aylık operasyon verileri değerlendirildi."
        ),
        "source": "AA",
        "category": "politics",
        "location_city": "Ankara",
        "location_country": "TR",
        "lng": 32.854, "lat": 39.920,
        "days_ago": 14, "priority": 7.5, "is_breaking": False,
        "summary": "TBMM'de güney sınırı güvenliği gizli oturumu; İçişleri, Dışişleri ve MİT bilgi sundu.",
        "sentiment": "neutral",
        "threat_relevance": 0.65,
        "person_ids": [ali_id, ibrahim_id],
        "entity_ids": [entities["ankara_mgh"].id if entities["ankara_mgh"] else None],
    },
    {
        "title": "Mersin Limanı'nda şüpheli konteyner operasyonu: Silah ve kaçak elektronik",
        "content": (
            "Mersin Uluslararası Limanı'nda yapılan risk odaklı gümrük denetiminde, "
            "manifesto bilgileriyle örtüşmeyen bir konteyner tespit edildi. Konteynerda "
            "devre dışı bırakılmış silah parçaları ve ihracat yasağı kapsamındaki elektronik "
            "bileşenler bulundu. Kaçakçılık soruşturması başlatıldı."
        ),
        "source": "CNN Türk",
        "category": "conflict",
        "location_city": "Mersin",
        "location_country": "TR",
        "lng": 34.633, "lat": 36.801,
        "days_ago": 2, "priority": 8.7, "is_breaking": False,
        "summary": "Mersin Limanı'nda silah parçası ve kaçak elektronik içeren konteyner ele geçirildi.",
        "sentiment": "negative",
        "threat_relevance": 0.88,
        "person_ids": [ahmet_id],
        "entity_ids": [entities["mersin_limani"].id if entities["mersin_limani"] else None],
    },
    # ── Güncel / Son dakika ──
    {
        "title": "İstanbul'da 'Kara Hat' finans ağı soruşturmasında tutuklama",
        "content": (
            "İstanbul Cumhuriyet Savcılığı'nın yürüttüğü finansal suç soruşturması kapsamında "
            "'Kara Hat' ağının İstanbul finans ayağının yöneticisi konumundaki kişi tutuklandı. "
            "Tutuklanan kişinin, Gaziantep ve Mersin'deki operasyonlar için para transferini "
            "organize ettiği ileri sürülmektedir. Soruşturma kapsamında birden fazla banka "
            "hesabı donduruldu."
        ),
        "source": "Hürriyet",
        "category": "conflict",
        "location_city": "Istanbul",
        "location_country": "TR",
        "lng": 28.968, "lat": 41.011,
        "days_ago": 1, "priority": 9.1, "is_breaking": True,
        "summary": "'Kara Hat' finans yöneticisi İstanbul'da tutuklandı; banka hesapları donduruldu.",
        "sentiment": "negative",
        "threat_relevance": 0.93,
        "person_ids": [elif_id, ibrahim_id, nadia_id],
        "entity_ids": [],
    },
    {
        "title": "Gaziantep-Kilis sınır hattında HUMINT kaynaklı uyarı: Yeni sevkiyat bekleniyor",
        "content": (
            "İstihbarat kaynaklarından elde edilen bilgilere göre, 'Kara Hat' ağının "
            "son operasyonlarına rağmen faaliyetlerini yeniden organize ettiği ve önümüzdeki "
            "10 gün içinde Kilis sınırından yeni bir silah sevkiyatı planladığı değerlendirilmektedir. "
            "Güvenlik birimleri takviye güç konuşlandırarak alarmda bekliyor."
        ),
        "source": "Akşam",
        "category": "military",
        "location_city": "Kilis",
        "location_country": "TR",
        "lng": 37.115, "lat": 36.718,
        "days_ago": 0, "priority": 9.8, "is_breaking": True,
        "summary": "HUMINT uyarısı: Kilis hattında önümüzdeki 10 günde yeni silah sevkiyatı bekleniyor.",
        "sentiment": "negative",
        "threat_relevance": 0.99,
        "person_ids": [mehmet_id, kareem_id, ahmet_id],
        "entity_ids": [entities["kilis_kapisi"].id if entities["kilis_kapisi"] else None],
    },
]

inserted_news = []
for nd in news_data:
    title = nd["title"]
    existing = db.query(News).filter(News.title == title).first()
    if existing:
        print(f"  (zaten var) {title[:50]}...")
        inserted_news.append(existing)
        continue

    pub_date = datetime.now(timezone.utc) - timedelta(days=nd["days_ago"])
    n = News(
        title=nd["title"],
        content=nd["content"],
        summary=nd.get("summary", ""),
        source=nd["source"],
        category=nd["category"],
        sentiment=nd.get("sentiment", "neutral"),
        location_city=nd["location_city"],
        location_country=nd["location_country"],
        geom=pt(nd["lng"], nd["lat"]),
        published_at=pub_date,
        collected_at=pub_date,
        is_processed=True,
        is_breaking=nd.get("is_breaking", False),
        priority_score=nd.get("priority", 7.0),
        threat_relevance=nd.get("threat_relevance", 0.5),
        is_turkey_relevant=True,
        relevance_score=nd.get("threat_relevance", 0.5),
    )
    db.add(n)
    db.flush()

    # Kişi bağlantıları
    for pid_val in nd.get("person_ids", []):
        if pid_val:
            try:
                db.execute(news_person.insert().values(news_id=n.id, person_id=pid_val))
            except Exception:
                pass  # already linked

    # Varlık bağlantıları
    for eid_val in nd.get("entity_ids", []):
        if eid_val:
            try:
                db.execute(news_entity.insert().values(news_id=n.id, entity_id=eid_val))
            except Exception:
                pass

    inserted_news.append(n)
    print(f"  + Haber: {title[:60]}...")

db.commit()
print(f"  Toplam {len(inserted_news)} haber kontrol edildi.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. KİŞİ HAREKETLERİ (PersonLocation)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n--- Kişi Hareketleri Ekleniyor ---")

movements = [
    # Kareem Al-Nasir: Azez → Kilis → Gaziantep güzergahı
    (kareem_id, 36.990, 36.580, "SY", "Azez", "event", 20),
    (kareem_id, 37.033, 36.668, "TR", "Kilis", "event", 18),
    (kareem_id, 37.115, 36.715, "TR", "Kilis", "event", 17),
    (kareem_id, 37.033, 36.668, "TR", "Kilis", "event", 15),
    (kareem_id, 37.383, 37.066, "TR", "Gaziantep", "event", 14),
    (kareem_id, 37.383, 37.066, "TR", "Gaziantep", "event", 13),
    (kareem_id, 37.033, 36.668, "TR", "Kilis", "event", 11),
    (kareem_id, 36.990, 36.580, "SY", "Azez", "event", 9),

    # Nadia Mansour: Beirut → Istanbul → Gaziantep
    (nadia_id, 35.490, 33.890, "LB", "Beirut", "event", 25),
    (nadia_id, 28.980, 41.010, "TR", "Istanbul", "event", 18),
    (nadia_id, 28.975, 41.014, "TR", "Istanbul", "event", 17),
    (nadia_id, 28.968, 41.011, "TR", "Istanbul", "statement", 16),
    (nadia_id, 37.383, 37.066, "TR", "Gaziantep", "event", 14),
    (nadia_id, 37.380, 37.062, "TR", "Gaziantep", "event", 13),
    (nadia_id, 28.980, 41.010, "TR", "Istanbul", "event", 10),
    (nadia_id, 35.490, 33.890, "LB", "Beirut", "event", 8),

    # Elif Demir: Artık Ankara'ya yönelmiş (kaçmaya mı çalışıyor?)
    (elif_id, 28.968, 41.011, "TR", "Istanbul", "event", 12),
    (elif_id, 28.972, 41.008, "TR", "Istanbul", "event", 11),
    (elif_id, 32.854, 39.920, "TR", "Ankara", "event", 9),
    (elif_id, 32.858, 39.916, "TR", "Ankara", "event", 8),
    (elif_id, 32.854, 39.920, "TR", "Ankara", "statement", 7),
    (elif_id, 28.968, 41.011, "TR", "Istanbul", "event", 3),

    # Mehmet Karaca: Operasyonlardan sonra Gaziantep → Şanlıurfa
    (mehmet_id, 37.383, 37.066, "TR", "Gaziantep", "event", 14),
    (mehmet_id, 37.383, 37.066, "TR", "Gaziantep", "event", 12),
    (mehmet_id, 38.791, 37.158, "TR", "Kahramanmaraş", "event", 10),
    (mehmet_id, 38.796, 37.580, "TR", "Şanlıurfa", "event", 8),
    (mehmet_id, 38.791, 37.158, "TR", "Kahramanmaraş", "event", 6),

    # Ahmet Yilmaz: Adana → gözaltı sonrası salıverildi → Mersin
    (ahmet_id, 35.321, 37.002, "TR", "Adana", "event", 10),
    (ahmet_id, 35.321, 37.002, "TR", "Adana", "event", 8),
    (ahmet_id, 34.633, 36.801, "TR", "Mersin", "event", 5),
    (ahmet_id, 34.633, 36.801, "TR", "Mersin", "event", 4),
    (ahmet_id, 34.628, 36.805, "TR", "Mersin", "event", 3),

    # Hassan Omar: Azez-Kilis kurye rotası
    (hassan_id, 36.993, 36.583, "SY", "Azez", "event", 22),
    (hassan_id, 37.033, 36.668, "TR", "Kilis", "event", 20),
    (hassan_id, 37.115, 36.715, "TR", "Kilis", "event", 19),
    (hassan_id, 37.033, 36.668, "TR", "Kilis", "event", 16),
    (hassan_id, 36.993, 36.583, "SY", "Azez", "event", 14),
    (hassan_id, 36.166, 36.402, "TR", "Hatay", "event", 12),
    (hassan_id, 36.170, 36.398, "TR", "Hatay", "event", 11),
]

added_movements = 0
for (pid_v, lng, lat, country, city, loc_type, days_ago) in movements:
    if not pid_v:
        continue
    ts = datetime.now(timezone.utc) - timedelta(days=days_ago)
    # Check duplicate
    existing = db.query(PersonLocation).filter(
        PersonLocation.person_id == pid_v,
        PersonLocation.city == city,
        PersonLocation.timestamp == ts,
    ).first()
    if existing:
        continue

    pl = PersonLocation(
        person_id=pid_v,
        geom=pt(lng, lat),
        country=country,
        city=city,
        location_type=loc_type,
        timestamp=ts,
    )
    db.add(pl)
    added_movements += 1

db.commit()
print(f"  + {added_movements} kişi hareketi eklendi.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. GÖRÜŞMELER (PersonMeeting)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n--- Görüşmeler Ekleniyor ---")

meetings = [
    # Kareem-Hassan: Azez'de tedarik koordinasyonu
    (kareem_id, hassan_id, 36.990, 36.580, "SY", "Azez",
     "operational", "Silah sevkiyatı koordinasyonu", 19),
    # Kareem-Mehmet: Kilis'te teslim
    (kareem_id, mehmet_id, 37.033, 36.668, "TR", "Kilis",
     "handover", "Kilis sınırında mal teslimi görüşmesi", 15),
    # Kareem-Ahmet: Gaziantep depo koordinasyonu
    (kareem_id, ahmet_id, 37.383, 37.066, "TR", "Gaziantep",
     "operational", "Gaziantep depo yerleşimi ve rota planlaması", 13),
    # Nadia-Fatima: İstanbul finans buluşması
    (nadia_id, fatima_id, 28.975, 41.014, "TR", "Istanbul",
     "financial", "Hawala transfer koordinasyonu — Beirut-Istanbul-Gaziantep", 17),
    # Nadia-Elif: İstanbul finans
    (nadia_id, elif_id, 28.968, 41.011, "TR", "Istanbul",
     "financial", "Para aklama koordinasyonu", 16),
    # Nadia-Gaziantep kuyumculuk görüşmesi
    (nadia_id, elif_id, 37.383, 37.066, "TR", "Gaziantep",
     "financial", "Kuyumcu aracılığıyla transfer mekanizması kuruldu", 13),
    # Mehmet-Karaca yeni örgütlenme
    (mehmet_id, kareem_id, 38.791, 37.158, "TR", "Kahramanmaraş",
     "strategic", "Operasyon sonrası yeniden yapılanma görüşmesi", 9),
    # Ahmet-Mersin liman kontağı
    (ahmet_id, hasan_id, 34.633, 36.801, "TR", "Mersin",
     "operational", "Mersin Limanı üzerinden alternatif rota planlaması", 4),
    # Kareem-Hassan yeni güzergah
    (kareem_id, hassan_id, 36.993, 36.583, "SY", "Azez",
     "planning", "Yeni tünel güzergahı aktivasyonu — HUMINT uyarısı", 8),
]

added_meetings = 0
for (pa, pb, lng, lat, country, city, mtype, ctx, days_ago) in meetings:
    if not pa or not pb:
        continue
    mdate = datetime.now(timezone.utc) - timedelta(days=days_ago)
    m = PersonMeeting(
        person_a_id=pa,
        person_b_id=pb,
        geom=pt(lng, lat),
        location_country=country,
        location_city=city,
        meeting_type=mtype,
        context=ctx,
        meeting_date=mdate,
    )
    db.add(m)
    added_meetings += 1

db.commit()
print(f"  + {added_meetings} görüşme eklendi.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. TEHDİT DEĞERLENDİRMELERİ (ThreatAssessment)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n--- Tehdit Değerlendirmeleri Ekleniyor ---")

threats = [
    {
        "title": "Kilis-Öncüpınar sınır hattı — Aktif silah kaçakçılığı tehdidi",
        "description": (
            "'Kara Hat' ağının HUMINT istihbaratına göre önümüzdeki 10 gün içinde "
            "Kilis sınırından yeni bir silah sevkiyatı planladığı değerlendirilmektedir. "
            "Kareem Al-Nasir liderliğindeki Suriyeli tedarik ağı organize etmektedir. "
            "Azez-Kilis tünel güzergahı aktif durumdadır."
        ),
        "threat_level": "critical",
        "threat_category": "arms_smuggling",
        "probability": 0.85,
        "impact": 9.0,
        "risk_score": 7.65,
        "radius_km": 15.0,
        "lng": 37.033, "lat": 36.668,
        "assessed_by": "GEOINT-AUTO",
        "source_news_ids": [],
        "evidence_summary": "HUMINT + kişi hareketi verileri + önceki operasyon örüntüsü",
    },
    {
        "title": "Ceyhan BTC Terminali — Drone keşif tehdidi",
        "description": (
            "BTC Terminali yakınında tespit edilen bilinmeyen drone, stratejik enerji "
            "altyapısına yönelik olası bir keşif operasyonuna işaret etmektedir. "
            "Terminalin sabotaj risk skoru artırılmıştır. Benzer drone aktivitesi "
            "son 30 günde 2 kez raporlanmıştır."
        ),
        "threat_level": "high",
        "threat_category": "infrastructure_threat",
        "probability": 0.65,
        "impact": 9.5,
        "risk_score": 6.18,
        "radius_km": 10.0,
        "lng": 35.813, "lat": 36.836,
        "assessed_by": "GEOINT-AUTO",
        "source_news_ids": [],
        "evidence_summary": "Drone tespiti + önceki güvenlik raporları",
    },
    {
        "title": "Gaziantep — Yeniden örgütlenen kaçakçılık ağı tehdidi",
        "description": (
            "Son operasyonlara rağmen 'Kara Hat' örgütünün Gaziantep merkezli "
            "faaliyetlerini yeniden organize ettiği değerlendirilmektedir. "
            "Mehmet Karaca'nın Kahramanmaraş ve Şanlıurfa'ya çekilerek operasyonları "
            "uzaktan yönettiğine dair istihbarat mevcuttur."
        ),
        "threat_level": "high",
        "threat_category": "organized_crime",
        "probability": 0.80,
        "impact": 7.5,
        "risk_score": 6.0,
        "radius_km": 25.0,
        "lng": 37.383, "lat": 37.066,
        "assessed_by": "GEOINT-AUTO",
        "source_news_ids": [],
        "evidence_summary": "Kişi hareketleri + görüşme kayıtları + haber analizi",
    },
    {
        "title": "İstanbul hawala ağı — Finansal suç tehdidi",
        "description": (
            "Suriye-Lübnan bağlantılı hawala ağının İstanbul kuyumculuk sektörü "
            "üzerinden faaliyet gösterdiğine dair MASAK bulgularına dayanılarak "
            "hazırlanan tehdit değerlendirmesi. Nadia Mansour ve Elif Demir bağlantıları "
            "aktif soruşturma altında."
        ),
        "threat_level": "high",
        "threat_category": "financial_crime",
        "probability": 0.90,
        "impact": 6.5,
        "risk_score": 5.85,
        "radius_km": 5.0,
        "lng": 28.975, "lat": 41.010,
        "assessed_by": "GEOINT-AUTO",
        "source_news_ids": [],
        "evidence_summary": "MASAK operasyonu + INTERPOL verisi + kişi hareketleri",
    },
    {
        "title": "Azez bölgesi — Silahlı çatışma yayılma riski",
        "description": (
            "Azez'deki silahlı grup çatışmasının Türkiye sınırına sıçrama riski "
            "orta-yüksek olarak değerlendirilmektedir. Türkiye destekli güçlerin "
            "bölgeye sevki çatışmanın tırmanmasını şimdilik önlemiştir. "
            "Kaçakçılık güzergahı rekabetinin çatışmayı beslemesi beklenmektedir."
        ),
        "threat_level": "high",
        "threat_category": "armed_conflict",
        "probability": 0.55,
        "impact": 8.5,
        "risk_score": 4.68,
        "radius_km": 30.0,
        "lng": 36.990, "lat": 36.580,
        "assessed_by": "GEOINT-AUTO",
        "source_news_ids": [],
        "evidence_summary": "Çatışma raporu + ACLED verisi + sınır istihbaratı",
    },
    {
        "title": "Mersin Limanı — Kaçak yük transferi tehdidi",
        "description": (
            "Mersin Limanı'nda ele geçirilen silah parçaları ve kaçak elektronik, "
            "Kara Hat ağının alternatif deniz güzergahını test ettiğine işaret etmektedir. "
            "Ahmet Yilmaz'ın Mersin'e geçişi bu bağlamda değerlendirilmektedir."
        ),
        "threat_level": "medium",
        "threat_category": "arms_smuggling",
        "probability": 0.60,
        "impact": 7.0,
        "risk_score": 4.2,
        "radius_km": 5.0,
        "lng": 34.633, "lat": 36.801,
        "assessed_by": "GEOINT-AUTO",
        "source_news_ids": [],
        "evidence_summary": "Liman denetimi + kişi hareketi",
    },
    {
        "title": "Hatay-Suriye sınır hattı — Uyuşturucu ve silah geçiş riski",
        "description": (
            "Cilvegözü sınır kapısında ele geçirilen uyuşturucu ve silahlar, "
            "Hatay hattının aktif bir kaçakçılık güzergahı olarak kullanıldığını "
            "doğrulamaktadır. Hassan Omar'ın bu bölgedeki hareketleri takip altında."
        ),
        "threat_level": "medium",
        "threat_category": "narcotics_smuggling",
        "probability": 0.70,
        "impact": 6.0,
        "risk_score": 4.2,
        "radius_km": 20.0,
        "lng": 36.166, "lat": 36.402,
        "assessed_by": "GEOINT-AUTO",
        "source_news_ids": [],
        "evidence_summary": "Operasyon bulgusu + kişi hareketi kayıtları",
    },
]

added_threats = 0
for td in threats:
    existing = db.query(ThreatAssessment).filter(ThreatAssessment.title == td["title"]).first()
    if existing:
        print(f"  (zaten var) {td['title'][:50]}...")
        continue

    t = ThreatAssessment(
        title=td["title"],
        description=td["description"],
        threat_level=td["threat_level"],
        threat_category=td["threat_category"],
        probability=td["probability"],
        impact=td["impact"],
        risk_score=td["risk_score"],
        radius_km=td["radius_km"],
        geom=pt(td["lng"], td["lat"]),
        assessment_type="area_threat",
        is_active=True,
        assessed_by=td["assessed_by"],
        evidence_summary=td["evidence_summary"],
        assessed_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(days=14),
    )
    db.add(t)
    added_threats += 1
    print(f"  + Tehdit: {td['title'][:55]}...")

db.commit()
print(f"  + {added_threats} tehdit değerlendirmesi eklendi.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ÖZET
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n" + "=" * 60)
print("SEED DATA TAMAMLANDI — Veritabanı Özeti")
print("=" * 60)

from db.models import News, Person, Entity, ThreatAssessment, PersonLocation, PersonMeeting
print(f"Haberler       : {db.query(News).count()}")
print(f"Kişiler        : {db.query(Person).count()}")
print(f"Varlıklar      : {db.query(Entity).count()}")
print(f"Tehditler      : {db.query(ThreatAssessment).count()}")
print(f"Kişi Lok.      : {db.query(PersonLocation).count()}")
print(f"Görüşmeler     : {db.query(PersonMeeting).count()}")

db.close()
print("\n✅ Seed data başarıyla yüklendi.")
print("Artık region report ve chatbot testleri yapılabilir.")
