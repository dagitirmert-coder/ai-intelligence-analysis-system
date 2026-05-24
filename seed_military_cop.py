# -*- coding: utf-8 -*-
"""
Askeri COP Örnek Veri Yükleyici — Operasyon GÜVENLI SINIR
==========================================================
Senaryo: Güneydoğu bölgesinde hayali bir sınır güvenlik operasyonu.
- Dost: KILINÇ Tugayı unsurları savunmada
- Düşman: KUZEY BİRLİĞİ (KBR) grubunun kuzeyde baskı yapması
- Bilinmeyen: Sınır bölgesinde tanımlanamayan unsurlar

Çalıştırma: python -X utf8 seed_military_cop.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timezone, timedelta
from db.engine import SessionLocal, engine, init_db
from db.models import (
    TacticalUnit, TacticalPosition, TacticalReport, TacticalAssessment
)

def utc(h_offset=0):
    """Returns current UTC minus h_offset hours."""
    return datetime.now(timezone.utc) - timedelta(hours=h_offset)

def main():
    print("=" * 60)
    print("  Operasyon GÜVENLI SINIR — COP Örnek Veri Yükleyici")
    print("=" * 60)

    init_db()
    db = SessionLocal()

    try:
        # ── Mevcut verileri temizle ──────────────────────────────
        print("\n[1/5] Mevcut askeri veriler temizleniyor...")
        db.query(TacticalAssessment).delete()
        db.query(TacticalPosition).delete()
        db.query(TacticalReport).delete()
        db.query(TacticalUnit).delete()
        db.commit()
        print("      Temizlendi.")

        # ════════════════════════════════════════════════════════
        # [2/5] DOST KUVVETLERİ (KILINÇ Tugayı)
        # ════════════════════════════════════════════════════════
        print("\n[2/5] Dost kuvvetler olusturuluyor...")

        friendly_units = [
            TacticalUnit(
                unit_id="KILINC-1",
                name="KILINÇ-1 / 3. Piyade Bolugu",
                side="friendly",
                unit_type="infantry",
                lat=37.1854, lng=40.7312,
                strength_personnel=145,
                strength_confidence=0.92,
                equipment_json={"apcs": 4, "vehicles": 8, "mortars": 2},
                weapons_json=["HK33", "M249 SAW", "RPG-7", "81mm Havan"],
                status="defensive",
                heading_deg=5,
                activity="Kızıltepe Sırtı'nı savunuyor, mevzi tahkim ediyor",
                commander="Üsteğmen Aydın",
                parent_unit="KILINÇ Tugayı / 1. Tabur",
                needs_json=["ammunition_low", "medical_resupply"],
                threat_level="medium",
                notes="Son 2 saattir küçük ateş temastı var. Kuzey yaklaşımı gözaltında.",
                source_count=3,
                first_seen=utc(6),
            ),
            TacticalUnit(
                unit_id="KILINC-2",
                name="KILINÇ-2 / Zırhlı Müfreze",
                side="friendly",
                unit_type="armor",
                lat=37.2105, lng=40.8045,
                strength_personnel=42,
                strength_confidence=0.98,
                equipment_json={"tanks": 3, "apcs": 2, "vehicles": 5},
                weapons_json=["M60T Sabra", "M2HB .50 Cal", "M60 Makinalı"],
                status="advancing",
                heading_deg=195,
                speed_kmh=18.0,
                activity="KILINÇ-1 destek için güneye ilerliyor, ETA 35 dk",
                commander="Yüzbaşı Demir",
                parent_unit="KILINÇ Tugayı / Zırhlı Destek Bölüğü",
                needs_json=["fuel_50pct"],
                threat_level="low",
                notes="M60T'ler tam operasyonel. Fuel %50 ile devam ediyor.",
                source_count=2,
                first_seen=utc(4),
            ),
            TacticalUnit(
                unit_id="KILINC-ART",
                name="KILINÇ-ART / Topçu Bataryası",
                side="friendly",
                unit_type="artillery",
                lat=37.2640, lng=40.8790,
                strength_personnel=68,
                strength_confidence=0.99,
                equipment_json={"artillery": 2, "vehicles": 6},
                weapons_json=["T-155 Fırtına", "120mm Havan"],
                status="active",
                heading_deg=0,
                activity="Ateş destek pozisyonunda, KILINÇ-1 çağrısı bekliyor",
                commander="Binbaşı Karahan",
                parent_unit="KILINÇ Tugayı / Ateş Destek Grubu",
                needs_json=[],
                threat_level="low",
                notes="2x T-155 Fırtına SPH hazır. Fire mission #4 ve #7 koordine edildi.",
                source_count=2,
                first_seen=utc(8),
            ),
            TacticalUnit(
                unit_id="KILINC-LOG",
                name="KILINÇ-LOG / İkmal Birliği",
                side="friendly",
                unit_type="logistics",
                lat=37.3120, lng=40.9240,
                strength_personnel=28,
                strength_confidence=0.95,
                equipment_json={"vehicles": 12, "fuel_trucks": 3},
                weapons_json=["G3", "HK33"],
                status="active",
                heading_deg=0,
                activity="İkmal deposunda bekliyor, ön hat transferi için güvenli koridor gerekli",
                commander="Astsubay Yılmaz",
                parent_unit="KILINÇ Tugayı / Lojistik Bölüğü",
                needs_json=["escort_required", "route_clearance"],
                threat_level="medium",
                notes="KILINÇ-1'e teslim edilecek: 20.000 mermi 5.56, 500 RPG roketi, 3 ton yakıt.",
                source_count=1,
                first_seen=utc(3),
            ),
            TacticalUnit(
                unit_id="KILINC-RECON",
                name="KILINÇ-RECON / Keşif Timi",
                side="friendly",
                unit_type="recon",
                lat=37.1530, lng=40.6870,
                strength_personnel=8,
                strength_confidence=1.0,
                equipment_json={"vehicles": 2},
                weapons_json=["MSG90 Keskin Nişancı", "MP5SD", "Termal Kamera"],
                status="active",
                heading_deg=340,
                activity="OPFOR-ALPHA hareketini takip ediyor, ön gözlem noktasında",
                commander="Üsteğmen Çelik",
                parent_unit="KILINÇ Tugayı / Keşif Bölüğü",
                needs_json=[],
                threat_level="high",
                notes="Kritik noktada. OPFOR-ALPHA ile 2.4 km mesafede. Taktik sessizlik.",
                source_count=4,
                first_seen=utc(5),
            ),
        ]

        for u in friendly_units:
            u.last_updated = datetime.now(timezone.utc)
            u.created_at = datetime.now(timezone.utc)
            db.add(u)

        db.flush()
        print(f"      {len(friendly_units)} dost birlik olusturuldu.")

        # ════════════════════════════════════════════════════════
        # [3/5] DÜŞMAN KUVVETLERİ (KBR — Kuzey Birliği)
        # ════════════════════════════════════════════════════════
        print("\n[3/5] Dusman kuvvetler olusturuluyor...")

        enemy_units = [
            TacticalUnit(
                unit_id="KBR-ALFA",
                name="KBR ALFA / Piyade Taburu",
                side="enemy",
                unit_type="infantry",
                lat=37.0890, lng=40.7020,
                strength_personnel=280,
                strength_confidence=0.70,
                equipment_json={"apcs": 8, "vehicles": 22, "mortars": 4, "heavy_mg": 6},
                weapons_json=["AK-74M", "RPK-74", "PKM", "RPG-29", "82mm Havan", "ATGM Kornet"],
                status="advancing",
                heading_deg=175,
                speed_kmh=4.5,
                activity="Güneye doğru ilerliyor, Kızıltepe Sırtı'na baskı yapıyor",
                commander="Bilinmiyor / 'Komutan Emir' lakaplı",
                parent_unit="KBR Ana Kuvveti",
                needs_json=[],
                threat_level="high",
                notes="En az 3 ayrı rapor teyit ediyor. KILINÇ-1 ile çatışma ihtimali yüksek.",
                source_count=4,
                first_seen=utc(5),
            ),
            TacticalUnit(
                unit_id="KBR-BRAVO",
                name="KBR BRAVO / Zırhlı Müfreze",
                side="enemy",
                unit_type="armor",
                lat=37.0650, lng=40.8450,
                strength_personnel=45,
                strength_confidence=0.75,
                equipment_json={"tanks": 6, "apcs": 4, "vehicles": 8},
                weapons_json=["T-72B", "BMP-2", "ZU-23-2", "9M133 Kornet"],
                status="advancing",
                heading_deg=220,
                speed_kmh=12.0,
                activity="Güneybatıya çark ederek sol kanattan kuşatma hareketi yapıyor",
                commander="Bilinmiyor",
                parent_unit="KBR Zırhlı Kolu",
                needs_json=[],
                threat_level="critical",
                notes="6 adet T-72B TESPİT EDİLDİ. Sol kanattan çevirme hareketi KILINÇ-1 için kritik tehdit!",
                source_count=3,
                first_seen=utc(3),
            ),
            TacticalUnit(
                unit_id="KBR-CHARLIE",
                name="KBR CHARLIE / Topçu Grubu",
                side="enemy",
                unit_type="artillery",
                lat=37.0280, lng=40.6550,
                strength_personnel=55,
                strength_confidence=0.60,
                equipment_json={"artillery": 4, "vehicles": 10},
                weapons_json=["D-30 122mm Obüs", "BM-21 Grad (tahmini)", "82mm Havan"],
                status="active",
                heading_deg=0,
                activity="Sabit ateş pozisyonunda, KBR-ALFA hareketine topçu desteği veriyor",
                commander="Bilinmiyor",
                parent_unit="KBR Ateş Destek Birimi",
                needs_json=[],
                threat_level="high",
                notes="SIGINT: 122mm faaliyeti tespit edildi. Koordinat belirsizliği +-1.5 km.",
                source_count=2,
                first_seen=utc(4),
            ),
            TacticalUnit(
                unit_id="KBR-DELTA",
                name="KBR DELTA / Sızma Timi",
                side="enemy",
                unit_type="special_forces",
                lat=37.1420, lng=40.9150,
                strength_personnel=14,
                strength_confidence=0.45,
                equipment_json={"vehicles": 2},
                weapons_json=["VSS Vintorez", "AS Val", "RPG-18", "C4 Patlayıcı"],
                status="active",
                heading_deg=270,
                activity="KILINÇ-ART'ın doğusundan batıya sızıyor, sabotaj ihtimali var",
                commander="Bilinmiyor",
                parent_unit="KBR İstihbarat/Özel Hareket Birimi",
                needs_json=[],
                threat_level="critical",
                notes="HUMINT: Topçu mevzilerini hedef almak üzere küçük tim kuzeybatı yaklaşımından geliyor.",
                source_count=2,
                first_seen=utc(2),
            ),
            TacticalUnit(
                unit_id="KBR-ECHO",
                name="KBR ECHO / İkmal Konvoyu",
                side="enemy",
                unit_type="logistics",
                lat=36.9870, lng=40.5920,
                strength_personnel=22,
                strength_confidence=0.55,
                equipment_json={"vehicles": 9, "trucks": 6},
                weapons_json=["AK-74M", "DShK 12.7mm"],
                status="active",
                heading_deg=15,
                activity="Kuzeyde KBR ana üssünden cephane ve yakıt getiriyor, kuzeye doğru seyrediyor",
                commander="Bilinmiyor",
                parent_unit="KBR Lojistik Birimleri",
                needs_json=[],
                threat_level="medium",
                notes="Konvoy kesilirse KBR-ALFA ve KBR-BRAVO'nun lojistiği 8-12 saatte tükenir.",
                source_count=2,
                first_seen=utc(3),
            ),
        ]

        for u in enemy_units:
            u.last_updated = datetime.now(timezone.utc)
            u.created_at = datetime.now(timezone.utc)
            db.add(u)

        db.flush()
        print(f"      {len(enemy_units)} dusman birlik olusturuldu.")

        # ── Bilinmeyenler ────────────────────────────────────────
        unknown_units = [
            TacticalUnit(
                unit_id="UNKNOWN-01",
                name="BİLİNMEYEN-01 / Araç Kolonu",
                side="unknown",
                unit_type="combined",
                lat=37.2200, lng=41.0450,
                strength_personnel=None,
                strength_confidence=0.30,
                equipment_json={"vehicles": 5},
                weapons_json=[],
                status="active",
                heading_deg=270,
                activity="Doğudan batıya hareket eden 5 araçlık kolon, tanımlanamadı",
                notes="Drone görüntüsünde tespit. Taraf teyidi için yakın keşif gerekli.",
                threat_level="medium",
                source_count=1,
                first_seen=utc(1),
            ),
            TacticalUnit(
                unit_id="UNKNOWN-02",
                name="BİLİNMEYEN-02 / Ayak İzi Grubu",
                side="unknown",
                unit_type="infantry",
                lat=37.1050, lng=40.6320,
                strength_personnel=20,
                strength_confidence=0.40,
                equipment_json={},
                weapons_json=[],
                status="active",
                heading_deg=90,
                activity="20-30 kişilik yaya grup, batıdan doğuya geçiş yapıyor",
                notes="Termal görüntüleme ile tespit. Silah taşıyıp taşımadığı belirsiz.",
                threat_level="medium",
                source_count=1,
                first_seen=utc(2),
            ),
        ]

        for u in unknown_units:
            u.last_updated = datetime.now(timezone.utc)
            u.created_at = datetime.now(timezone.utc)
            db.add(u)

        db.flush()
        print(f"      {len(unknown_units)} bilinmeyen birlik olusturuldu.")

        # ════════════════════════════════════════════════════════
        # Pozisyon Geçmişi (hareket izleri)
        # ════════════════════════════════════════════════════════
        all_units = db.query(TacticalUnit).all()
        uid_map = {u.unit_id: u.id for u in all_units}

        position_tracks = {
            # KILINC-1: savunma mevzisine çekildi
            "KILINC-1": [
                (37.2010, 40.7050, 6, 185, "İleri karakol noktasında, keşif"),
                (37.1980, 40.7180, 5, 180, "Geri çekilme hareketi başladı"),
                (37.1920, 40.7240, 4, 175, "Ara mevzide yeniden konuşlanma"),
                (37.1854, 40.7312, 0, 5, "Kiziltepe Sirti savunma mevzisi — aktif"),
            ],
            # KILINC-2: konuşlanma bölgesinden destek için güneye
            "KILINC-2": [
                (37.3240, 40.8120, 5, 195, "Konuşlanma bölgesi, beklemede"),
                (37.2870, 40.8090, 3, 195, "Hareket emri alındı, güneye"),
                (37.2560, 40.8060, 2, 192, "M60T kolonu ilerliyor"),
                (37.2105, 40.8045, 0, 195, "Destek pozisyonuna yaklaşıyor — ETA 35dk"),
            ],
            # KBR-ALFA: kuzeyde toplanıp güneye akıyor
            "KBR-ALFA": [
                (36.9450, 40.6980, 6, 185, "Kuzey toplanma alanından hareket"),
                (37.0120, 40.7000, 5, 180, "Hız artırıldı, baskı başladı"),
                (37.0540, 40.7010, 3, 178, "Hafif çatışma, devam ediyor"),
                (37.0890, 40.7020, 0, 175, "KILINC-1 mevzine 9 km, yaklaşıyor"),
            ],
            # KBR-BRAVO: doğudan çark hareketi
            "KBR-BRAVO": [
                (36.9200, 40.9800, 5, 270, "Doğu kolunda bekliyor"),
                (36.9580, 40.9200, 4, 250, "Çevreleme harekatı başladı"),
                (37.0180, 40.8850, 3, 230, "T-72'ler sert arazide ilerliyor"),
                (37.0650, 40.8450, 0, 220, "Sol kanat cephe çevirmesi — KRİTİK"),
            ],
            # KBR-CHARLIE: sabit topçu pozisyonu
            "KBR-CHARLIE": [
                (37.0180, 40.6500, 5, 0, "İlk ateş pozisyonu kuruldu"),
                (37.0250, 40.6520, 3, 0, "Ateş desteği sağlıyor, aktif"),
                (37.0280, 40.6550, 0, 0, "4x D-30 ateş hazır konumda"),
            ],
            # KBR-DELTA: doğudan sızma
            "KBR-DELTA": [
                (37.1980, 41.0500, 4, 270, "Doğuda sızma başlangıcı"),
                (37.1720, 40.9850, 3, 270, "Doğu yaklaşımından ilerliyor"),
                (37.1420, 40.9150, 0, 270, "KILINC-ART bölgesine yaklaşıyor"),
            ],
            # KILINC-RECON: ileri gözlem noktasına
            "KILINC-RECON": [
                (37.1820, 40.6680, 5, 340, "Keşif patrolu başladı"),
                (37.1640, 40.6760, 4, 335, "KBR-ALFA'yı tespit etti, raporlandı"),
                (37.1530, 40.6870, 0, 340, "İleri gözlem noktasında, sessiz takip"),
            ],
            # KBR-ECHO: kuzeyden ikmal
            "KBR-ECHO": [
                (36.9120, 40.5700, 5, 15, "Kuzey ikmal deposundan yola çıktı"),
                (36.9500, 40.5800, 3, 15, "Sınır hattını geçiyor"),
                (36.9870, 40.5920, 0, 15, "KBR-ALFA'ya yaklaşıyor"),
            ],
            # UNKNOWN-01: doğudan batıya hareket
            "UNKNOWN-01": [
                (37.2200, 41.1500, 2, 270, "Doğuda tespit, batıya yöneldi"),
                (37.2200, 41.0450, 0, 270, "Hareket devam ediyor, teyit bekleniyor"),
            ],
        }

        pos_count = 0
        for uid, track in position_tracks.items():
            unit_fk = uid_map.get(uid)
            if not unit_fk:
                continue
            for lat, lng, h_offset, heading, activity in track:
                pos = TacticalPosition(
                    unit_id=unit_fk,
                    lat=lat, lng=lng,
                    heading_deg=heading,
                    timestamp=utc(h_offset),
                    source="report",
                    accuracy_m=200,
                    activity=activity,
                )
                db.add(pos)
                pos_count += 1

        db.flush()
        print(f"      {pos_count} pozisyon gecmisi olusturuldu.")

        # ════════════════════════════════════════════════════════
        # [4/5] SAHA RAPORLARI
        # ════════════════════════════════════════════════════════
        print("\n[4/5] Saha raporlari olusturuluyor...")

        reports = [
            TacticalReport(
                title="SPOTREP-001 / İlk Temas Raporu — KBR-ALFA",
                raw_text="""SPOTREP — GİZLİ
