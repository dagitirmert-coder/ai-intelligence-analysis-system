"""
Seed script: Create comprehensive intelligence profile analysis for Ahmet Yilmaz.

Generates:
- Full psychological profile
- Strengths & weaknesses with exploitability scores
- Political & ideological analysis
- Key contacts and adversaries
- Behavioral patterns (travel, communication, daily routine)
- Future predictions with locations and dates
- News-derived intelligence summary
- Public statements

Usage:
    python seed_profile_analysis.py
"""
import os
import sys
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.engine import SessionLocal
from db.models import Person, PersonProfileAnalysis


# ── Dates (relative to today) ────────────────────────────
NOW = datetime.now(timezone.utc)


AHMET_PROFILE = {
    # ── Psychological Profile ──
    "personality_type": "Paranoid-Metikulöz (Hesapçı Kaçınmacı)",
    "emotional_state": "Yüksek gerilim altında kontrollü — son operasyonlarda artan tedirginlik belirtileri. "
                       "Gaziantep buluşmasında sinirli tavırlar gözlemlendi. Uykusuzluk belirtileri mevcut.",
    "stress_level": "high",
    "decision_style": "Aşırı temkinli, her kararı 48-72 saat düşünür. Kritik kararları yalnız alır, "
                      "danışman kullanmaz. Rutin değişikliklerinden kaçınır ama baskı altında hızlı refleks gösterir.",
    "risk_tolerance": "calculated",

    # ── Strengths ──
    "strengths_json": [
        {
            "trait": "Operasyonel disiplin",
            "description": "Telefon kullanımını minimize eder, her görüşme için farklı buluşma noktası seçer. "
                           "Dijital ayak izi bırakmamak konusunda eğitimli.",
            "confidence": 0.9
        },
        {
            "trait": "Lojistik zekası",
            "description": "Karmaşık tedarik zincirlerini hafızadan yönetir. Birden fazla alternatif rota "
                           "planlar ve anında değiştirebilir.",
            "confidence": 0.85
        },
        {
            "trait": "İnsan yönetimi",
            "description": "Alt kademe operatörler üzerinde güçlü otorite. Sadakat ödüllendirilir, "
                           "ihanet ağır cezalandırılır. Korkuyla değil saygıyla yönetir.",
            "confidence": 0.8
        },
        {
            "trait": "Adaptasyon yeteneği",
            "description": "Plaka değişimi, SIM değişimi, kimlik değişimi konusunda hızlı. "
                           "Adana gişesinde tespit edilen plaka değişimi bunu kanıtlıyor.",
            "confidence": 0.9
        },
    ],

    # ── Weaknesses ──
    "weaknesses_json": [
        {
            "trait": "Aile bağımlılığı",
            "description": "İstanbul Üsküdar'da yaşayan annesini düzenli ziyaret eder. Bu ziyaretler "
                           "önceden tahmin edilebilir patern oluşturuyor. Annesi hasta (diyabet).",
            "exploitability": 0.85,
            "confidence": 0.8
        },
        {
            "trait": "Rutine bağlılık",
            "description": "Sabah 05:30-06:00 arası uyanır, mutlaka çay içer. Yeni şehirlere varışta "
                           "ilk iş olarak merkezi bir kahvehane arar. Bu önceden tahmin edilebilir.",
            "exploitability": 0.7,
            "confidence": 0.85
        },
        {
            "trait": "Dimitri Volkov'a bağımlılık",
            "description": "Tek güvenilir uluslararası tedarikçisi Volkov. Volkov devre dışı kalırsa "
                           "tedarik zinciri çöker. Bu ilişki kritik kırılganlık noktası.",
            "exploitability": 0.9,
            "confidence": 0.85
        },
        {
            "trait": "Ego / küçümsenme hassasiyeti",
            "description": "Otoritesinin sorgulanmasına tahammülsüz. Geçmişte Hasan Kaya ile bu yüzden "
                           "gerginlik yaşandı. Provokasyona açık.",
            "exploitability": 0.6,
            "confidence": 0.7
        },
        {
            "trait": "Teknoloji yetersizliği",
            "description": "Dijital güvenlik bilgisi yüzeysel. VPN kullanmaz, şifreleme yeteneği sınırlı. "
                           "IMEI değiştirmiyor, sadece SIM değiştiriyor — bu teknik bir zafiyet.",
            "exploitability": 0.8,
            "confidence": 0.9
        },
    ],

    # ── Habits ──
    "habits_json": [
        {"habit": "Sabah erken kalkma", "frequency": "daily", "location": "Her konaklamada", "time_pattern": "05:30-06:00"},
        {"habit": "Kahvehane buluşması", "frequency": "Her yeni şehirde", "location": "Merkezi mahalle kahvehanesi", "time_pattern": "Varıştan 2-3 saat sonra"},
        {"habit": "Araç değişimi", "frequency": "Her 200-300km", "location": "Şehirler arası", "time_pattern": "Gece yarısı"},
        {"habit": "Nakit kullanımı", "frequency": "Her zaman", "location": "Tüm işlemler", "time_pattern": "Sürekli"},
        {"habit": "Anne ziyareti", "frequency": "2 haftada bir", "location": "Üsküdar, İstanbul", "time_pattern": "Cuma öğleden sonra"},
        {"habit": "Cami ziyareti", "frequency": "Cuma", "location": "Varış şehrinin merkez camisi", "time_pattern": "12:00-13:00"},
    ],

    # ── Political & Ideological ──
    "political_orientation": "Pragmatist — ideolojik motivasyon düşük, finansal çıkar birincil. "
                             "Milliyetçi söylem kullanır ama ikna edici değil. Herhangi bir partiye "
                             "açık bağlılığı yok.",
    "ideological_notes": "Din konusunda yüzeysel pratik (Cuma namazı). Asıl motivasyonu para ve güç. "
                         "Suriye iç savaşından fırsatçı yararlanma — taraf tutmuyor, herkese satıyor. "
                         "Kürt bölgelerinde de Arap bölgelerinde de iş yapıyor. Ulusal sadakati şüpheli.",
    "loyalties_json": [
        {"entity": "Bozkurt Hattı ağı", "loyalty_level": "high", "since": "2021", "notes": "Ağın kurucu üyesi, kişisel çıkarla bağlı"},
        {"entity": "Aile (anne, kardeş)", "loyalty_level": "very_high", "since": "Doğum", "notes": "En güçlü bağ — operasyonel zayıflık"},
        {"entity": "Hasan Kaya", "loyalty_level": "medium", "since": "2023", "notes": "İş ortaklığı, kişisel değil"},
        {"entity": "Dimitri Volkov", "loyalty_level": "low", "since": "2024", "notes": "Tamamen ticari, güven sınırlı"},
    ],
    "motivations_json": [
        {"motivation": "Finansal kazanç", "priority": 1, "evidence": "Tüm operasyonlar kâr odaklı, ideolojik motivasyon yok"},
        {"motivation": "Aile güvenliği", "priority": 2, "evidence": "Anne bakım masrafları operasyonların sürmesinin bir nedeni"},
        {"motivation": "Statü / saygınlık", "priority": 3, "evidence": "Ağ içinde 'Kartal' kod adıyla tanınma isteği"},
        {"motivation": "Macera / adrenalin", "priority": 4, "evidence": "Tehlikeli operasyonlara gönüllü katılım"},
    ],

    # ── Key Contacts ──
    "key_contacts_json": [
        {
            "name": "Hasan Kaya",
            "role": "Lojistik sorumlusu",
            "relationship": "İş ortağı — kamyon filosu sağlıyor",
            "trust_level": "medium",
            "frequency": "Haftada 1-2 kez",
            "notes": "Kadıköy buluşması teyit edildi. Bazen anlaşmazlık yaşanıyor."
        },
        {
            "name": "Dimitri Volkov",
            "role": "Uluslararası tedarikçi",
            "relationship": "Odessa üzerinden malzeme sağlıyor",
            "trust_level": "low",
            "frequency": "Ayda 1-2 kez",
            "notes": "Gaziantep otel buluşması. Volkov güvenilmez ama alternatifi yok."
        },
        {
            "name": "Fatma Yilmaz (anne)",
            "role": "Aile",
            "relationship": "Anne — Üsküdar'da yaşıyor, diyabet hastası",
            "trust_level": "absolute",
            "frequency": "2 haftada bir ziyaret",
            "notes": "Operasyonel zayıflık noktası. Telefonla da iletişim kuruyor."
        },
        {
            "name": "Bilinmeyen temas 'Şahin'",
            "role": "Sınır geçiş koordinatörü",
            "relationship": "Kilis sınır hattında lojistik sağlıyor",
            "trust_level": "medium",
            "frequency": "Operasyon bazlı",
            "notes": "Yalnızca kod adıyla biliniyor. Suriye tarafı bağlantı."
        },
        {
            "name": "Garage sahibi (Ankara-Ulus)",
            "role": "Araç tedariği",
            "relationship": "Sahte plakalı araç sağlıyor",
            "trust_level": "low",
            "frequency": "Ankara geçişlerinde",
            "notes": "Ulus'taki depo ziyareti drone ile teyit edildi."
        },
    ],

    # ── Adversaries ──
    "adversaries_json": [
        {"name": "Rakip ağ lideri 'Boğa'", "reason": "Gaziantep bölgesinde pazar payı kavgası", "threat_level": "high"},
        {"name": "Eski ortak Selim Arslan", "reason": "2024'te ihanet — bilgi sızdırdığı şüphesi", "threat_level": "medium"},
        {"name": "Emniyet İstihbarat Şb.", "reason": "Aktif soruşturma dosyası mevcut", "threat_level": "critical"},
    ],

    # ── Travel Patterns ──
    "travel_patterns_json": [
        {
            "route": "İstanbul → Ankara → Gaziantep → Kilis",
            "frequency": "Ayda 1-2 kez",
            "purpose": "Ana tedarik hattı operasyonu",
            "last_seen": "2026-03-13",
            "notes": "E5 → O4 otoyolu kullanıyor, gece seyahat tercih ediyor"
        },
        {
            "route": "İstanbul → Üsküdar (anne ziyareti)",
            "frequency": "2 haftada bir",
            "purpose": "Kişisel — aile ziyareti",
            "last_seen": "2026-03-08",
            "notes": "Cuma öğleden sonra, 2-3 saat kalıyor"
        },
        {
            "route": "Gaziantep → Suriye sınırı (Kilis/Öncüpınar)",
            "frequency": "Operasyon bazlı",
            "purpose": "Sınır ötesi sevkiyat koordinasyonu",
            "last_seen": "2026-03-13",
            "notes": "Suriye tarafında 'Abu Tarek' kimliği ile hareket ediyor"
        },
        {
            "route": "İstanbul → Ambarlı Limanı",
            "frequency": "Ayda 1",
            "purpose": "Konteyner sevkiyat kontrolü",
            "last_seen": "2026-03-10",
            "notes": "Uydu görüntüsü ile teyit edildi"
        },
    ],

    "communication_patterns": (
        "Telefon kullanımı minimal — günde max 2-3 kısa arama. Her şehirde yeni SIM alıyor ama "
        "IMEI değiştirmiyor (kritik zafiyet). Önemli görüşmeler yüz yüze. Kurye sistemi kullanıyor — "
        "Hasan Kaya üzerinden mesaj iletimi. Şifreli dil: 'malzeme' = silah, 'çay' = buluşma, "
        "'yola çıkıyorum' = sevkiyat başladı, 'hava güzel' = güvenli, 'yağmur yağıyor' = tehlike."
    ),

    "financial_patterns": (
        "Tamamen nakit operasyon — banka hesabı yok (tespit edilen). Gaziantep'te bir sarraftan "
        "düzenli döviz alımı (dolar/euro). Tahmini operasyon bütçesi: aylık 50-80 bin USD. "
        "Annesi adına İstanbul'da bir daire var (muhtemelen kara para aklama). "
        "Volkov'a ödemeler Havale değil fiziki altın ile yapılıyor."
    ),

    # ── Daily Routine ──
    "daily_routine_json": [
        {"time_range": "05:30-06:00", "activity": "Uyanma, çay", "location": "Konaklama yeri", "regularity": "very_high"},
        {"time_range": "06:00-07:00", "activity": "Çevre kontrolü, araç kontrol", "location": "Konaklama çevresi", "regularity": "high"},
        {"time_range": "08:00-10:00", "activity": "Kahvehane / bilgi toplama", "location": "Merkezi mahalle", "regularity": "high"},
        {"time_range": "10:00-12:00", "activity": "Operasyonel görüşmeler", "location": "Değişken", "regularity": "medium"},
        {"time_range": "12:00-13:00", "activity": "Öğle namazı (Cuma zorunlu)", "location": "Merkez cami", "regularity": "medium"},
        {"time_range": "14:00-18:00", "activity": "Seyahat / lojistik", "location": "Araç içi", "regularity": "medium"},
        {"time_range": "19:00-20:00", "activity": "Akşam yemeği (genelde lokanta)", "location": "Konaklama yakını", "regularity": "high"},
        {"time_range": "21:00-23:00", "activity": "Telefon kontrol, plan yapma", "location": "Konaklama yeri", "regularity": "high"},
        {"time_range": "23:00-05:30", "activity": "Uyku (hafif uyku, sık uyanma)", "location": "Konaklama yeri", "regularity": "medium"},
    ],

    # ── Predictions (future dates from today) ──
    "predictions_json": [
        {
            "date": (NOW + timedelta(days=2)).strftime("%Y-%m-%d"),
            "location": {"city": "İstanbul", "country": "Türkiye", "lat": 41.0251, "lng": 29.0198},
            "activity": "Anne ziyareti — Üsküdar",
            "confidence": 0.75,
            "reasoning": "2 haftalık periyodik ziyaret döngüsü. Son ziyaret ~12 gün önce. "
                         "Cuma gününe denk geliyor, geleneksel ziyaret günü."
        },
        {
            "date": (NOW + timedelta(days=5)).strftime("%Y-%m-%d"),
            "location": {"city": "İstanbul", "country": "Türkiye", "lat": 41.0049, "lng": 28.8563},
            "activity": "Ambarlı Limanı — konteyner sevkiyat kontrolü",
            "confidence": 0.6,
            "reasoning": "Aylık liman ziyaret döngüsü. Mart sonu sevkiyat dönemi. "
                         "Volkov'dan yeni malzeme bekleniyor."
        },
        {
            "date": (NOW + timedelta(days=8)).strftime("%Y-%m-%d"),
            "location": {"city": "Ankara", "country": "Türkiye", "lat": 39.9180, "lng": 32.8600},
            "activity": "Ulus deposu — araç ve plaka değişimi",
            "confidence": 0.55,
            "reasoning": "Güneydoğu hattı operasyonundan önce Ankara'da araç değişimi yapıyor. "
                         "Geçmiş 3 operasyonda aynı patern."
        },
        {
            "date": (NOW + timedelta(days=10)).strftime("%Y-%m-%d"),
            "location": {"city": "Gaziantep", "country": "Türkiye", "lat": 37.0662, "lng": 37.3833},
            "activity": "Sanayi sitesi buluşma — sevkiyat hazırlığı",
            "confidence": 0.65,
            "reasoning": "Ankara sonrası Gaziantep rotası standart. Sanayi sitesindeki depo "
                         "operasyonel üs olarak kullanılıyor."
        },
        {
            "date": (NOW + timedelta(days=12)).strftime("%Y-%m-%d"),
            "location": {"city": "Kilis", "country": "Türkiye", "lat": 36.7184, "lng": 37.1212},
            "activity": "Sınır bölgesi — sevkiyat geçişi koordinasyonu",
            "confidence": 0.5,
            "reasoning": "Gaziantep'ten 1-2 gün sonra Kilis'e geçiş. 'Şahin' ile buluşma. "
                         "Gece karanlığında sınır operasyonu bekleniyor."
        },
        {
            "date": (NOW + timedelta(days=18)).strftime("%Y-%m-%d"),
            "location": {"city": "İstanbul", "country": "Türkiye", "lat": 41.0082, "lng": 28.9784},
            "activity": "Dönüş — İstanbul'a geri geliş, gelir dağıtımı",
            "confidence": 0.5,
            "reasoning": "Operasyon sonrası İstanbul'a dönüş süreci ~5-7 gün. "
                         "Nakit dağıtımı ve sonraki operasyon planlaması."
        },
    ],

    "next_likely_location": {
        "city": "İstanbul",
        "country": "Türkiye",
        "lat": 41.0251,
        "lng": 29.0198,
        "confidence": 0.75,
        "reasoning": "Anne ziyaret döngüsü yaklaşıyor. Üsküdar bölgesinde 2-3 gün kalması bekleniyor.",
        "eta": (NOW + timedelta(days=2)).strftime("%Y-%m-%d"),
    },

    "threat_forecast": (
        "YÜKSEK TEHDİT — Önümüzdeki 2 hafta içinde yeni bir sınır ötesi sevkiyat operasyonu "
        "bekleniyor. Volkov ile Gaziantep buluşmasında fiyat anlaşmasının sağlandığı teyit edildi. "
        "Operasyon rotası: İstanbul → Ankara (araç değişimi) → Gaziantep (depo) → Kilis (sınır geçişi). "
        "EN KRİTİK PENCERE: +8 ile +12 gün arası. Yakalama operasyonu için en uygun nokta: "
        "Bolu Tüneli gişesi (kaçış imkanı en düşük) veya Ankara Ulus deposu (sabit konum, 2+ saat kalıyor)."
    ),

    # ── News / OSINT ──
    "news_mentions_summary": (
        "Son 30 günde 'Ahmet Yilmaz' veya 'Kartal' kod adıyla 3 farklı istihbarat raporunda geçiyor. "
        "Gaziantep yerel basınında 'sınır bölgesinde silah kaçakçılığı operasyonu' haberleri hedefin "
        "faaliyet alanı ile örtüşüyor. Suriye kaynaklı haberler Kilis hattında artan kaçakçılık "
        "aktivitesini doğruluyor. Medya ilgisi düşük — hedef kamuoyunda tanınmıyor."
    ),
    "media_sentiment": "negative",

    "public_statements_json": [
        {
            "date": "2026-03-10",
            "statement": "Malzeme hazır, yarın yola çıkıyorum",
            "context": "Telefon dinleme — İstanbul'dan bilinmeyen numaraya",
            "source": "SIGINT — Telefon dinleme kaydı"
        },
        {
            "date": "2026-03-11",
            "statement": "Ankara'dayım, Kilis'e geçiş için araç lazım",
            "context": "Telefon dinleme — 'Abu Tarek' kod adıyla Suriye teması",
            "source": "SIGINT — Telefon dinleme kaydı"
        },
        {
            "date": "2026-03-08",
            "statement": "Boğa'nın adamları Antep'te sorun çıkarıyor, dikkatli ol",
            "context": "Hasan Kaya'ya kurye ile iletilen mesaj (muhbir bilgisi)",
            "source": "HUMINT — Muhbir raporu"
        },
    ],

    # ── Overall ──
    "overall_threat_level": "high",
    "analyst_assessment": (
        "Hedef, Güneydoğu Anadolu hattında aktif bir silah kaçakçılığı ağının kilit figürü. "
        "Operasyonel disiplini yüksek ancak teknik güvenlik bilgisi zayıf (IMEI değişmiyor). "
        "En büyük kırılganlık noktaları: (1) anne ziyaret rutini, (2) Volkov'a tedarik bağımlılığı, "
        "(3) IMEI takip edilebilirliği. Yakalama operasyonu için önerilen strateji: "
        "Bolu Tüneli veya Ankara Ulus deposunda kontrollü operasyon. Gaziantep/Kilis bölgesinde "
        "operasyon riskli — yerel destek ağı güçlü ve kaçış rotaları çok."
    ),
    "reliability_score": 0.78,
    "last_updated": NOW,
}


