"""
HUMINT Module Seed Data — Realistic test data for demonstration.
Run: python seed_humint.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timezone, timedelta
from db.engine import SessionLocal, init_db
from db.models import (
    HumintSource, HumintHandler, DebriefingReport,
    IntelligenceRequirement, RequirementResponse,
)
from db.compat import make_point


def utcnow():
    return datetime.now(timezone.utc)


def seed():
    init_db()
    db = SessionLocal()

    # Check if already seeded
    if db.query(HumintHandler).count() > 0:
        print("HUMINT data already seeded. Skipping.")
        db.close()
        return

    print("Seeding HUMINT data...")

    # ── HANDLERS ──
    handlers = [
        HumintHandler(
            callsign="KARTAL-1",
            real_name="Mehmet Yılmaz",
            rank="Binbaşı",
            unit="MİT Operasyon",
            specialization="Terörle mücadele",
            max_sources=5,
        ),
        HumintHandler(
            callsign="KONTROL-3",
            real_name="Ayşe Demir",
            rank="Yüzbaşı",
            unit="İstihbarat Dairesi",
            specialization="Sınır güvenliği",
            max_sources=4,
        ),
        HumintHandler(
            callsign="BOZKURT-7",
            real_name="Ahmet Kaya",
            rank="Albay",
            unit="TSK İstihbarat",
            specialization="Askeri istihbarat",
            max_sources=6,
        ),
    ]
    db.add_all(handlers)
    db.flush()

    # ── SOURCES ──
    sources = [
        HumintSource(
            codename="GÖLGE-1",
            source_type="agent",
            nationality="SY",
            languages=["ar", "tr"],
            reliability_grade="B",
            credibility_grade="2",
            motivation="money",
            access_level="Suriye askeri lojistik",
            area_of_access="İdlib-Halep ikmal hatları",
            country="Syria",
            city="Idlib",
            operating_region="Kuzeybatı Suriye",
            status="active",
            risk_level="high",
            communication_method="encrypted_msg",
            handler_id=handlers[0].id,
            geom=make_point(36.63, 35.93),
            tags=["military", "logistics", "idlib"],
            intel_value_score=8.2,
            total_reports=15,
            confirmed_reports=11,
            failed_reports=1,
            last_contact_date=utcnow() - timedelta(days=3),
        ),
        HumintSource(
            codename="ATLAS-3",
            source_type="asset",
            nationality="IQ",
            languages=["ar", "ku", "en"],
            reliability_grade="A",
            credibility_grade="1",
            motivation="ideology",
            access_level="Irak Kürt bölgesi siyasi çevreler",
            area_of_access="Erbil-Süleymaniye siyasi ağ",
            country="Iraq",
            city="Erbil",
            operating_region="Kuzey Irak / KRG",
            status="active",
            risk_level="medium",
            communication_method="face_to_face",
            handler_id=handlers[1].id,
            geom=make_point(44.01, 36.19),
            tags=["politics", "kurdish", "oil"],
            intel_value_score=9.1,
            total_reports=28,
            confirmed_reports=25,
            failed_reports=0,
            last_contact_date=utcnow() - timedelta(days=1),
        ),
        HumintSource(
            codename="FIRTINA-5",
            source_type="walk-in",
            nationality="IR",
            languages=["fa", "ar", "en"],
            reliability_grade="C",
            credibility_grade="3",
            motivation="revenge",
            access_level="İran Devrim Muhafızları alt kademe",
            area_of_access="IRGC Kudüs Gücü Suriye operasyonları",
            country="Turkey",
            city="Van",
            operating_region="Doğu Türkiye / Batı İran",
            status="active",
            risk_level="critical",
            communication_method="dead_drop",
            handler_id=handlers[2].id,
            geom=make_point(43.38, 38.49),
            tags=["iran", "irgc", "proxy"],
            intel_value_score=6.8,
            total_reports=7,
            confirmed_reports=4,
            failed_reports=2,
            last_contact_date=utcnow() - timedelta(days=10),
        ),
        HumintSource(
            codename="RÜZGAR-2",
            source_type="defector",
            nationality="SY",
            languages=["ar", "ru"],
            reliability_grade="B",
            credibility_grade="2",
            motivation="ideology",
            access_level="Suriye rejimi askeri iletişim",
            area_of_access="Şam askeri karargahı",
            country="Turkey",
            city="Hatay",
            operating_region="Güney Türkiye",
            status="dormant",
            risk_level="medium",
            communication_method="encrypted_msg",
            handler_id=handlers[0].id,
            geom=make_point(36.16, 36.20),
            tags=["syria", "regime", "military", "comms"],
            intel_value_score=7.0,
            total_reports=12,
            confirmed_reports=9,
            failed_reports=1,
            last_contact_date=utcnow() - timedelta(days=45),
        ),
        HumintSource(
            codename="PUSULA-9",
            source_type="freelancer",
            nationality="LB",
            languages=["ar", "fr", "en"],
            reliability_grade="D",
            credibility_grade="4",
            motivation="money",
            access_level="Lübnan Hizbullah dış çevre",
            area_of_access="Bekaa Vadisi silah kaçakçılığı",
            country="Lebanon",
            city="Baalbek",
            operating_region="Lübnan / Güney Suriye",
            status="active",
            risk_level="high",
            communication_method="phone",
            handler_id=handlers[2].id,
            geom=make_point(36.21, 34.01),
            tags=["hezbollah", "weapons", "smuggling"],
            intel_value_score=4.5,
            total_reports=5,
            confirmed_reports=1,
            failed_reports=3,
            last_contact_date=utcnow() - timedelta(days=20),
        ),
    ]
    db.add_all(sources)
    db.flush()

    # ── DEBRIEFINGS ──
    debriefings = [
        DebriefingReport(
            source_id=sources[0].id,
            handler_id=handlers[0].id,
            debriefing_date=utcnow() - timedelta(days=3),
            duration_minutes=45,
            debriefing_type="scheduled",
            title="İdlib M4 karayolu konvoy hareketliliği",
            raw_narrative="""Kaynak, son bir hafta içinde M4 karayolu üzerinden günde ortalama 4-5 askeri konvoy geçişi gözlemlediğini bildirdi.