TARİH/SAAT: {t5}
RAPORLAYAN: KILINÇ-RECON / Üsteğmen Çelik

BOYUT: Tahminen 250-300 piyade, 8 zırhlı, 20+ araç.
FAALİYET: Güneye doğru düzenli ilerleme, bölük düzeninde.
KONUM: Kızıltepe Sırtı'nın 9 km kuzeyinde, koordinat 37.0890°N 40.7020°E
BİRLİK: KBR Ana Kuvveti renk sembolleri ve taktik düzeni gözlemlendi.
ZAMAN: 05:45 yerel saat
TEÇHİZAT: AK-74, RPK, PKM, RPG-29, BMP tipi araçlar, 82mm havan.

YORUM: Büyük piyade unsurunun organize ilerleme hareketi. Hız saatte ~4 km.
KILINÇ-1 mevziine ETA: yaklaşık 2.5 saat.
ÖNLEM: Topçu desteği (KILINÇ-ART) hazır tutulmalı. KILINÇ-2 hızlandırılmalı.
""".format(t5=utc(5).strftime("%Y-%m-%d %H:%M UTC")),
                source_type="humint",
                reporting_unit="KILINC-RECON",
                area_of_interest="Kızıltepe Sırtı Kuzey Yaklaşımı",
                reporter_lat=37.1530, reporter_lng=40.6870,
                report_time=utc(5),
                is_processed=True,
                units_extracted=1,
                parsed_summary="KILINC-RECON KBR-ALFA'yı (280+ personel, 8 zırhlı) güneye ilerlerken tespit etti. KILINÇ-1 mevziine ETA ~2.5 saat.",
            ),
            TacticalReport(
                title="SITREP-002 / Zırhlı Çevreleme Tespiti — KBR-BRAVO",
                raw_text="""SITREP — GİZLİ
