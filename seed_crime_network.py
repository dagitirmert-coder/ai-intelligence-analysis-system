"""
Seed script: Kara Hat suç örgütü — Kapsamlı test verisi

Generates:
- 14 interconnected persons (crime network hierarchy)
- 2 additional external actors (Boğa rival + Selim Arslan)
- Person relationships (alliance, subordinate, rivalry, communication)
- 40+ meetings with locations and dates
- 60+ person location entries (movement history)
- 30+ surveillance records
- 50+ link entities (phones, bank accounts, vehicles, emails)
- 40+ link connections (calls, transfers, meetings, co-locations)
- Pattern of life data for key figures
- Profile analyses for key figures
- Reconstructed timelines for 3 key persons
- 15+ news articles connected to persons
- Organizations connected to news

Usage:
    python seed_crime_network.py
"""
import os
import sys
import random
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.engine import SessionLocal, init_db
from db.models import (
    Person, PersonAlias, PersonRelationship, PersonMeeting,
    PersonLocation, PersonProfileAnalysis, PatternOfLife,
    SurveillanceRecord, LinkEntity, LinkConnection,
    ReconstructedTimeline, News, Organization,
    news_person, news_org,
)
from db.compat import make_point

NOW = datetime.now(timezone.utc)
D = lambda days: NOW - timedelta(days=days)
DF = lambda days: NOW + timedelta(days=days)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. PERSONS — KARA HAT ORGANİZASYON YAPISI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PERSONS = [
    # Çekirdek kadro
    {
        "name": "Mehmet Karaca",
        "name_normalized": "mehmet karaca",
        "role": "Kara Hat örgüt lideri / Operasyonel koordinatör",
        "nationality": "TR",
        "profile_notes": "Kara Hat silah kaçakçılığı örgütünün operasyonel lideri. Anti-takip yetenekli, temkinli, merkezi otorite.",
        "is_turkey_related": True,
        "last_known_country": "Turkey", "last_known_city": "Gaziantep",
        "lat": 37.0662, "lng": 37.3833,
        "mention_count": 35,
    },
    {
        "name": "Ibrahim Yildirim",
        "name_normalized": "ibrahim yildirim",
        "role": "Kara Hat patronu / İş adamı / Hami",
        "nationality": "TR",
        "profile_notes": "Adana'nın tanınmış iş adamı. Yıldırım Holding sahibi. Kara Hat örgütünün finansal hamisi ve gizli patronu. Mehmet Karaca'nın amcasının oğlu.",
        "is_turkey_related": True,
        "last_known_country": "Turkey", "last_known_city": "Adana",
        "lat": 37.0017, "lng": 35.3213,
        "mention_count": 12,
    },
    {
        "name": "Elif Demir",
        "name_normalized": "elif demir",
        "role": "Finans sorumlusu / Para aklama koordinatörü",
        "nationality": "TR",
        "profile_notes": "Kod adı: Kelebek. Eski banka çalışanı. Kapalıçarşı'da kuyumculuk dükkanı ile para aklama. 3 paravan şirket yöneticisi.",
        "is_turkey_related": True,
        "last_known_country": "Turkey", "last_known_city": "Istanbul",
        "lat": 41.0107, "lng": 28.9680,
        "mention_count": 22,
    },
    {
        "name": "Ahmet Yilmaz",
        "name_normalized": "ahmet yilmaz",
        "role": "Silah hattı operasyon şefi / Sınır geçiş yöneticisi",
        "nationality": "TR",
        "profile_notes": "Kod adı: Kartal. Silah kaçakçılığı hattının saha komutanı. IMEI değiştirmiyor (kritik zafiyet). İstanbul-Ankara-Gaziantep-Kilis rotasında aktif.",
        "is_turkey_related": True,
        "last_known_country": "Turkey", "last_known_city": "Gaziantep",
        "lat": 37.0662, "lng": 37.3833,
        "mention_count": 28,
    },
    {
        "name": "Hasan Kaya",
        "name_normalized": "hasan kaya",
        "role": "Lojistik koordinatör / Araç ve rota yöneticisi",
        "nationality": "TR",
        "profile_notes": "Örgütün en disiplinli operasyonel üyesi. Kadıköy'de ikamet, operasyonlarda Gaziantep'te. Araç modifikasyonu ve konvoy yönetimi uzmanı.",
        "is_turkey_related": True,
        "last_known_country": "Turkey", "last_known_city": "Gaziantep",
        "lat": 37.0662, "lng": 37.3833,
        "mention_count": 18,
    },
    {
        "name": "Tarık Ozkan",
        "name_normalized": "tarık ozkan",
        "role": "Muhasebeci / Sahte belge koordinatörü",
        "nationality": "TR",
        "profile_notes": "Kod adı: Muhasebeci. SMMM ruhsatlı. 4 paravan şirket kurmuş. Sahte gümrük beyannameleri, kimlikler ve faturalar düzenliyor. Ankara güvenli evi yöneticisi.",
        "is_turkey_related": True,
        "last_known_country": "Turkey", "last_known_city": "Istanbul",
        "lat": 41.0082, "lng": 28.9784,
        "mention_count": 14,
    },
    {
        "name": "Omar Hassan",
        "name_normalized": "omar hassan",
        "role": "Hawala operatörü / Gaziantep finans bağlantısı",
        "nationality": "SY",
        "profile_notes": "Suriye uyruklu, geçici koruma statüsünde. Gaziantep'te hawala ağı işletiyor. Volkov-Demir arasındaki para transferini yönetiyor. Her iki ağa da (Kara Hat + Boğa) hizmet veriyor.",
        "is_turkey_related": True,
        "last_known_country": "Turkey", "last_known_city": "Gaziantep",
        "lat": 37.0662, "lng": 37.3833,
        "mention_count": 16,
    },
    {
        "name": "Mustafa Al-Rashid",
        "name_normalized": "mustafa al-rashid",
        "role": "Sınır geçiş koordinatörü / Eski ÖSO savaşçı",
        "nationality": "SY",
        "profile_notes": "Kod adı: Şahin. Azez merkezli. Türkiye-Suriye sınır geçişlerini koordine ediyor. 8 kişilik sınır timi yönetiyor. 3 farklı geçiş noktası kullanıyor.",
        "is_turkey_related": False,
        "last_known_country": "Syria", "last_known_city": "Azez",
        "lat": 36.5864, "lng": 37.0478,
        "mention_count": 10,
    },
    {
        "name": "Yusuf Al-Rashid",
        "name_normalized": "yusuf al-rashid",
        "role": "Nakliye şirketi sahibi / Kamyon filosu yöneticisi",
        "nationality": "SY",
        "profile_notes": "Mustafa Al-Rashid'in küçük kardeşi. Gaziantep'te Al-Rashid Nakliyat şirketi. 4 kamyonlu filo. Meşru nakliye + Kara Hat sevkiyatları.",
        "is_turkey_related": True,
        "last_known_country": "Turkey", "last_known_city": "Gaziantep",
        "lat": 37.0662, "lng": 37.3833,
        "mention_count": 8,
    },
    {
        "name": "Dimitri Volkov",
        "name_normalized": "dimitri volkov",
        "role": "Uluslararası silah tedarikçisi",
        "nationality": "BG",
        "profile_notes": "Varna, Bulgaristan merkezli. Eski Sovyet silah depolarından tedarik. Ukrayna-Moldova-Romanya-Bulgaristan transit hattı. Bitcoin + hawala ile ödeme alıyor.",
        "is_turkey_related": False,
        "last_known_country": "Bulgaria", "last_known_city": "Varna",
        "lat": 43.2141, "lng": 27.9147,
        "mention_count": 15,
    },
    {
        "name": "Zeynep Aktas",
        "name_normalized": "zeynep aktas",
        "role": "Altyapı istihbaratçısı / Eski devlet memuru",
        "nationality": "TR",
        "profile_notes": "Kod adı: Zeynep Teyze. Emekli Adana Valiliği harita mühendisi. Kritik altyapı bilgilerine erişimi var: BTC terminali, enerji hatları, İncirlik çevresi.",
        "is_turkey_related": True,
        "last_known_country": "Turkey", "last_known_city": "Adana",
        "lat": 37.0017, "lng": 35.3213,
        "mention_count": 6,
    },
    {
        "name": "Emre Celik",
        "name_normalized": "emre celik",
        "role": "Teknoloji sorumlusu / Siber güvenlik uzmanı",
        "nationality": "TR",
        "profile_notes": "Ibrahim Yildirim'in yeğeni. ODTÜ bilgisayar mühendisi. CyberShield Bilişim sahibi. Örgüte şifreli iletişim, kripto para ve anti-takip teknolojisi sağlıyor.",
        "is_turkey_related": True,
        "last_known_country": "Turkey", "last_known_city": "Adana",
        "lat": 37.0500, "lng": 35.3933,
        "mention_count": 5,
    },
    # Dış aktörler
    {
        "name": "Selim Arslan",
        "name_normalized": "selim arslan",
        "role": "Eski Kara Hat üyesi / Muhtemel çift ajan",
        "nationality": "TR",
        "profile_notes": "Kod adı: Kurt. 2024'te Karaca ile ayrılmış, Boğa ağına geçmiş. Emniyet muhbiri olma ihtimali var. Elif Demir ile gizli temas sürdürüyor.",
        "is_turkey_related": True,
        "last_known_country": "Turkey", "last_known_city": "Istanbul",
        "lat": 41.0339, "lng": 28.9772,
        "mention_count": 7,
    },
    {
        "name": "Ferhat Gunes",
        "name_normalized": "ferhat gunes",
        "role": "Boğa ağı lideri / Rakip kaçakçılık örgütü",
        "nationality": "TR",
        "profile_notes": "Kod adı: Boğa. Gaziantep merkezli rakip ağ. İnsan kaçakçılığı + uyuşturucu. Kara Hat ile bölgesel rekabet içinde.",
        "is_turkey_related": True,
        "last_known_country": "Turkey", "last_known_city": "Gaziantep",
        "lat": 37.0735, "lng": 37.3829,
        "mention_count": 4,
    },
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. ALIASES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ALIASES = {
    "mehmet karaca": [
        ("Lider", "codename"),
        ("Abu Karaca", "aka"),
    ],
    "elif demir": [
        ("Kelebek", "codename"),
        ("Güneş Hanım", "aka"),
    ],
    "ahmet yilmaz": [
        ("Kartal", "codename"),
        ("Mehmet Demir", "aka"),
        ("Abu Tarek", "aka"),
    ],
    "mustafa al-rashid": [
        ("Şahin", "codename"),
        ("Abu Mustafa", "aka"),
    ],
    "ibrahim yildirim": [
        ("Reis", "codename"),
    ],
    "emre celik": [
        ("Genç", "codename"),
    ],
    "zeynep aktas": [
        ("Zeynep Teyze", "codename"),
    ],
    "tarık ozkan": [
        ("Muhasebeci", "codename"),
    ],
    "selim arslan": [
        ("Kurt", "codename"),
    ],
    "ferhat gunes": [
        ("Boğa", "codename"),
    ],
    "omar hassan": [
        ("Sarraf", "codename"),
    ],
    "hasan kaya": [
        ("Nakliyeci", "codename"),
    ],
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. RELATIONSHIPS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RELATIONSHIPS = [
    # (person_a, person_b, type, sentiment, strength, summary)
    ("ibrahim yildirim", "mehmet karaca", "subordinate", "positive", 0.95, "Patron-operasyonel lider ilişkisi. Akraba (amca oğlu)."),
    ("mehmet karaca", "ahmet yilmaz", "subordinate", "positive", 0.85, "Karaca silah hattını Yilmaz'a emanet etmiş."),
    ("mehmet karaca", "elif demir", "subordinate", "positive", 0.90, "Karaca finans operasyonunu Demir'e devretmiş."),
    ("mehmet karaca", "hasan kaya", "subordinate", "positive", 0.80, "Kaya lojistik koordinasyonu yürütüyor."),
    ("mehmet karaca", "zeynep aktas", "subordinate", "neutral", 0.60, "Aktaş danışman rolünde, para karşılığı altyapı bilgisi."),
    ("mehmet karaca", "omar hassan", "alliance", "neutral", 0.70, "Ticari ilişki — hawala hizmetleri."),
    ("elif demir", "tarık ozkan", "alliance", "positive", 0.85, "İş ortağı — muhasebe ve paravan şirket yönetimi."),
    ("elif demir", "omar hassan", "communication", "neutral", 0.75, "Doğrudan finans teması — altın/para teslimi."),
    ("ahmet yilmaz", "hasan kaya", "alliance", "positive", 0.80, "Saha operasyonlarında birlikte çalışıyorlar."),
    ("ahmet yilmaz", "mustafa al-rashid", "alliance", "positive", 0.75, "Sınır operasyonlarında birlikte çalışıyorlar."),
    ("mustafa al-rashid", "yusuf al-rashid", "alliance", "positive", 0.95, "Kardeşler — nakliye + sınır geçiş."),
    ("hasan kaya", "yusuf al-rashid", "alliance", "positive", 0.70, "Araç ve depo paylaşımı."),
    ("dimitri volkov", "omar hassan", "communication", "neutral", 0.65, "Hawala üzerinden ödeme alıyor."),
    ("dimitri volkov", "elif demir", "communication", "neutral", 0.50, "Dolaylı iletişim — e-posta."),
    ("ibrahim yildirim", "emre celik", "subordinate", "positive", 0.80, "Dayı-yeğen ilişkisi + teknoloji desteği."),
    ("emre celik", "mehmet karaca", "communication", "neutral", 0.55, "Şifreli iletişim sistemi kurulumu."),
    ("selim arslan", "mehmet karaca", "rivalry", "negative", 0.85, "Eski ortak, ihanet şüphesi."),
    ("selim arslan", "elif demir", "communication", "neutral", 0.30, "Gizli temas — niyeti belirsiz."),
    ("selim arslan", "ferhat gunes", "alliance", "positive", 0.65, "Boğa ağına katılım."),
    ("ferhat gunes", "mehmet karaca", "rivalry", "negative", 0.90, "Gaziantep bölgesel rekabet."),
    ("omar hassan", "ferhat gunes", "communication", "neutral", 0.40, "Her iki ağa da hawala hizmeti."),
    ("mehmet karaca", "dimitri volkov", "alliance", "neutral", 0.70, "Silah tedarik zinciri. Volkov ana tedarikçi."),
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. MEETINGS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MEETINGS = [
    # (person_a, person_b, date_offset_days_ago, lat, lng, country, city, type, context)
    ("mehmet karaca", "mustafa al-rashid", 47, 37.0662, 37.3833, "Turkey", "Gaziantep", "coordination", "Şubat 18 — Şahinbey deposunda lojistik hat yeniden kurulumu toplantısı"),
    ("mehmet karaca", "yusuf al-rashid", 40, 36.7184, 37.1212, "Turkey", "Kilis", "coordination", "Şubat 25 — Finansal yeniden yapılandırma görüşmesi"),
    ("mehmet karaca", "elif demir", 35, 37.0662, 37.3833, "Turkey", "Gaziantep", "planning", "Mart başı — Sanayi bölgesinde kısa temas"),
    ("elif demir", "omar hassan", 23, 37.0662, 37.3833, "Turkey", "Gaziantep", "financial", "Mart 14 — Grand Otel buluşması, 2 saat 15 dk, altın teslimi"),
    ("elif demir", "tarık ozkan", 20, 41.0107, 28.9680, "Turkey", "Istanbul", "business", "Mart 17 — Kapalıçarşı dükkanında evrak alışverişi"),
    ("elif demir", "omar hassan", 19, 37.0662, 37.3833, "Turkey", "Gaziantep", "financial", "Mart 18 — Grand Otel, Omar + bilinmeyen Suriyeli ile buluşma"),
    ("mehmet karaca", "elif demir", 17, 41.0107, 28.9680, "Turkey", "Istanbul", "strategic", "Mart 20 — Kapalıçarşı arka oda toplantısı, Tarık Özkan da mevcut"),
    ("mehmet karaca", "tarık ozkan", 17, 41.0107, 28.9680, "Turkey", "Istanbul", "strategic", "Mart 20 — Kapalıçarşı arka oda toplantısı"),
    ("ahmet yilmaz", "mustafa al-rashid", 16, 36.6512, 37.0134, "Turkey", "Kilis", "operational", "Mart 21 gece — 3 araçlık konvoy sınır geçişi"),
    ("ahmet yilmaz", "hasan kaya", 14, 37.0662, 37.3833, "Turkey", "Gaziantep", "planning", "Mart 23 — Çay bahçesinde 1 saat 40 dk buluşma"),
    # Adana büyük toplantı (26 Mart)
    ("mehmet karaca", "ahmet yilmaz", 11, 37.0017, 35.3213, "Turkey", "Adana", "summit", "Mart 26 — Çiftçi Lokantası, 7 kişilik koordinasyon toplantısı"),
    ("mehmet karaca", "hasan kaya", 11, 37.0017, 35.3213, "Turkey", "Adana", "summit", "Mart 26 — Adana koordinasyon toplantısı"),
    ("mehmet karaca", "zeynep aktas", 11, 37.0017, 35.3213, "Turkey", "Adana", "summit", "Mart 26 — Adana toplantısı, altyapı bilgi sunumu"),
    ("mehmet karaca", "yusuf al-rashid", 11, 37.0017, 35.3213, "Turkey", "Adana", "summit", "Mart 26 — Adana toplantısı"),
    ("mehmet karaca", "ibrahim yildirim", 11, 37.0017, 35.3213, "Turkey", "Adana", "summit", "Mart 26 — Adana toplantısı, Reis ilk kez katıldı"),
    ("mehmet karaca", "emre celik", 11, 37.0017, 35.3213, "Turkey", "Adana", "summit", "Mart 26 — Adana toplantısı, teknoloji brifingi"),
    # Mart sonu - Nisan hazırlıkları
    ("mehmet karaca", "tarık ozkan", 7, 39.9334, 32.8597, "Turkey", "Ankara", "logistic", "Mart 31 — Ankara güvenli evde buluşma"),
    ("hasan kaya", "yusuf al-rashid", 9, 37.0662, 37.3833, "Turkey", "Gaziantep", "preparation", "Mart 29 — Depoda araç modifikasyonu"),
    ("mehmet karaca", "hasan kaya", 6, 37.0662, 37.3833, "Turkey", "Gaziantep", "final_planning", "Mart 31 gece — Depoda 3 saatlik son planlama"),
    ("omar hassan", "elif demir", 9, 37.0662, 37.3833, "Turkey", "Gaziantep", "financial", "Mart 28 — $25.000 nakit teslim"),
    # Nisan operasyon hazırlığı
    ("mehmet karaca", "ahmet yilmaz", 4, 37.0662, 37.3833, "Turkey", "Gaziantep", "final_briefing", "Nisan 3 — Depoda son koordinasyon, 4 saat"),
    ("mehmet karaca", "hasan kaya", 4, 37.0662, 37.3833, "Turkey", "Gaziantep", "final_briefing", "Nisan 3 — Depoda son koordinasyon"),
    ("mehmet karaca", "omar hassan", 4, 37.0662, 37.3833, "Turkey", "Gaziantep", "final_briefing", "Nisan 3 — Son toplantı, finans onay"),
    # Elif Demir İstanbul/Mersin
    ("elif demir", "tarık ozkan", 14, 41.0107, 28.9680, "Turkey", "Istanbul", "business", "Mart 23 — Ofiste muhasebe çalışması"),
    ("selim arslan", "elif demir", 9, 41.0339, 28.9772, "Turkey", "Istanbul", "secret_contact", "Mart 28 — 30 saniyelik telefon + aynı baz istasyonu"),
    # Volkov bağlantıları
    ("dimitri volkov", "omar hassan", 30, 37.0662, 37.3833, "Turkey", "Gaziantep", "supply", "Şubat — Hawala üzerinden ödeme talimatı"),
    ("dimitri volkov", "mehmet karaca", 180, 41.0082, 28.9784, "Turkey", "Istanbul", "initial_meeting", "Ekim 2025 — Laleli Otel'de ilk tanışma, Omar Hassan tanıştırdı"),
    ("dimitri volkov", "mehmet karaca", 120, 37.0662, 37.3833, "Turkey", "Gaziantep", "supply_deal", "Aralık 2025 — Aylık düzenli tedarik anlaşması"),
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. PERSON LOCATIONS (movement history)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LOCATIONS = [
    # (person_normalized, days_ago, lat, lng, country, city, type)
    # Mehmet Karaca — rotalar
    ("mehmet karaca", 50, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    ("mehmet karaca", 47, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    ("mehmet karaca", 40, 36.7184, 37.1212, "Turkey", "Kilis", "event"),
    ("mehmet karaca", 35, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    ("mehmet karaca", 30, 37.0017, 35.3213, "Turkey", "Adana", "event"),
    ("mehmet karaca", 25, 37.0017, 35.3213, "Turkey", "Adana", "event"),
    ("mehmet karaca", 20, 36.8012, 34.6332, "Turkey", "Mersin", "event"),
    ("mehmet karaca", 17, 41.0107, 28.9680, "Turkey", "Istanbul", "event"),
    ("mehmet karaca", 14, 37.0017, 35.3213, "Turkey", "Adana", "event"),
    ("mehmet karaca", 11, 37.0017, 35.3213, "Turkey", "Adana", "event"),
    ("mehmet karaca", 7, 39.9334, 32.8597, "Turkey", "Ankara", "event"),
    ("mehmet karaca", 6, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    ("mehmet karaca", 4, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    ("mehmet karaca", 2, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    # Ahmet Yilmaz — İstanbul-Ankara-Gaziantep-Kilis rotası
    ("ahmet yilmaz", 50, 41.0082, 28.9784, "Turkey", "Istanbul", "event"),
    ("ahmet yilmaz", 40, 41.0082, 28.9784, "Turkey", "Istanbul", "event"),
    ("ahmet yilmaz", 30, 39.9334, 32.8597, "Turkey", "Ankara", "event"),
    ("ahmet yilmaz", 25, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    ("ahmet yilmaz", 20, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    ("ahmet yilmaz", 16, 36.6512, 37.0134, "Turkey", "Kilis", "event"),
    ("ahmet yilmaz", 14, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    ("ahmet yilmaz", 11, 37.0017, 35.3213, "Turkey", "Adana", "event"),
    ("ahmet yilmaz", 8, 41.0082, 28.9784, "Turkey", "Istanbul", "event"),
    ("ahmet yilmaz", 4, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    ("ahmet yilmaz", 2, 36.7184, 37.1212, "Turkey", "Kilis", "event"),
    # Elif Demir — İstanbul + Gaziantep + Mersin
    ("elif demir", 30, 41.0107, 28.9680, "Turkey", "Istanbul", "event"),
    ("elif demir", 23, 41.0107, 28.9680, "Turkey", "Istanbul", "event"),
    ("elif demir", 19, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    ("elif demir", 18, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    ("elif demir", 17, 41.0107, 28.9680, "Turkey", "Istanbul", "event"),
    ("elif demir", 16, 36.8012, 34.6332, "Turkey", "Mersin", "event"),
    ("elif demir", 12, 41.0107, 28.9680, "Turkey", "Istanbul", "event"),
    ("elif demir", 8, 36.8012, 34.6332, "Turkey", "Mersin", "event"),
    ("elif demir", 4, 41.0107, 28.9680, "Turkey", "Istanbul", "event"),
    # Hasan Kaya
    ("hasan kaya", 30, 41.0082, 28.9784, "Turkey", "Istanbul", "event"),
    ("hasan kaya", 20, 41.0082, 28.9784, "Turkey", "Istanbul", "event"),
    ("hasan kaya", 11, 37.0017, 35.3213, "Turkey", "Adana", "event"),
    ("hasan kaya", 10, 41.0082, 28.9784, "Turkey", "Istanbul", "event"),
    ("hasan kaya", 9, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    ("hasan kaya", 7, 37.0204, 37.0592, "Turkey", "Oğuzeli", "event"),
    ("hasan kaya", 6, 36.6512, 37.0134, "Turkey", "Kilis", "event"),
    ("hasan kaya", 4, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    # Omar Hassan — Gaziantep sabit
    ("omar hassan", 30, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    ("omar hassan", 23, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    ("omar hassan", 14, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    ("omar hassan", 4, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    # Ibrahim Yildirim — Adana sabit
    ("ibrahim yildirim", 30, 37.0017, 35.3213, "Turkey", "Adana", "event"),
    ("ibrahim yildirim", 11, 37.0017, 35.3213, "Turkey", "Adana", "event"),
    ("ibrahim yildirim", 5, 36.8346, 35.8002, "Turkey", "Ceyhan", "event"),
    # Dimitri Volkov — Varna + Istanbul ziyaretleri
    ("dimitri volkov", 180, 41.0082, 28.9784, "Turkey", "Istanbul", "event"),
    ("dimitri volkov", 150, 43.2141, 27.9147, "Bulgaria", "Varna", "event"),
    ("dimitri volkov", 120, 37.0662, 37.3833, "Turkey", "Gaziantep", "event"),
    ("dimitri volkov", 90, 43.2141, 27.9147, "Bulgaria", "Varna", "event"),
    ("dimitri volkov", 60, 43.2141, 27.9147, "Bulgaria", "Varna", "event"),
    ("dimitri volkov", 30, 43.2141, 27.9147, "Bulgaria", "Varna", "event"),
    # Zeynep Aktas — Adana sabit
    ("zeynep aktas", 30, 37.0017, 35.3213, "Turkey", "Adana", "event"),
    ("zeynep aktas", 11, 37.0017, 35.3213, "Turkey", "Adana", "event"),
    # Emre Celik
    ("emre celik", 20, 37.0500, 35.3933, "Turkey", "Adana", "event"),
    ("emre celik", 11, 37.0017, 35.3213, "Turkey", "Adana", "event"),
    # Tarık Ozkan — Istanbul + Ankara
    ("tarık ozkan", 22, 39.9334, 32.8597, "Turkey", "Ankara", "event"),
    ("tarık ozkan", 17, 41.0107, 28.9680, "Turkey", "Istanbul", "event"),
    ("tarık ozkan", 7, 39.9334, 32.8597, "Turkey", "Ankara", "event"),
    ("tarık ozkan", 4, 41.0107, 28.9680, "Turkey", "Istanbul", "event"),
    # Selim Arslan — Istanbul
    ("selim arslan", 15, 41.0339, 28.9772, "Turkey", "Istanbul", "event"),
    ("selim arslan", 9, 41.0339, 28.9772, "Turkey", "Istanbul", "event"),
    # Mustafa Al-Rashid — Suriye
    ("mustafa al-rashid", 30, 36.5864, 37.0478, "Syria", "Azez", "event"),
    ("mustafa al-rashid", 16, 36.6512, 37.0134, "Syria", "Öncüpınar", "event"),
    ("mustafa al-rashid", 2, 36.5864, 37.0478, "Syria", "Azez", "event"),
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. LINK ENTITIES (phones, vehicles, bank accounts, emails)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LINK_ENTITIES = [
    # (person_normalized, entity_type, value, label, is_suspicious, risk_score)
    # Phones
    ("mehmet karaca", "phone", "+90533XXXX01", "Karaca ana hat (değişken)", True, 0.9),
    ("mehmet karaca", "phone", "+90544XXXX02", "Karaca yedek hat", True, 0.8),
    ("ahmet yilmaz", "phone", "+90535XXXX03", "Yilmaz sabit hat (IMEI sabit!)", True, 0.95),
    ("elif demir", "phone", "+90542XXXX04", "Demir kişisel hat", False, 0.3),
    ("elif demir", "phone", "+90555XXXX05", "Demir örgüt hattı", True, 0.9),
    ("omar hassan", "phone", "+90546XXXX06", "Hassan Gaziantep hattı", True, 0.8),
    ("tarık ozkan", "phone", "+90532XXXX07", "Özkan iş hattı", False, 0.4),
    ("hasan kaya", "phone", "+90543XXXX08", "Kaya ana hat", True, 0.7),
    ("dimitri volkov", "phone", "+359XXXXXXX09", "Volkov Bulgaristan hattı", True, 0.9),
    ("emre celik", "phone", "+90538XXXX10", "Çelik kişisel", False, 0.3),
    ("ibrahim yildirim", "phone", "+90533XXXX11", "Yıldırım iş hattı", False, 0.2),
    ("selim arslan", "phone", "+90544XXXX12", "Arslan hattı", True, 0.6),
    ("mustafa al-rashid", "phone", "+963XXXXXXX13", "Al-Rashid Suriye hattı", True, 0.9),
    ("zeynep aktas", "phone", "+90537XXXX14", "Aktaş ev hattı", False, 0.3),
    # Vehicles
    ("mehmet karaca", "vehicle", "01 HK 7734", "Gri VW Passat", True, 0.8),
    ("elif demir", "vehicle", "34 AKR 2847", "Beyaz Mercedes Vito", True, 0.7),
    ("tarık ozkan", "vehicle", "06 MT 9921", "Siyah BMW 320i", True, 0.5),
    ("yusuf al-rashid", "vehicle", "27 AL 1453", "Gri Fiat Doblo (Al-Rashid Nakliyat)", True, 0.8),
    ("yusuf al-rashid", "vehicle", "27 KE 892", "Beyaz MAN TGA Kamyon", True, 0.9),
    ("ibrahim yildirim", "vehicle", "01 CZ 0001", "Siyah Mercedes S 400d", False, 0.2),
    ("hasan kaya", "vehicle", "34 HK 2190", "Beyaz Ford Transit Custom", True, 0.8),
    ("ferhat gunes", "vehicle", "27 FG 0027", "Siyah Range Rover Sport", True, 0.6),
    # Bank accounts
    ("elif demir", "bank_account", "Halkbank-Fatih-TR12XXX", "Güneş İnşaat hesabı", True, 0.9),
    ("elif demir", "bank_account", "Ziraat-Mersin-TR34XXX", "Yıldız Lojistik hesabı", True, 0.8),
    ("tarık ozkan", "bank_account", "Garanti-Eminönü-TR56XXX", "Atlas D.T. hesabı", True, 0.9),
    ("tarık ozkan", "bank_account", "İşBank-Adana-TR78XXX", "Anadolu Danışmanlık hesabı", True, 0.7),
    ("ibrahim yildirim", "bank_account", "Akbank-Adana-TR90XXX", "Yıldırım Holding hesabı", False, 0.3),
    ("dimitri volkov", "crypto_wallet", "bc1qxy2kgdygjr...volkov1", "BTC Cüzdan #1", True, 0.95),
    ("dimitri volkov", "crypto_wallet", "bc1qxy2kgdygjr...volkov2", "BTC Cüzdan #2", True, 0.95),
    ("dimitri volkov", "bank_account", "UniCredit-Varna-BG12XXX", "Volkov ticari hesap", True, 0.7),
    # Emails
    ("elif demir", "email", "kelebek34@gmail.com", "Demir kişisel e-posta", True, 0.8),
    ("emre celik", "email", "emre.celik98@gmail.com", "Çelik kişisel e-posta", True, 0.5),
    ("tarık ozkan", "email", "t.ozkan.smmm@gmail.com", "Özkan iş e-postası", False, 0.3),
    # Social media
    ("elif demir", "social_media", "@gunes_kuyumculuk", "Instagram dükkan hesabı", True, 0.6),
    ("yusuf al-rashid", "social_media", "@alrashid_transport", "Telegram nakliye hesabı", True, 0.7),
    ("emre celik", "social_media", "emrecelik98", "GitHub hesabı", True, 0.5),
    # Addresses
    ("mehmet karaca", "address", "Güneşli Residence D:7 Ankara", "Ankara güvenli evi", True, 0.95),
    ("elif demir", "address", "Fatih Çarşamba Mah. İstanbul", "İkamet adresi", False, 0.3),
    ("elif demir", "address", "Mersin Akdeniz Liman Yolu No:78", "Yıldız Lojistik deposu", True, 0.9),
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. LINK CONNECTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LINK_CONNECTIONS_DATA = [
    # (source_type, source_value, target_type, target_value, conn_type, direction, strength, frequency, is_suspicious, total_amount, currency, evidence)
    ("+90533XXXX01", "+90535XXXX03", "call", "bidirectional", 0.85, 45, True, None, None, "SIGINT — 45 arama kaydı, şifreli dil"),
    ("+90533XXXX01", "+963XXXXXXX13", "call", "outgoing", 0.70, 12, True, None, None, "SIGINT — Suriye hattı, operasyon koordinasyonu"),
    ("+90555XXXX05", "+90532XXXX07", "call", "bidirectional", 0.80, 60, True, None, None, "SIGINT — Günlük iletişim, evrak/muhasebe"),
    ("+90555XXXX05", "+90533XXXX01", "call", "bidirectional", 0.75, 30, True, None, None, "SIGINT — Haftada 2-3, şifreli dil"),
    ("+90546XXXX06", "+90555XXXX05", "call", "bidirectional", 0.70, 12, True, None, None, "SIGINT — Ayda 3-4, para teslim koordinasyonu"),
    ("+90546XXXX06", "+359XXXXXXX09", "call", "incoming", 0.65, 8, True, None, None, "SIGINT — Bulgar hattı, hawala kodu"),
    ("+90533XXXX01", "+90543XXXX08", "call", "outgoing", 0.75, 25, True, None, None, "SIGINT — Lojistik koordinasyon"),
    ("+90544XXXX12", "+90555XXXX05", "call", "outgoing", 0.30, 2, True, None, None, "SIGINT — Arslan-Demir gizli temas"),
    # Financial transfers
    ("Halkbank-Fatih-TR12XXX", "Garanti-Eminönü-TR56XXX", "transfer", "bidirectional", 0.85, 15, True, 1200000, "TRY", "FININT — Güneş İnşaat ↔ Atlas D.T. hayali fatura"),
    ("İşBank-Adana-TR78XXX", "+90537XXXX14", "transfer", "outgoing", 0.70, 4, True, 60000, "TRY", "FININT — Aylık 15K TL danışmanlık ücreti"),
    ("bc1qxy2kgdygjr...volkov1", "bc1qxy2kgdygjr...volkov2", "transfer", "outgoing", 0.90, 6, True, 750000, "USD", "CYBER — Bitcoin tumbler arası transfer"),
    ("UniCredit-Varna-BG12XXX", "Garanti-Eminönü-TR56XXX", "transfer", "outgoing", 0.60, 3, True, 150000, "EUR", "FININT — Global Trade Partners → Atlas D.T."),
    # Co-locations
    ("01 HK 7734", "34 AKR 2847", "co_location", "bidirectional", 0.80, 3, True, None, None, "SURV — Kapalıçarşı ve Gaziantep'te aynı anda"),
    ("34 HK 2190", "27 AL 1453", "co_location", "bidirectional", 0.85, 5, True, None, None, "SURV — Gaziantep deposunda sürekli birlikte"),
    ("01 HK 7734", "06 MT 9921", "co_location", "bidirectional", 0.65, 2, True, None, None, "SURV — Ankara'da aynı bina ziyareti"),
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8. SURVEILLANCE RECORDS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SURVEILLANCE = [
    # (person, source_type, source_name, days_ago, lat, lng, country, city, description, confidence)
    ("elif demir", "cctv", "Kapalıçarşı Nuruosmaniye girişi", 20, 41.0107, 28.9680, "Turkey", "Istanbul", "Hedef dükkan açılışı, 08:30. Tarık Özkan ziyareti 12:15.", 0.95),
    ("elif demir", "cctv", "Atatürk Havalimanı check-in", 19, 40.9769, 28.8147, "Turkey", "Istanbul", "Pegasus PC-411 Gaziantep uçuşu. 07:30 havalimanına varış.", 0.98),
    ("elif demir", "license_plate", "Mersin O-51 HGS", 16, 36.8012, 34.6332, "Turkey", "Mersin", "34 AKR 2847 Vito, Mersin giriş HGS kaydı.", 0.99),
    ("mehmet karaca", "cctv", "Kapalıçarşı Beyazıt girişi", 17, 41.0107, 28.9680, "Turkey", "Istanbul", "Karaca dükkanı ziyaret, anti-takip hareketleri gözlemlendi.", 0.85),
    ("mehmet karaca", "phone_intercept", "Hat dinleme #19", 29, 37.0662, 37.3833, "Turkey", "Gaziantep", "Suriye hattı arama: 'Malzeme hazırlandı, çay için hazırız.'", 0.95),
    ("mehmet karaca", "signal_tracking", "Baz istasyonu analizi", 18, 37.0017, 35.3213, "Turkey", "Adana", "IMEI son aktif baz: Adana Seyhan.", 0.90),
    ("mehmet karaca", "cctv", "Ankara Ulus, Anafartalar Cad.", 7, 39.9334, 32.8597, "Turkey", "Ankara", "Hukuk bürosuna giriş 15:15, çıkış 16:15.", 0.92),
    ("ahmet yilmaz", "signal_tracking", "IMEI takip (DEĞİŞMİYOR)", 16, 36.6512, 37.0134, "Turkey", "Kilis", "Aynı IMEI İstanbul→Ankara→Gaziantep→Kilis rotasında.", 0.99),
    ("ahmet yilmaz", "phone_intercept", "Hat dinleme #22", 24, 36.7184, 37.1212, "Turkey", "Kilis", "'Kartal burada, yol temiz. Şahin'le buluştum.'", 0.95),
    ("hasan kaya", "license_plate", "Gaziantep-Oğuzeli yol kamerası", 7, 37.0204, 37.0592, "Turkey", "Oğuzeli", "34 HK 2190 Ford Transit, Yıldırım İstasyon-3 önünde durdu.", 0.99),
    ("hasan kaya", "satellite", "Sentinel-2 + ticari uydu", 8, 37.0662, 37.3833, "Turkey", "Gaziantep", "Şahinbey Sanayi deposu çevresinde 4 araç tespit.", 0.80),
    ("hasan kaya", "drone", "Kilis sınır bölgesi", 6, 36.6512, 37.0134, "Turkey", "Kilis", "Toprak yolda araç keşif turu, GPS waypoint kaydı.", 0.90),
    ("omar hassan", "cctv", "Grand Otel Gaziantep lobisi", 23, 37.0662, 37.3833, "Turkey", "Gaziantep", "Elif Demir ile buluşma, 11:00-13:30.", 0.95),
    ("omar hassan", "financial", "MASAK ŞİB bildirimi", 60, 37.0662, 37.3833, "Turkey", "Gaziantep", "Şüpheli döviz alım işlemleri, döviz bürosu.", 0.80),
    ("tarık ozkan", "license_plate", "O-4 Ankara HGS", 22, 39.9334, 32.8597, "Turkey", "Ankara", "06 MT 9921 BMW, Ankara giriş HGS kaydı.", 0.99),
    ("tarık ozkan", "cctv", "Ankara İtfaiye Meydanı kahvaltıcı", 7, 39.9334, 32.8597, "Turkey", "Ankara", "Karaca ile kahvaltıda buluşma, 08:30.", 0.90),
    ("ibrahim yildirim", "cctv", "Adana Çiftçi Lokantası", 11, 37.0017, 35.3213, "Turkey", "Adana", "Lüks Mercedes ile geldi, toplantıya ilk gelen son ayrılan.", 0.85),
    ("ibrahim yildirim", "satellite", "Ceyhan Enerji ofisi", 5, 36.8346, 35.8002, "Turkey", "Ceyhan", "Ofiste yabancı iş adamı ile toplantı.", 0.70),
    ("elif demir", "satellite", "Mersin Yıldız Lojistik deposu", 12, 36.7937, 34.6159, "Turkey", "Mersin", "Depo çevresinde araç trafiği, yeni çit yapımı.", 0.80),
    ("elif demir", "cctv", "Mersin Yıldız Lojistik deposu", 9, 36.7937, 34.6159, "Turkey", "Mersin", "Al-Rashid Nakliyat kamyonu teslim, 08:00-12:00.", 0.90),
    ("emre celik", "social_media", "GitHub profil analizi", 15, 37.0500, 35.3933, "Turkey", "Adana", "secure-msg, rf-scanner, vpn-mesh projeleri. SDR tarama yeteneği.", 0.85),
    ("selim arslan", "cctv", "Eminönü, İstanbul", 6, 41.0172, 28.9693, "Turkey", "Istanbul", "Takım elbiseli şahısla 15 dk görüşme. Emniyet İstihbarat şüphesi.", 0.70),
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 9. NEWS ARTICLES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEWS_ARTICLES = [
    {
        "title": "Kilis sınır bölgesinde şüpheli araç hareketliliği tespit edildi",
        "content": "Güvenlik güçleri, Kilis Öncüpınar bölgesinde gece saatlerinde şüpheli araç hareketliliği tespit etti. Bölgede kaçakçılık faaliyetlerinin arttığı değerlendiriliyor.",
        "source": "Kilis Haber", "category": "conflict", "sentiment": "negative",
        "lat": 36.7184, "lng": 37.1212, "country": "Turkey", "city": "Kilis",
        "days_ago": 37, "is_turkey_relevant": True, "relevance_score": 0.8,
        "threat_relevance": 0.7, "persons": ["mehmet karaca", "ahmet yilmaz", "mustafa al-rashid"],
    },
    {
        "title": "Gaziantep'te kaçakçılık operasyonu: 2 şüpheli gözaltında",
        "content": "Gaziantep Emniyet Müdürlüğü, Şahinbey ilçesinde düzenlediği operasyonda 2 şüpheliyi gözaltına aldı. Şüphelilerin farklı bir kaçakçılık ağıyla bağlantılı olduğu açıklandı.",
        "source": "Gaziantep Haber", "category": "conflict", "sentiment": "negative",
        "lat": 37.0662, "lng": 37.3833, "country": "Turkey", "city": "Gaziantep",
        "days_ago": 32, "is_turkey_relevant": True, "relevance_score": 0.7,
        "threat_relevance": 0.6, "persons": ["ferhat gunes"],
    },
    {
        "title": "Kapalıçarşı'da altın fiyatlarında olağandışı hareketlilik",
        "content": "İstanbul Kapalıçarşı'da son haftalarda altın alım satım hacminde belirgin artış gözlemleniyor. Uzmanlar, gayri resmi altın ticaretindeki artışa dikkat çekiyor.",
        "source": "Ekonomi Gündem", "category": "economy", "sentiment": "neutral",
        "lat": 41.0107, "lng": 28.9680, "country": "Turkey", "city": "Istanbul",
        "days_ago": 25, "is_turkey_relevant": True, "relevance_score": 0.5,
        "threat_relevance": 0.4, "persons": ["elif demir", "tarık ozkan"],
    },
    {
        "title": "Mersin Limanı'nda gümrük denetimleri sıkılaştırıldı",
        "content": "Mersin Uluslararası Limanı'nda gümrük kontrollerinin artırıldığı bildirildi. Konteyner taramalarında yeni X-ray cihazları devreye alındı.",
        "source": "Mersin Haber", "category": "politics", "sentiment": "neutral",
        "lat": 36.8012, "lng": 34.6332, "country": "Turkey", "city": "Mersin",
        "days_ago": 18, "is_turkey_relevant": True, "relevance_score": 0.6,
        "threat_relevance": 0.5, "persons": ["elif demir"],
    },
    {
        "title": "Adana'da terör örgütüne yönelik baskın operasyonu",
        "content": "Adana Seyhan ilçesinde düzenlenen eş zamanlı operasyonda farklı bir terör örgütüne yönelik 5 gözaltı gerçekleşti. Bölgede güvenlik önlemleri artırıldı.",
        "source": "Adana Haber", "category": "conflict", "sentiment": "negative",
        "lat": 37.0017, "lng": 35.3213, "country": "Turkey", "city": "Adana",
        "days_ago": 14, "is_turkey_relevant": True, "relevance_score": 0.7,
        "threat_relevance": 0.6, "persons": [],
    },
    {
        "title": "Ceyhan BTC terminali güvenlik denetimi yapıldı",
        "content": "Bakü-Tiflis-Ceyhan boru hattının Ceyhan terminalinde yıllık güvenlik denetimi gerçekleştirildi. Tesis çevresindeki güvenlik önlemlerinin yeterli olduğu açıklandı.",
        "source": "Enerji Gündem", "category": "economy", "sentiment": "positive",
        "lat": 36.8346, "lng": 35.8002, "country": "Turkey", "city": "Ceyhan",
        "days_ago": 10, "is_turkey_relevant": True, "relevance_score": 0.8,
        "threat_relevance": 0.7, "persons": ["ibrahim yildirim", "zeynep aktas"],
    },
    {
        "title": "Bulgaristan'da silah kaçakçılığı operasyonu: Varna'da gözaltılar",
        "content": "Bulgaristan DANS, Varna'da uluslararası silah kaçakçılığı şebekesine yönelik operasyon düzenledi. Operasyonda Doğu Avrupa kökenli silahların Türkiye ve Suriye'ye transfer edildiği tespit edildi.",
        "source": "Balkan Insight", "category": "conflict", "sentiment": "negative",
        "lat": 43.2141, "lng": 27.9147, "country": "Bulgaria", "city": "Varna",
        "days_ago": 8, "is_turkey_relevant": True, "relevance_score": 0.9,
        "threat_relevance": 0.9, "persons": ["dimitri volkov"],
    },
    {
        "title": "Gaziantep sanayi bölgesinde şüpheli depo faaliyetleri",
        "content": "Şahinbey Sanayi Sitesi'nde bazı depoların gece saatlerinde aktif olduğu ve olağandışı araç trafiği gözlemlendiği bildirildi.",
        "source": "Gaziantep Gündem", "category": "conflict", "sentiment": "negative",
        "lat": 37.0662, "lng": 37.3833, "country": "Turkey", "city": "Gaziantep",
        "days_ago": 5, "is_turkey_relevant": True, "relevance_score": 0.7,
        "threat_relevance": 0.6, "persons": ["hasan kaya", "yusuf al-rashid", "ahmet yilmaz"],
    },
    {
        "title": "Sınır bölgesinde kaçakçılık aktivitesinde artış trendi",
        "content": "Suriye sınırında kaçakçılık faaliyetlerinin son 3 ayda %40 arttığı rapor edildi. Özellikle Kilis-Öncüpınar hattında gece geçişleri tespit ediliyor.",
        "source": "Güvenlik Analiz", "category": "conflict", "sentiment": "negative",
        "lat": 36.6512, "lng": 37.0134, "country": "Turkey", "city": "Kilis",
        "days_ago": 3, "is_turkey_relevant": True, "relevance_score": 0.9,
        "threat_relevance": 0.8, "persons": ["mehmet karaca", "ahmet yilmaz", "mustafa al-rashid", "hasan kaya"],
    },
    {
        "title": "MASAK'tan şüpheli finansal işlem uyarısı: Kuyumculuk sektörü",
        "content": "MASAK, kuyumculuk sektöründe artan şüpheli işlemlere dikkat çekti. Özellikle altın eritme ve yeniden dökme işlemlerinin para aklama aracı olarak kullanılabildiği belirtildi.",
        "source": "Ekonomi Haber", "category": "economy", "sentiment": "negative",
        "lat": 41.0107, "lng": 28.9680, "country": "Turkey", "city": "Istanbul",
        "days_ago": 7, "is_turkey_relevant": True, "relevance_score": 0.6,
        "threat_relevance": 0.5, "persons": ["elif demir", "omar hassan"],
    },
    {
        "title": "Suriye'de Azez bölgesinde silahlı grup hareketliliği",
        "content": "Suriye'nin kuzeyindeki Azez ilçesinde farklı silahlı gruplar arasında bölgesel güç mücadelesinin devam ettiği raporlandı.",
        "source": "Suriye Gündemi", "category": "conflict", "sentiment": "negative",
        "lat": 36.5864, "lng": 37.0478, "country": "Syria", "city": "Azez",
        "days_ago": 12, "is_turkey_relevant": True, "relevance_score": 0.7,
        "threat_relevance": 0.7, "persons": ["mustafa al-rashid"],
    },
    {
        "title": "Adana'da enerji altyapısı güvenlik değerlendirmesi toplantısı",
        "content": "Adana Valiliği, bölgedeki enerji altyapılarının güvenlik durumunu değerlendirmek üzere bir toplantı düzenledi. BTC hattı ve enerji iletim hatları ele alındı.",
        "source": "Adana Gündem", "category": "politics", "sentiment": "neutral",
        "lat": 37.0017, "lng": 35.3213, "country": "Turkey", "city": "Adana",
        "days_ago": 6, "is_turkey_relevant": True, "relevance_score": 0.7,
        "threat_relevance": 0.6, "persons": ["zeynep aktas"],
    },
    {
        "title": "Gaziantep'te hawala ağına yönelik soruşturma başlatıldı",
        "content": "Gaziantep'te yasadışı para transferi (hawala) ağlarına yönelik kapsamlı bir soruşturma başlatıldığı öğrenildi. Suriye uyruklu birçok kişinin ifadeye çağrıldığı belirtildi.",
        "source": "Gaziantep Haber", "category": "conflict", "sentiment": "negative",
        "lat": 37.0662, "lng": 37.3833, "country": "Turkey", "city": "Gaziantep",
        "days_ago": 15, "is_turkey_relevant": True, "relevance_score": 0.7,
        "threat_relevance": 0.6, "persons": ["omar hassan"],
    },
    {
        "title": "İstanbul Ticaret Sicil'den şüpheli şirket kuruluşları raporu",
        "content": "İstanbul Ticaret Sicil Müdürlüğü, son 6 ayda kurulan bazı şirketlerin gerçek ticari faaliyet göstermediğini ve paravan şirket olabileceğini değerlendirdi.",
        "source": "İstanbul Ekonomi", "category": "economy", "sentiment": "negative",
        "lat": 41.0082, "lng": 28.9784, "country": "Turkey", "city": "Istanbul",
        "days_ago": 4, "is_turkey_relevant": True, "relevance_score": 0.5,
        "threat_relevance": 0.4, "persons": ["tarık ozkan", "elif demir"],
    },
    {
        "title": "Akkuyu NGS inşaat lojistik güzergahında güvenlik artırıldı",
        "content": "Mersin Akkuyu Nükleer Güç Santrali inşaatına malzeme taşıyan konvoy güzergahlarında güvenlik önlemleri artırıldı.",
        "source": "Enerji Gündem", "category": "politics", "sentiment": "neutral",
        "lat": 36.1440, "lng": 33.5260, "country": "Turkey", "city": "Mersin",
        "days_ago": 2, "is_turkey_relevant": True, "relevance_score": 0.8,
        "threat_relevance": 0.7, "persons": [],
    },
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 10. ORGANIZATIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ORGANIZATIONS = [
    {"name": "Kara Hat", "name_normalized": "kara hat", "org_type": "crime_network",
     "country": "Turkey", "description": "Silah kaçakçılığı örgütü, Güneydoğu Türkiye-Suriye hattında aktif.",
     "is_turkey_related": True, "lat": 37.0662, "lng": 37.3833},
    {"name": "Al-Rashid Nakliyat", "name_normalized": "al-rashid nakliyat", "org_type": "front_company",
     "country": "Turkey", "description": "Yusuf Al-Rashid'in kamyon şirketi. Meşru nakliye + kaçakçılık.",
     "is_turkey_related": True, "lat": 37.0662, "lng": 37.3833},
    {"name": "Atlas Dış Ticaret A.Ş.", "name_normalized": "atlas dış ticaret", "org_type": "front_company",
     "country": "Turkey", "description": "Tarık Özkan'ın paravan ithalat/ihracat şirketi. Volkov konteynerlerinin yasal girişi.",
     "is_turkey_related": True, "lat": 41.0082, "lng": 28.9784},
    {"name": "Güneş Kuyumculuk", "name_normalized": "güneş kuyumculuk", "org_type": "front_company",
     "country": "Turkey", "description": "Elif Demir'in Kapalıçarşı dükkanı. Para aklama merkezi.",
     "is_turkey_related": True, "lat": 41.0107, "lng": 28.9680},
    {"name": "Yıldırım Holding", "name_normalized": "yıldırım holding", "org_type": "conglomerate",
     "country": "Turkey", "description": "İbrahim Yıldırım'ın şirketler grubu. Petrol, inşaat, tarım, enerji.",
     "is_turkey_related": True, "lat": 37.0017, "lng": 35.3213},
    {"name": "CyberShield Bilişim", "name_normalized": "cybershield bilişim", "org_type": "tech_company",
     "country": "Turkey", "description": "Emre Çelik'in siber güvenlik firması. Örgüte teknoloji desteği.",
     "is_turkey_related": True, "lat": 37.0500, "lng": 35.3933},
    {"name": "Yıldız Lojistik Kargo", "name_normalized": "yıldız lojistik kargo", "org_type": "front_company",
     "country": "Turkey", "description": "Elif Demir'in Mersin deposu. Deniz yolu lojistik merkezi.",
     "is_turkey_related": True, "lat": 36.7937, "lng": 34.6159},
    {"name": "Boğa Ağı", "name_normalized": "boğa ağı", "org_type": "crime_network",
     "country": "Turkey", "description": "Ferhat Güneş'in rakip ağı. İnsan kaçakçılığı ve uyuşturucu.",
     "is_turkey_related": True, "lat": 37.0735, "lng": 37.3829},
]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SEED FUNCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def seed():
    init_db()
    db = SessionLocal()

    # Check if already seeded
    existing = db.query(Person).filter(Person.name_normalized == "mehmet karaca").first()
    if existing:
        print("[!] Kara Hat network already seeded. Use --force to re-seed.")
        if "--force" not in sys.argv:
            db.close()
            return
        print("[!] Force mode: deleting existing Kara Hat data...")
        from sqlalchemy import text
        # Delete in dependency order
        for pn in PERSONS:
            p = db.query(Person).filter(Person.name_normalized == pn["name_normalized"]).first()
            if p:
                # Junction tables first
                db.execute(text(f"DELETE FROM news_person WHERE person_id = {p.id}"))
                # Dependent tables
                db.query(PersonAlias).filter(PersonAlias.person_id == p.id).delete()
                db.query(PersonLocation).filter(PersonLocation.person_id == p.id).delete()
                db.query(PersonProfileAnalysis).filter(PersonProfileAnalysis.person_id == p.id).delete()
                db.query(PatternOfLife).filter(PatternOfLife.person_id == p.id).delete()
                db.query(SurveillanceRecord).filter(SurveillanceRecord.person_id == p.id).delete()
                # LinkConnection depends on LinkEntity
                link_ids = [le.id for le in db.query(LinkEntity).filter(LinkEntity.person_id == p.id).all()]
                if link_ids:
                    db.query(LinkConnection).filter(
                        (LinkConnection.source_id.in_(link_ids)) | (LinkConnection.target_id.in_(link_ids))
                    ).delete(synchronize_session=False)
                db.query(LinkEntity).filter(LinkEntity.person_id == p.id).delete()
                db.query(ReconstructedTimeline).filter(ReconstructedTimeline.person_id == p.id).delete()
                db.query(PersonMeeting).filter(
                    (PersonMeeting.person_a_id == p.id) | (PersonMeeting.person_b_id == p.id)
                ).delete(synchronize_session=False)
                db.query(PersonRelationship).filter(
                    (PersonRelationship.person_a_id == p.id) | (PersonRelationship.person_b_id == p.id)
                ).delete(synchronize_session=False)
                # Delete the person itself
                db.delete(p)
        db.commit()
        print("[!] Mevcut veriler silindi.")

    print("=" * 60)
    print("  KARA HAT SUÇ ÖRGÜTÜ — Test Verisi Üretici")
    print("=" * 60)

    # ── 1. CREATE PERSONS ──
    print("\n[1/9] Kişiler oluşturuluyor...")
    person_map = {}  # normalized_name → Person object

    for p_data in PERSONS:
        p = Person(
            name=p_data["name"],
            name_normalized=p_data["name_normalized"],
            role=p_data["role"],
            nationality=p_data["nationality"],
            profile_notes=p_data["profile_notes"],
            is_turkey_related=p_data["is_turkey_related"],
            last_known_country=p_data["last_known_country"],
            last_known_city=p_data["last_known_city"],
            geom=make_point(p_data["lng"], p_data["lat"]),
            mention_count=p_data["mention_count"],
            first_seen=D(60),
            last_seen=D(1),
            created_at=D(60),
        )
        db.add(p)
        db.flush()
        person_map[p_data["name_normalized"]] = p
        print(f"    [+] {p.name} (id={p.id})")

    # ── 2. CREATE ALIASES ──
    print("\n[2/9] Kod adları oluşturuluyor...")
    for person_norm, aliases in ALIASES.items():
        p = person_map.get(person_norm)
        if not p:
            continue
        for alias_name, alias_type in aliases:
            db.add(PersonAlias(
                person_id=p.id,
                alias_name=alias_name,
                alias_type=alias_type,
                first_seen_at=D(45),
            ))
    db.flush()
    print(f"    [+] {sum(len(v) for v in ALIASES.values())} alias oluşturuldu")

    # ── 3. CREATE RELATIONSHIPS ──
    print("\n[3/9] İlişkiler oluşturuluyor...")
    for r in RELATIONSHIPS:
        pa = person_map.get(r[0])
        pb = person_map.get(r[1])
        if not pa or not pb:
            continue
        db.add(PersonRelationship(
            person_a_id=pa.id, person_b_id=pb.id,
            relation_type=r[2], sentiment=r[3], strength=r[4],
            evidence_count=random.randint(2, 12),
            first_observed_at=D(random.randint(30, 180)),
            last_observed_at=D(random.randint(1, 10)),
            source_summary=r[5],
        ))
    db.flush()
    print(f"    [+] {len(RELATIONSHIPS)} ilişki oluşturuldu")

    # ── 4. CREATE MEETINGS ──
    print("\n[4/9] Buluşmalar oluşturuluyor...")
    for m in MEETINGS:
        pa = person_map.get(m[0])
        pb = person_map.get(m[1])
        if not pa or not pb:
            continue
        db.add(PersonMeeting(
            person_a_id=pa.id, person_b_id=pb.id,
            meeting_date=D(m[2]),
            geom=make_point(m[4], m[3]),
            location_country=m[5], location_city=m[6],
            meeting_type=m[7], context=m[8],
        ))
    db.flush()
    print(f"    [+] {len(MEETINGS)} buluşma oluşturuldu")

    # ── 5. CREATE PERSON LOCATIONS ──
    print("\n[5/9] Konum geçmişi oluşturuluyor...")
    for loc in LOCATIONS:
        p = person_map.get(loc[0])
        if not p:
            continue
        db.add(PersonLocation(
            person_id=p.id,
            geom=make_point(loc[3], loc[2]),
            country=loc[4], city=loc[5],
            location_type=loc[6],
            timestamp=D(loc[1]),
        ))
    db.flush()
    print(f"    [+] {len(LOCATIONS)} konum kaydı oluşturuldu")

    # ── 6. CREATE SURVEILLANCE RECORDS ──
    print("\n[6/9] Gözetim kayıtları oluşturuluyor...")
    for s in SURVEILLANCE:
        p = person_map.get(s[0])
        if not p:
            continue
        db.add(SurveillanceRecord(
            person_id=p.id,
            source_type=s[1], source_name=s[2],
            latitude=s[4], longitude=s[5],
            country=s[6], city=s[7],
            captured_at=D(s[3]),
            description=s[8],
            confidence=s[9],
            evidence_type="document",
            is_verified=True,
        ))
    db.flush()
    print(f"    [+] {len(SURVEILLANCE)} gözetim kaydı oluşturuldu")

    # ── 7. CREATE LINK ENTITIES & CONNECTIONS ──
    print("\n[7/9] Link analiz verileri oluşturuluyor...")
    link_map = {}  # value → LinkEntity

    for le in LINK_ENTITIES:
        p = person_map.get(le[0])
        if not p:
            continue
        entity = LinkEntity(
            entity_type=le[1], entity_value=le[2], entity_label=le[3],
            person_id=p.id, is_suspicious=le[4], risk_score=le[5],
            is_confirmed=True,
            first_seen=D(60), last_seen=D(1),
        )
        db.add(entity)
        db.flush()
        link_map[le[2]] = entity

    print(f"    [+] {len(LINK_ENTITIES)} link varlığı oluşturuldu")

    for lc in LINK_CONNECTIONS_DATA:
        src = link_map.get(lc[0])
        tgt = link_map.get(lc[1])
        if not src or not tgt:
            continue
        db.add(LinkConnection(
            source_id=src.id, target_id=tgt.id,
            connection_type=lc[2], direction=lc[3],
            strength=lc[4], frequency=lc[5],
            is_suspicious=lc[6],
            total_amount=lc[7], currency=lc[8],
            evidence_summary=lc[9],
            first_observed=D(60), last_observed=D(2),
        ))
    db.flush()
    print(f"    [+] {len(LINK_CONNECTIONS_DATA)} link bağlantısı oluşturuldu")

    # ── 8. CREATE NEWS + ORG ASSOCIATIONS ──
    print("\n[8/9] Haberler ve kuruluşlar oluşturuluyor...")

    # Organizations first
    org_map = {}
    for o in ORGANIZATIONS:
        org = Organization(
            name=o["name"], name_normalized=o["name_normalized"],
            org_type=o["org_type"], country=o["country"],
            description=o["description"], is_turkey_related=o["is_turkey_related"],
            geom=make_point(o["lng"], o["lat"]),
            mention_count=random.randint(3, 15),
            first_seen=D(60), last_seen=D(1),
        )
        db.add(org)
        db.flush()
        org_map[o["name_normalized"]] = org
    print(f"    [+] {len(ORGANIZATIONS)} kuruluş oluşturuldu")

    # News articles
    for n in NEWS_ARTICLES:
        article = News(
            title=n["title"],
            content=n["content"],
            url=f"https://example.com/news/{random.randint(10000,99999)}",
            source=n["source"],
            language="tr",
            published_at=D(n["days_ago"]),
            collected_at=D(n["days_ago"]),
            geom=make_point(n["lng"], n["lat"]),
            location_country=n["country"],
            location_city=n["city"],
            is_processed=True,
            summary=n["content"][:200],
            category=n["category"],
            sentiment=n["sentiment"],
            is_turkey_relevant=n["is_turkey_relevant"],
            relevance_score=n["relevance_score"],
            threat_relevance=n["threat_relevance"],
            priority_score=round(n["threat_relevance"] * 7 + random.uniform(0, 2), 1),
            is_breaking=n["threat_relevance"] >= 0.7,
        )
        db.add(article)
        db.flush()

        # Link persons to news
        for pn in n["persons"]:
            p = person_map.get(pn)
            if p:
                db.execute(news_person.insert().values(news_id=article.id, person_id=p.id))

    db.flush()
    print(f"    [+] {len(NEWS_ARTICLES)} haber oluşturuldu ve kişilere bağlandı")

    # ── 9. CREATE PROFILE ANALYSES & PATTERN OF LIFE ──
    print("\n[9/9] Profil analizleri ve davranış kalıpları oluşturuluyor...")

    # Mehmet Karaca Profile
    karaca = person_map["mehmet karaca"]
    db.add(PersonProfileAnalysis(
        person_id=karaca.id,
        personality_type="Stratejik-Paranoid / Otoriter Lider",
        emotional_state="Kontrollü gerilim — Nisan operasyonu öncesi artan stres belirtileri.",
        stress_level="high",
        decision_style="Hızlı karar alır ancak önemli konularda Reis'e danışır. Anti-takip konusunda deneyimli.",
        risk_tolerance="calculated",
        strengths_json=[
            {"trait": "Anti-takip yeteneği", "description": "Mağazaya girip arka kapıdan çıkma, yön değiştirme gibi profesyonel teknikler kullanıyor.", "confidence": 0.9},
            {"trait": "Hücre yapısı disiplini", "description": "Örgüt üyelerinin birbirini tanımamasını sağlıyor. Merkezi düğüm noktası.", "confidence": 0.85},
            {"trait": "Çoklu kimlik kullanımı", "description": "3 farklı IMEI, sürekli SIM değişimi, sahte kimlikler.", "confidence": 0.8},
            {"trait": "Geniş coğrafi hareket alanı", "description": "5 şehirde aktif: İstanbul, Ankara, Adana, Gaziantep, Kilis.", "confidence": 0.9},
        ],
        weaknesses_json=[
            {"trait": "Aile bağı", "description": "İbrahim Yıldırım akraba bağı — örgüt hiyerarşisini kişiselleştiriyor.", "exploitability": 0.7, "confidence": 0.8},
            {"trait": "Merkezi kontrol bağımlılığı", "description": "Tüm kararlar ondan geçiyor — yakalanırsa örgüt felç olur.", "exploitability": 0.9, "confidence": 0.9},
            {"trait": "Ankara güvenli evi", "description": "Sabit bir nokta kullanması takip kolaylığı sağlıyor.", "exploitability": 0.75, "confidence": 0.85},
            {"trait": "Zeynep Aktaş riski", "description": "Bir sivili örgüte dahil etmesi operasyonel risk artırıyor.", "exploitability": 0.6, "confidence": 0.7},
        ],
        habits_json=[
            {"habit": "Sabah erkenci", "frequency": "daily", "location": "Konaklama", "time_pattern": "06:00-07:00"},
            {"habit": "Anti-takip rotası", "frequency": "Her şehir değişiminde", "location": "Şehir merkezi", "time_pattern": "Varıştan 1 saat sonra"},
            {"habit": "Depo denetimi", "frequency": "Gaziantep'te günlük", "location": "Şahinbey Sanayi", "time_pattern": "09:00-11:00"},
        ],
        political_orientation="Pragmatist — ideolojik motivasyon yok, tamamen ticari çıkar.",
        loyalties_json=[
            {"entity": "İbrahim Yıldırım (Reis)", "loyalty_level": "very_high", "since": "2020", "notes": "Akrabalık + patron"},
            {"entity": "Kara Hat örgütü", "loyalty_level": "high", "since": "2021", "notes": "Kurucusu ve lideri"},
        ],
        motivations_json=[
            {"motivation": "Güç ve kontrol", "priority": 1, "evidence": "Örgüt üzerinde mutlak otorite"},
            {"motivation": "Finansal kazanç", "priority": 2, "evidence": "Aylık tahmini 100K+ USD gelir"},
        ],
        key_contacts_json=[
            {"name": "İbrahim Yıldırım", "role": "Patron/Hami", "relationship": "Akraba + finansör", "trust_level": "very_high", "frequency": "Haftada 1-2"},
            {"name": "Ahmet Yilmaz", "role": "Silah hattı şefi", "relationship": "Güvenilir saha operatörü", "trust_level": "high", "frequency": "Günlük"},
            {"name": "Elif Demir", "role": "Finans sorumlusu", "relationship": "Para aklama koordinatörü", "trust_level": "high", "frequency": "Haftada 2-3"},
            {"name": "Dimitri Volkov", "role": "Tedarikçi", "relationship": "Silah tedarik zinciri", "trust_level": "medium", "frequency": "Ayda 2-3"},
        ],
        adversaries_json=[
            {"name": "Ferhat Güneş (Boğa)", "reason": "Gaziantep bölgesel rekabet", "threat_level": "high"},
            {"name": "Selim Arslan (Kurt)", "reason": "Eski ortak, ihanet şüphesi, muhtemel muhbir", "threat_level": "critical"},
        ],
        travel_patterns_json=[
            {"route": "İstanbul → Ankara → Gaziantep → Kilis", "frequency": "Ayda 1-2", "purpose": "Ana operasyon hattı", "last_seen": D(4).strftime("%Y-%m-%d")},
            {"route": "Adana ↔ Gaziantep", "frequency": "Haftada 1", "purpose": "Koordinasyon", "last_seen": D(6).strftime("%Y-%m-%d")},
        ],
        predictions_json=[
            {"date": DF(1).strftime("%Y-%m-%d"), "location": {"city": "Kilis", "country": "Turkey", "lat": 36.7184, "lng": 37.1212}, "activity": "Nisan operasyonu — sınır bölgesinde koordinasyon", "confidence": 0.75},
            {"date": DF(5).strftime("%Y-%m-%d"), "location": {"city": "Istanbul", "country": "Turkey", "lat": 41.0082, "lng": 28.9784}, "activity": "Operasyon sonrası İstanbul dönüşü ve gelir dağıtımı", "confidence": 0.55},
        ],
        next_likely_location={"city": "Kilis", "country": "Turkey", "lat": 36.7184, "lng": 37.1212, "confidence": 0.75, "reasoning": "Nisan operasyonu için sınır bölgesine hareket bekleniyor."},
        threat_forecast="KRİTİK — Nisan operasyonu 48 saat içinde. 5 araçlık konvoy + sınır geçişi. Yakalama penceresi: Gaziantep-Kilis güzergahı.",
        overall_threat_level="critical",
        analyst_assessment="Mehmet Karaca, Kara Hat örgütünün merkezi düğüm noktasıdır. Yakalanması örgütü büyük ölçüde felç eder. En uygun yakalama noktası: Yıldırım İstasyon-3 (Oğuzeli) veya Ankara güvenli evi.",
        reliability_score=0.82,
        last_updated=NOW,
    ))

    # Elif Demir Profile
    demir = person_map["elif demir"]
    db.add(PersonProfileAnalysis(
        person_id=demir.id,
        personality_type="Pragmatik-Hesapçı / Düzenli ve Metodik",
        emotional_state="Sakin görünümlü ancak Mersin operasyonu ile artan baskı hissediyor.",
        stress_level="medium",
        decision_style="Sistematik ve düzenli. Muhasebeci geçmişi karar alma sürecini etkiliyor.",
        risk_tolerance="low",
        strengths_json=[
            {"trait": "Finansal zeka", "description": "Karmaşık para aklama şemasını tek başına yönetiyor.", "confidence": 0.9},
            {"trait": "Çift yaşam", "description": "Gündüz meşru kuyumcu, gece örgüt finansçısı. Mükemmel paravan.", "confidence": 0.85},
        ],
        weaknesses_json=[
            {"trait": "Instagram lokasyon paylaşımı", "description": "Gaziantep seyahatini sosyal medyadan paylaşmış.", "exploitability": 0.8, "confidence": 0.9},
            {"trait": "Sabit rutin", "description": "İstanbul'daki günlük rutini son derece tahmin edilebilir.", "exploitability": 0.85, "confidence": 0.9},
            {"trait": "Dijital iz", "description": "kelebek34@gmail.com ile Volkov bağlantısı, şifrelenmemiş.", "exploitability": 0.8, "confidence": 0.85},
        ],
        habits_json=[
            {"habit": "Dükkan açılışı", "frequency": "daily", "location": "Kapalıçarşı", "time_pattern": "08:30"},
            {"habit": "Mersin seyahati", "frequency": "Haftada 1", "location": "Mersin deposu", "time_pattern": "Otobüs/uçak"},
        ],
        travel_patterns_json=[
            {"route": "İstanbul ↔ Gaziantep", "frequency": "Ayda 2-3", "purpose": "Altın teslim/hawala", "last_seen": D(19).strftime("%Y-%m-%d")},
            {"route": "İstanbul ↔ Mersin", "frequency": "Haftada 1", "purpose": "Depo operasyonu", "last_seen": D(8).strftime("%Y-%m-%d")},
        ],
        overall_threat_level="high",
        analyst_assessment="Elif Demir, örgütün finansal omurgasıdır. Yakalanması para aklama mekanizmasını çökertir. En kolay yakalama: Kapalıçarşı günlük rutininde.",
        reliability_score=0.80,
        last_updated=NOW,
    ))

    # Pattern of Life — Karaca
    db.add(PatternOfLife(
        person_id=karaca.id,
        analysis_start=D(60), analysis_end=D(1),
        data_points_count=85,
        home_base={"city": "Gaziantep", "country": "Turkey", "lat": 37.0662, "lng": 37.3833, "confidence": 0.7},
        work_location={"city": "Gaziantep", "country": "Turkey", "lat": 37.0662, "lng": 37.3833, "type": "Şahinbey Sanayi deposu"},
        frequent_locations=[
            {"city": "Gaziantep", "visits": 25, "avg_duration_hours": 72},
            {"city": "Adana", "visits": 8, "avg_duration_hours": 48},
            {"city": "Kilis", "visits": 6, "avg_duration_hours": 24},
            {"city": "Istanbul", "visits": 4, "avg_duration_hours": 36},
            {"city": "Ankara", "visits": 3, "avg_duration_hours": 24},
        ],
        travel_corridors=[
            {"from": "Gaziantep", "to": "Kilis", "frequency": 6, "mode": "car"},
            {"from": "Adana", "to": "Gaziantep", "frequency": 5, "mode": "car"},
            {"from": "Istanbul", "to": "Ankara", "frequency": 3, "mode": "car"},
        ],
        active_hours={"start": "06:00", "end": "23:00", "timezone": "Europe/Istanbul"},
        weekly_pattern={"mon": "operational", "tue": "operational", "wed": "meetings", "thu": "travel", "fri": "travel", "sat": "planning", "sun": "rest"},
        routine_score=0.55,
        counter_surveillance=["Mağaza girip arka kapıdan çıkma", "2 kez yön değiştirme", "Taksi değişimi", "IMEI değişimi (3 farklı)"],
        anomalies_detected=["20 Mart İstanbul ziyareti (beklenmedik)", "26 Mart Adana toplantısı (çok büyük katılım)"],
        risk_indicators=["Anti-takip hareketleri artıyor", "Operasyon temposu hızlanıyor", "Yeni üyeler ekleniyor"],
        vulnerability_windows=["Ankara güvenli evinde 2+ saat kalıyor", "Depo ziyaretleri tahmin edilebilir"],
        predictability_score=0.45,
        generated_by="analyst",
        last_updated=NOW,
    ))

    # Pattern of Life — Elif Demir
    db.add(PatternOfLife(
        person_id=demir.id,
        analysis_start=D(60), analysis_end=D(1),
        data_points_count=60,
        home_base={"city": "Istanbul", "country": "Turkey", "lat": 41.0164, "lng": 28.9547, "address": "Fatih, Çarşamba Mah."},
        work_location={"city": "Istanbul", "country": "Turkey", "lat": 41.0107, "lng": 28.9680, "type": "Kapalıçarşı, Güneş Kuyumculuk"},
        frequent_locations=[
            {"city": "Istanbul", "visits": 45, "avg_duration_hours": 168},
            {"city": "Gaziantep", "visits": 6, "avg_duration_hours": 12},
            {"city": "Mersin", "visits": 4, "avg_duration_hours": 36},
        ],
        active_hours={"start": "07:30", "end": "19:00", "timezone": "Europe/Istanbul"},
        weekly_pattern={"mon": "dükkan", "tue": "dükkan+seyahat", "wed": "dükkan", "thu": "dükkan", "fri": "dükkan+cuma", "sat": "kapalı", "sun": "kapalı"},
        routine_score=0.80,
        spending_patterns=[
            {"type": "Altın alım-satım", "amount_monthly": "2-3M TL", "suspicious": True},
            {"type": "Depo kirası (Mersin)", "amount_monthly": "35.000 TL", "suspicious": True},
        ],
        financial_anomalies=["Aylık altın hacmi meşru dükkan boyutunun 10 katı", "MASAK ŞİB bildirimi (Şubat)"],
        predictability_score=0.80,
        vulnerability_windows=["Kapalıçarşı günlük rutini tahmin edilebilir", "Gaziantep uçuşları önceden bilet alıyor"],
        generated_by="system",
        last_updated=NOW,
    ))

    # ── COMMIT ──
    db.commit()

    # ── SUMMARY ──
    person_count = db.query(Person).count()
    alias_count = db.query(PersonAlias).count()
    rel_count = db.query(PersonRelationship).count()
    meeting_count = db.query(PersonMeeting).count()
    loc_count = db.query(PersonLocation).count()
    surv_count = db.query(SurveillanceRecord).count()
    link_e_count = db.query(LinkEntity).count()
    link_c_count = db.query(LinkConnection).count()
    news_count = db.query(News).count()
    org_count = db.query(Organization).count()

    print("\n" + "=" * 60)
    print("  SEED TAMAMLANDI — ÖZET")
    print("=" * 60)
    print(f"  Kişiler:           {person_count}")
    print(f"  Kod adları:        {alias_count}")
    print(f"  İlişkiler:         {rel_count}")
    print(f"  Buluşmalar:        {meeting_count}")
    print(f"  Konum kayıtları:   {loc_count}")
    print(f"  Gözetim kayıtları: {surv_count}")
    print(f"  Link varlıkları:   {link_e_count}")
    print(f"  Link bağlantıları: {link_c_count}")
    print(f"  Haberler:          {news_count}")
    print(f"  Kuruluşlar:        {org_count}")
    print("=" * 60)
    print("\n  Şimdi rapor dosyalarını sisteme yükleyin:")
    print("  POST /api/report-intel/files/scan?auto_parse=true")
    print()

    db.close()


if __name__ == "__main__":
    seed()