Konvoylar genellikle gece saatlerinde (02:00-04:00) hareket ediyor. Araçların çoğu zırhlı personel taşıyıcı (BTR-80) ve mühimmat kamyonu.
Kaynak, konvoyların Lazkiye limanından geldiğini ve İdlib güneyine yönlendirildiğini değerlendirmektedir.
Ayrıca son konvoyda Rusya plakalı araçlar gözlemlenmiş.""",
            analyst_summary="M4 üzerinde artan askeri lojistik, olası operasyon hazırlığına işaret.",
            persons_mentioned=[
                {"name": "General Suheil al-Hassan", "role": "Tiger Forces Komutanı", "context": "Konvoy yönlendirmesi"},
            ],
            locations_mentioned=[
                {"name": "M4 Karayolu", "country": "Syria", "context": "Konvoy güzergahı"},
                {"name": "Lazkiye Limanı", "country": "Syria", "context": "İkmal kaynağı"},
            ],
            threats_identified=[
                {"type": "military_buildup", "target": "İdlib güneyi", "probability": "high", "timeframe": "2-4 hafta", "details": "Olası kara operasyonu"},
            ],
            information_grade="B2",
            source_demeanor="cooperative",
            consistency_with_previous="consistent",
            corroboration_status="partially_corroborated",
            priority="urgent",
            category="military",
            classification="secret",
            country="Turkey",
            city="Hatay",
            geom=make_point(36.16, 36.20),
            is_parsed=True,
        ),
        DebriefingReport(
            source_id=sources[1].id,
            handler_id=handlers[1].id,
            debriefing_date=utcnow() - timedelta(days=1),
            duration_minutes=90,
            debriefing_type="scheduled",
            title="KRG petrol ihracat anlaşması güncellemesi",
            raw_narrative="""Kaynak, KRG hükümetinin Bağdat ile yeni petrol geliri paylaşım müzakerelerinin