TARİH/SAAT: {t3}
RAPORLAYAN: İHA Görüntüleme / KILINÇ Tugayı İstihbarat Subayı

DRONE GÖZLEM RAPORU:
Koordinat: 37.0650°N 40.8450°E
6 adet T-72B tankı güneybatı yönünde hareket ediyor.
4 adet BMP-2 ve 8 destek aracı eşlik ediyor.
Ortalama hız: saatte 12 km.

DURUM DEĞERLENDİRMESİ:
- Bu hareket KILINÇ-1'in sol (doğu) kanadını çevrelemek üzere tasarlanmış görünüyor.
- T-72B'ler aktif M60T'lere karşı önemli avantaj taşıyor.
- KILINÇ-1 mevzii 6-8 saat içinde çevrilebilir.

ACİL EYLEM GEREKLİ:
1. KILINÇ-2'nin güçlendirilmesi veya yeniden konuşlandırılması
2. KILINÇ-ART'ın T-72 kolonu üzerine hazırlık atışı
3. Hava destek talebi değerlendirilmeli

KILINÇ-LOG'un sevkiyat güzergahı güvensiz hale geldi.
""".format(t3=utc(3).strftime("%Y-%m-%d %H:%M UTC")),
                source_type="drone",
                reporting_unit="KILINC Tugayi Istihbarat",
                area_of_interest="Doğu Kanat / T-72 Çevreleme Rotası",
                reporter_lat=37.0650, reporter_lng=40.8450,
                report_time=utc(3),
                is_processed=True,
                units_extracted=1,
                parsed_summary="İHA gözlemi: 6x T-72B içeren KBR-BRAVO sol kanattan çevreleme manevrasında. KILINÇ-1 için kritik tehdit.",
            ),
            TacticalReport(
                title="SIGINT-003 / Topçu Aktivitesi — KBR-CHARLIE",
                raw_text="""SİGİNT RAPORU — ÇOK GİZLİ