def seed_profile():
    db = SessionLocal()
    try:
        # Find Ahmet Yilmaz
        person = db.query(Person).filter(Person.name_normalized == "ahmet yilmaz").first()
        if not person:
            print("[!] Ahmet Yilmaz not found. Run seed_surveillance.py first.")
            return

        # Delete existing analysis
        existing = db.query(PersonProfileAnalysis).filter(
            PersonProfileAnalysis.person_id == person.id
        ).first()
        if existing:
            db.delete(existing)
            db.commit()
            print(f"[!] Deleted existing analysis for person_id={person.id}")

        # Create new analysis
        analysis = PersonProfileAnalysis(person_id=person.id, **AHMET_PROFILE)
        db.add(analysis)
        db.commit()

        print(f"[+] Profile analysis created for: {person.name} (id={person.id})")
        print(f"    Personality: {analysis.personality_type}")
        print(f"    Stress: {analysis.stress_level}")
        print(f"    Strengths: {len(analysis.strengths_json)}")
        print(f"    Weaknesses: {len(analysis.weaknesses_json)}")
        print(f"    Habits: {len(analysis.habits_json)}")
        print(f"    Key contacts: {len(analysis.key_contacts_json)}")
        print(f"    Predictions: {len(analysis.predictions_json)}")
        print(f"    Threat level: {analysis.overall_threat_level}")
        print(f"    Reliability: {analysis.reliability_score}")

    except Exception as e:
        db.rollback()
        print(f"[!] Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_profile()