çıkmaza girdiğini bildirdi. KRG Başbakanı'nın özel danışmanından aldığı bilgiye göre,
Bağdat günlük 400.000 varil üzerinden %17 pay teklif ederken, KRG %20 talep ediyor.
Müzakereler Nisan ortasına kadar sonuçlanmazsa, KRG bağımsız ihracata dönmeyi planlıyor.
Bu durum Türkiye'nin Ceyhan boru hattı politikasını doğrudan etkileyecek.""",
            analyst_summary="KRG-Bağdat petrol müzakeresi kritik eşikte. Türkiye enerji güvenliği etkisi var.",
            persons_mentioned=[
                {"name": "Mesrur Barzani", "role": "KRG Başbakanı", "context": "Müzakere yetkilendirmesi"},
                {"name": "Danışman X", "role": "KRG Başbakanlık Danışmanı", "context": "Bilgi kaynağı"},
            ],
            organizations_mentioned=[
                {"name": "KRG", "type": "government", "context": "Petrol müzakere tarafı"},
                {"name": "Irak Federal Hükümeti", "type": "government", "context": "Müzakere tarafı"},
            ],
            threats_identified=[
                {"type": "economic", "target": "Ceyhan boru hattı", "probability": "medium", "timeframe": "1-3 ay", "details": "Petrol akış kesintisi riski"},
            ],
            information_grade="A1",
            source_demeanor="matter-of-fact",
            consistency_with_previous="consistent",
            corroboration_status="corroborated",
            priority="important",
            category="economic",
            classification="confidential",
            country="Iraq",
            city="Erbil",
            geom=make_point(44.01, 36.19),
            is_parsed=True,
        ),
        DebriefingReport(
            source_id=sources[2].id,
            handler_id=handlers[2].id,
            debriefing_date=utcnow() - timedelta(days=10),
            duration_minutes=60,
            debriefing_type="emergency",
            title="IRGC Kudüs Gücü Suriye takviye bilgisi",
            raw_narrative="""Kaynak acil temas kurarak, IRGC Kudüs Gücü'nün Suriye'deki varlığını
artırmak için yeni bir birlik rotasyonu planladığını bildirdi. Tahran'dan Şam'a
2 hafta içinde yaklaşık 500 personel transferi bekleniyor.
Transfer Bağdat üzerinden kara yoluyla yapılacak. Kaynak, birliklerin
Deir ez-Zor ve Bukamal bölgesine konuşlanacağını değerlendirmektedir.
Bilginin kaynağı, IRGC lojistik birimindeki eski bir meslektaşı.""",
            information_grade="C3",
            source_demeanor="nervous",
            consistency_with_previous="new_topic",
            corroboration_status="unverified",
            priority="flash",
            category="military",
            classification="top_secret",
            country="Turkey",
            city="Van",
            geom=make_point(43.38, 38.49),
            follow_up_needed=True,
            follow_up_questions=[
                {"question": "Transfer tarihi kesinleşti mi?", "priority": "high", "context": "Zamanlama doğrulaması"},
                {"question": "Birlik tipi nedir? Piyade mi, özel kuvvet mi?", "priority": "medium", "context": "Tehdit değerlendirmesi"},
            ],
            is_parsed=True,
        ),
    ]
    db.add_all(debriefings)
    db.flush()

    # ── INTELLIGENCE REQUIREMENTS ──
    pir1 = IntelligenceRequirement(
        requirement_type="PIR",
        serial_number="PIR-001",
        title="Suriye kuzeybatısında Rus-Suriye askeri operasyon niyeti",
        description="Rusya ve Suriye rejim güçlerinin İdlib bölgesinde planlanan askeri operasyonların kapsamı, zamanlaması ve hedefleri nelerdir?",
        justification="Türkiye sınır güvenliği ve mülteci akını riski açısından kritik",
        priority="critical",
        status="partially_answered",
        satisfaction_level=0.35,
        geographic_focus="İdlib, Suriye",
        topic_category="military",
        requested_by="Genelkurmay İstihbarat Başkanlığı",
        deadline=utcnow() + timedelta(days=14),
        collection_sources=["HUMINT", "SIGINT", "IMINT"],
        indicators=["Askeri konvoy artışı", "Hava üssü aktivitesi", "Sivil tahliye"],
        keywords=["İdlib", "operasyon", "Rusya", "Tiger Forces"],
        geom=make_point(36.63, 35.93),
        response_count=2,
    )

    pir2 = IntelligenceRequirement(
        requirement_type="PIR",
        serial_number="PIR-002",
        title="İran'ın Suriye'deki askeri varlık genişletme planları",
        description="IRGC Kudüs Gücü'nün Suriye'deki kuvvet yapısı, konuşlanma noktaları ve genişleme planları nelerdir?",
        priority="urgent",
        status="active",
        satisfaction_level=0.15,
        geographic_focus="Suriye (Deir ez-Zor, Bukamal, Şam)",
        topic_category="military",
        requested_by="MİT",
        collection_sources=["HUMINT", "SIGINT"],
        keywords=["IRGC", "Kudüs Gücü", "Suriye", "İran"],
        geom=make_point(40.34, 34.45),
        response_count=1,
    )

    pir3 = IntelligenceRequirement(
        requirement_type="PIR",
        serial_number="PIR-003",
        title="KRG enerji politikası ve Türkiye etkisi",
        description="KRG'nin petrol ihracat stratejisi Türkiye'nin enerji güvenliğini nasıl etkileyecek?",
        priority="important",
        status="partially_answered",
        satisfaction_level=0.55,
        geographic_focus="Kuzey Irak, Ceyhan",
        topic_category="economic",
        requested_by="Enerji Bakanlığı",
        collection_sources=["HUMINT", "OSINT"],
        keywords=["KRG", "petrol", "Ceyhan", "boru hattı"],
        geom=make_point(44.01, 36.19),
        response_count=3,
    )

    db.add_all([pir1, pir2, pir3])
    db.flush()

    # EEIs under PIR-001
    eeis = [
        IntelligenceRequirement(
            requirement_type="EEI",
            serial_number="PIR-001-A",
            title="M4 karayolu üzerindeki lojistik hareketlilik düzeyi",
            description="M4 üzerinden günlük konvoy sayısı, içeriği ve yönü nedir?",
            parent_id=pir1.id,
            priority="urgent",
            status="partially_answered",
            satisfaction_level=0.6,
            topic_category="military",
            response_count=1,
        ),
        IntelligenceRequirement(
            requirement_type="EEI",
            serial_number="PIR-001-B",
            title="Hmeymim hava üssü uçuş aktivitesi",
            description="Hmeymim'den günlük sorti sayısı ve hedef bölgeler nelerdir?",
            parent_id=pir1.id,
            priority="urgent",
            status="active",
            satisfaction_level=0.1,
            topic_category="military",
            response_count=0,
        ),
    ]
    db.add_all(eeis)
    db.flush()

    # ── RESPONSES ──
    responses = [
        RequirementResponse(
            requirement_id=pir1.id,
            debriefing_id=debriefings[0].id,
            source_type="humint",
            answer_text="M4 üzerinde günde 4-5 konvoy, gece hareketi, BTR-80 ve mühimmat. Lazkiye'den İdlib güneyine.",
            confidence=0.75,
            information_grade="B2",
            satisfaction_delta=0.25,
            is_key_finding=True,
        ),
        RequirementResponse(
            requirement_id=pir2.id,
            debriefing_id=debriefings[2].id,
            source_type="humint",
            answer_text="500 personel takviyesi, 2 hafta içinde, Bağdat üzerinden. Deir ez-Zor/Bukamal bölgesi.",
            confidence=0.5,
            information_grade="C3",
            satisfaction_delta=0.15,
        ),
        RequirementResponse(
            requirement_id=pir3.id,
            debriefing_id=debriefings[1].id,
            source_type="humint",
            answer_text="Bağdat %17, KRG %20 talep ediyor. Nisan ortası deadline. Başarısız olursa bağımsız ihracat.",
            confidence=0.9,
            information_grade="A1",
            satisfaction_delta=0.35,
            is_key_finding=True,
        ),
    ]
    db.add_all(responses)

    db.commit()
    db.close()

    print(f"  [OK] {len(handlers)} handler")
    print(f"  [OK] {len(sources)} source")
    print(f"  [OK] {len(debriefings)} debriefing")
    print(f"  [OK] 3 PIR + {len(eeis)} EEI")
    print(f"  [OK] {len(responses)} response")
    print("HUMINT seed complete!")


if __name__ == "__main__":
    seed()