TARİH/SAAT: {t4}
RAPORLAYAN: Elektronik İstihbarat Birimi

İNTERSEPT ÖZETİ:
37.0280°N 40.6550°E koordinatında 122mm aktivitesi tespit edildi.
RF emisyonları 4 ayrı ateş kontrol kanalına işaret ediyor.
Ses analizi: D-30 obüs harası karakteristiği.

TAHMİNİ DÜZEN:
- 4 x D-30 122mm Obüs (±2 hata payı)
- BM-21 Grad mevcudiyeti olası (sinyal imzası tespit edildi, teyit edilemedi)
- Personel: 50-60

ATIM MENZİLİ ANALİZİ:
Bu koordinattan D-30 (menzil: 15.4 km) KILINÇ-1, KILINÇ-2 ve KILINÇ-ART'ı kapsıyor.
BM-21 (menzil: 40 km) durumunda tüm KILINÇ operasyon bölgesi tehdit altında.

ÖNERİ: Öncelikli karşı batarya ateşi veya hava saldırısı değerlendirilmeli.
""".format(t4=utc(4).strftime("%Y-%m-%d %H:%M UTC")),
                source_type="sigint",
                reporting_unit="Elektronik Istihbarat Birimi",
                area_of_interest="KBR Topçu Pozisyonu / Güneybatı Bölgesi",
                report_time=utc(4),
                is_processed=True,
                units_extracted=1,
                parsed_summary="SİGİNT: 37.028°N 40.655°E'de 4x D-30 topçu pozisyonu teyit edildi. Tüm KILINÇ unsurları menzil dahilinde.",
            ),
            TacticalReport(
                title="LOGSTAT-004 / KILINÇ-1 Kritik İkmal Talebi",
                raw_text="""LOJİSTİK DURUM RAPORU (LOGSTAT)
TARİH/SAAT: {t2}
RAPORLAYAN: KILINÇ-1 / Üsteğmen Aydın

ACİL İHTİYAÇLAR:
1. CEPHANE (KRİTİK):
   - 5.56x45mm: Stok %15, mevcut çatışma hızıyla 6 saat
   - RPG Roketi: 14 adet kaldı
   - 81mm Havan Mühimmatı: 22 adet kaldı

2. TIBBİ (ORTA):
   - 3 yaralı (1 ağır, 2 hafif)
   - Tahliye helikopteri talep ediliyor (ağır yaralı için)
   - İlaç ve yara sargısı kritik

3. YAKLAŞIM GÜZERGAHI:
   KILINÇ-LOG ikmalini ön hatta iletemiyor. KBR-BRAVO'nun çevreleme
   hareketi nedeniyle doğu güzergahı kapalı. Batı güzergahı için
   keşif ve KILINÇ-2 eskortu gerekli.

ÖZET: 12 saat içinde ikmal ulaşmazsa mevzi tutma kapasitesi kritik seviyeye düşer.
""".format(t2=utc(2).strftime("%Y-%m-%d %H:%M UTC")),
                source_type="field_report",
                reporting_unit="KILINC-1",
                area_of_interest="Kızıltepe Sırtı Mevzii",
                reporter_lat=37.1854, reporter_lng=40.7312,
                report_time=utc(2),
                is_processed=True,
                units_extracted=1,
                parsed_summary="KILINÇ-1 kritik ikmal talebi: Cephane %15, 3 yaralı. 12 saat içinde ikmal ulaşmazsa mevzi tutma kapasitesi düşer.",
            ),
            TacticalReport(
                title="SPOTREP-005 / KBR-DELTA Sızma Timi Tespiti",
                raw_text="""SPOTREP — ÇOK GİZLİ / GECİKTİRİLMEMELİ
TARİH/SAAT: {t2}
RAPORLAYAN: HUMINT Kaynağı (Güvenilirlik: B2)

KAYNAK BİLGİSİ:
Güvenilir bir yerel kaynak, yaklaşık 12-15 kişilik silahlı grubun
KILINÇ-ART topçu mevzilerine yönelik sabotaj/saldırı hazırlığında
olduğunu bildiriyor.

KONUM: 37.1420°N 40.9150°E civarı, doğudan batı istikametinde ilerleme.

SİLAHLANMA (kaynak bildirimi):
- Susturuculu keskin nişancı tüfekleri
- Patlayıcı gereçler (C4 tipi)
- Gece görüş cihazları

YORUM: Eğer bu bilgi doğruysa, topçu bataryasının etkisizleştirilmesi
KBR'ye büyük taktik avantaj sağlar. KILINÇ-ART çevresinde acil güvenlik
önlemleri alınmalı.

ÖNERİ: KILINÇ-ART savunma çemberi güçlendirilmeli, çevre devriye artırılmalı.
""".format(t2=utc(2).strftime("%Y-%m-%d %H:%M UTC")),
                source_type="humint",
                reporting_unit="HUMINT Birimi",
                area_of_interest="KILINÇ-ART Güvenlik Bölgesi",
                report_time=utc(2),
                is_processed=True,
                units_extracted=1,
                parsed_summary="HUMINT: 12-15 kişilik KBR sabotaj timi, KILINÇ-ART topçu mevzisini hedefliyor. Susturuculu silahlar ve patlayıcı taşıyorlar.",
            ),
        ]

        for r in reports:
            r.received_at = datetime.now(timezone.utc)
            r.created_at = datetime.now(timezone.utc) if not hasattr(r, 'created_at') else r.created_at
            db.add(r)

        db.flush()
        print(f"      {len(reports)} saha raporu olusturuldu.")

        # ════════════════════════════════════════════════════════
        # [5/5] TAKTİK DEĞERLENDİRMELER
        # ════════════════════════════════════════════════════════
        print("\n[5/5] Taktik degerlendirmeler olusturuluyor...")

        kbr_alfa_id = uid_map.get("KBR-ALFA")
        kbr_bravo_id = uid_map.get("KBR-BRAVO")
        kbr_delta_id = uid_map.get("KBR-DELTA")

        assessments = [
            TacticalAssessment(
                unit_fk=kbr_bravo_id,
                assessment_type="threat_estimate",
                title="KBR-BRAVO / T-72 Zırhlı Kolu — Kritik Tehdit Değerlendirmesi",
                content="""KBR-BRAVO, 6 adet T-72B tankı ve 4 adet BMP-2 ile KILINÇ-1 mevziinin sol (doğu) kanadını çevrelemek üzere güneybatı istikametinde hareket etmektedir.

Bu unsurun KILINÇ-2 (3x M60T) ile karşılaşması durumunda:
- Sayısal üstünlük KBR tarafında (6 vs 3 tank)
- T-72B'nin yeni reaktif zırhı M60T'nin ana silahına karşı önemli koruma sağlar
- BMP-2'ler boşluk doldurmada ve piyade desteğinde etkin

Çevreleme hareketi 4-6 saat içinde tamamlanabilir. KILINÇ-1 bu durumda:
1. İkmal güzergahlarını tamamen kaybeder
2. İki cephede baskıya maruz kalır (KBR-ALFA önden, KBR-BRAVO arkadan)""",
                recommendation="""ACİL ÖNLEMLER:
1. KILINÇ-ART: KBR-BRAVO kolununa karşı anında karşı batarya ateşi açılmalı
2. KILINÇ-2: Güneye değil, KBR-BRAVO'yu durdurmak üzere doğuya yönlendirilmeli
3. Hava desteği talep edilmeli — T-72B kümesi öncelikli hedef
4. KILINÇ-1: Doğu savunma hattını güçlendirmeli, batı çıkış güzergahı hazırlanmalı
5. KILINÇ-LOG: İkmal batı güzergahından yapılmalı, keşif acil""",
                confidence=0.82,
                priority="critical",
                area_name="Doğu Kanat / T-72 Çevreleme Rotası",
                lat=37.0650, lng=40.8450,
                generated_by="analyst",
            ),
            TacticalAssessment(
                unit_fk=kbr_alfa_id,
                assessment_type="course_of_action",
                title="KBR-ALFA / Piyade Taburunun Olası Hareket Tarzları",
                content="""KBR-ALFA (280+ personel, 8 zırhlı) güneye ilerlemekte ve Kızıltepe Sırtı'na baskı yapmaktadır. 3 olası hareket tarzı:

HTZ-1 (En Olası — %60): Doğrudan cephe baskısı
KBR-ALFA, KILINÇ-1 mevziine doğrudan taarruz açar. KBR-CHARLIE topçu desteği, KBR-BRAVO sol kanatten çevirmeyle eş zamanlı.

HTZ-2 (Orta Olası — %25): Bekleme / Sarma
Sırt mevziini bloke edip KBR-BRAVO'nun çevrelemeyi tamamlamasını bekler, ardından koordineli saldırı.

HTZ-3 (Az Olası — %15): Göstermelik baskı / Gerçek hedef farklı
KILINÇ-1'i bağlayarak KBR-DELTA'nın KILINÇ-ART sabotajını kolaylaştırır.""",
                recommendation="""KILINÇ-1 savunması güçlendirilmeli ve KILINÇ-ART ateş desteği hazırlığı yapılmalı. HTZ-1 durumunda savunma derinliği kritik.""",
                confidence=0.68,
                priority="high",
                area_name="Kızıltepe Sırtı Kuzey Yaklaşımı",
                lat=37.0890, lng=40.7020,
                generated_by="analyst",
            ),
            TacticalAssessment(
                unit_fk=kbr_delta_id,
                assessment_type="warning",
                title="KBR-DELTA / Sabotaj Timi — Acil Uyarı",
                content="""HUMINT doğrulaması ve konum analizi birlikte değerlendirildiğinde, KBR-DELTA'nın KILINÇ-ART topçu mevzisini hedef aldığı kuvvetle muhtemeldir.

Tehdit analizi:
- 14 kişilik özel hareket timi, susturuculu silahlar ve C4 patlayıcı
- KILINÇ-ART'ın 3.2 km doğusunda, batıya ilerliyor
- Gece görüş donanımı varsa gece operasyonu planlıyor olabilir
- Topçu mevzisinin etkisizleştirilmesi KBR'ye büyük taktik avantaj sağlar

Bu tehdit realize olursa: KILINÇ-1 ateş desteği kaybeder, KBR-ALFA taarruz avantajı elde eder.""",
                recommendation="""1. KILINÇ-ART çevresi: Savunma çemberi 360° kurulmalı
2. 150m çevre aydınlatma fişek / hareket sensörü
3. KBR-DELTA rotasını kesmek için KILINÇ-RECON yönlendirilmeli
4. Tüm mevziler çift nöbetçi düzenine geçmeli""",
                confidence=0.72,
                priority="critical",
                area_name="KILINÇ-ART Güvenlik Alanı",
                lat=37.1420, lng=40.9150,
                generated_by="analyst",
            ),
            TacticalAssessment(
                unit_fk=None,
                assessment_type="situation_update",
                title="GENEL DURUM DEĞERLENDİRMESİ — Operasyon Güvenli Sınır",
                content="""GENEL OPERASYON DURUMU — KRİTİK

Mevcut durumda KILINÇ Tugayı 3 ayrı tehdidle aynı anda başa çıkmak durumundadır:

1. CEPHE BASINCI (KBR-ALFA): 280+ kişilik piyade KILINÇ-1'e yaklaşıyor. ETA: ~2 saat.
2. KANAT ÇEVRIMI (KBR-BRAVO): 6x T-72B doğu kanadını sarıyor. ETA: 4-6 saat.
3. SABOTAJ TEHDİDİ (KBR-DELTA): Topçu mevzisine yönelik, ETA: belirsiz/muhtemelen gece.

Buna ek olarak:
- KILINÇ-1 cephane kritik seviyede (6 saat)
- İkmal güzergahı kesme tehdidi altında
- 3 yaralı tahliye bekliyor

GÜÇ DENGESI:
Dost: ~291 muharip, 3 tank, 2 topçu, 2 obüs
Düşman: ~411 teyit edilen muharip, 6 tank, 4 araç, 4 topçu (UNKNOWN-01 ve 02 hariç)
Oran: 1.41:1 düşman üstünlüğü (donanım avantajı hariç)""",
                recommendation="""ÖNCELİKLİ EYLEMLER (önem sırasıyla):
1. KBR-BRAVO'nun durdurulması — hava/topçu desteği
2. KILINÇ-LOG ikmalinin batı güzergahından yapılması
3. KBR-DELTA'nın engellenmesi için KILINÇ-RECON yönlendirilmesi
4. KILINÇ-ART tarafından KBR-CHARLIE karşı batarya atışı
5. Takviye talep edilmesi""",
                confidence=0.85,
                priority="critical",
                area_name="Operasyon Güvenli Sınır — Genel Bölge",
                lat=37.1500, lng=40.7800,
                generated_by="analyst",
            ),
        ]

        for a in assessments:
            a.created_at = datetime.now(timezone.utc)
            a.updated_at = datetime.now(timezone.utc)
            db.add(a)

        db.commit()
        print(f"      {len(assessments)} degerlendirme olusturuldu.")

        # ── Özet ────────────────────────────────────────────────
        print("\n" + "=" * 60)
        print("  YUKLEME TAMAMLANDI")
        print("=" * 60)
        total_friendly = db.query(TacticalUnit).filter_by(side="friendly").count()
        total_enemy = db.query(TacticalUnit).filter_by(side="enemy").count()
        total_unknown = db.query(TacticalUnit).filter_by(side="unknown").count()
        total_pos = db.query(TacticalPosition).count()
        total_rep = db.query(TacticalReport).count()
        total_ass = db.query(TacticalAssessment).count()
        print(f"  Birimler  : {total_friendly} dost / {total_enemy} dusman / {total_unknown} bilinmeyen")
        print(f"  Pozisyon  : {total_pos} konum gecmisi kaydi")
        print(f"  Raporlar  : {total_rep} saha raporu")
        print(f"  Analiz    : {total_ass} taktik degerlendirme")
        print()
        print("  Sistemi baslatin ve sol menuden 'Askeri Mod' > 'Operasyonel Durum Resmi'")
        print("  sayfasini acin. COP katmanini etkinlestirin.")
        print("=" * 60)

    except Exception as e:
        db.rollback()
        print(f"\nHATA: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()
