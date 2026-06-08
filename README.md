[README.md](https://github.com/user-attachments/files/28721440/README.md)
<div align="center">

#  AI Intelligence Analysis System
### *İZÇİ — Multi-Source OSINT & GEOINT Platform*

**A modular, AI-powered open-source intelligence system for person-centric analysis, geospatial reasoning, and multi-source data fusion — running entirely on local LLMs with no cloud dependency.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-PostGIS-336791?style=flat-square&logo=postgresql&logoColor=white)](https://postgis.net)
[![Ollama](https://img.shields.io/badge/LLM-Ollama%20%2F%20Gemma3-black?style=flat-square)](https://ollama.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Thesis](https://img.shields.io/badge/Academic-M.S.%20Thesis%20%40%20Hacettepe-red?style=flat-square)](https://bi.hacettepe.edu.tr)

---

</div>

##  About This Project

This repository contains the software artifact of a Master's thesis developed at **Hacettepe University, Institute of Informatics** (Bilişim Sistemleri, 2026).

The system — codenamed **İZÇİ** — is a full-stack intelligence platform that:

- Ingests **unstructured Turkish and English text** from multiple open sources (news feeds, press releases, public reports, HUMINT notes)
- Extracts **persons, organizations, locations, meetings, and relationships** using locally-run large language models
- **Deduplicates and clusters** extracted entities using spatiotemporal PostGIS operations
- Builds a **multi-source relationship graph** from five independent link types
- Generates **person-centric intelligence dossiers** with behavioral anomaly detection, pattern-of-life modeling, and intent classification

> The thesis addresses a critical gap: performing OSINT for **Turkish-language content** at small-to-medium intelligence unit scale, without cloud infrastructure or proprietary APIs.

---

##  Screenshots

| GEOINT Dashboard | Person Intelligence (PERSINT) |
|:---:|:---:|
| ![Dashboard](screenshots/ui_dashboard.png) | ![Person Intelligence](screenshots/Kişi_İstihabrat.png) |

| Operations Panel | |
|:---:|:---:|
| ![Operations](screenshots/Operasyon_Ekran_Kaydı.png) | |

---

##  System Architecture Diagrams

| Person Intelligence Pipeline | Data Model & Entity Relationships |
|:---:|:---:|
| ![Person Profile Pipeline](screenshots/person_profile_pipeline.png) | ![Data Model](screenshots/data_model_workflow.png) |

| Five-Signal Relationship Graph | Pattern of Life & Behavioral Analysis |
|:---:|:---:|
| ![Relationship Graph](screenshots/five_signal_relationship_graph.png) | ![Pattern of Life](screenshots/pattern_of_life_analysis.png) |

| Autonomous Agent Dispatcher | PostGIS Geospatial Data Layer |
|:---:|:---:|
| ![Agent Architecture](screenshots/agent_dispatcher_architecture.png) | ![PostGIS](screenshots/postgis_data_layer.png) |

---

##  Key Features

###  AI-Powered Entity Extraction
- Named entity recognition (persons, orgs, locations, events) from free-form text
- Two-tier LLM routing: **Gemma 3 12B** for complex reasoning, **Gemma 3 4B** for fast tasks
- Structured JSON extraction with a 3-layer self-repair pipeline (handles malformed Turkish LLM output)

###  Person Intelligence (PERSINT)
- **11 sub-components** per person module:
  - Deduplicated timeline construction
  - Recency-Frequency-Confidence weighted current location estimation
  - Multi-source relationship graph (5 independent link types)
  - Behavioral anomaly detection (Z-score baseline comparison)
  - Alias / pseudonym detection
  - Intent-aware multilayer chat engine
  - Cross-person analysis
  - HUMINT integration
  - Pattern of Life modeling
  - Red team analysis
  - Regional activity summary

###  Geospatial Intelligence (GEOINT)
- 3D interactive map powered by **CesiumJS**
- PostGIS spatial queries (proximity, terrain, line-of-sight)
- OpenStreetMap tile integration
- Satellite imagery analysis via **OpenCV**

###  Multi-Source Data Fusion
- MAP-REDUCE profile synthesis across sources
- Relationship graph from: co-occurrence traces, meeting records, shared report mentions, alias matches, and news-news links
- Autonomous agent infrastructure with **APScheduler**

###  Audio & Multimedia
- Audio transcription using **Faster-Whisper**
- Photo upload and person matching

###  Military COP Mode
- Common Operating Picture dashboard
- Threat scoring, scenario engine (**NetworkX**), predictive analytics
- Risk assessment and simulation modules

---

##  Architecture
```
┌─────────────────────────────────────────────────────┐
│                  Presentation Layer                  │
│     Jinja2 Templates · CesiumJS · vis.js · D3.js    │
├─────────────────────────────────────────────────────┤
│                   Service Layer                      │
│   FastAPI · 30+ REST API Routers · Agent Workers    │
│   Ollama LLM Client (Gemma 3 12B / 4B)             │
├─────────────────────────────────────────────────────┤
│                    Data Layer                        │
│   PostgreSQL + PostGIS · SQLAlchemy ORM · Alembic   │
└─────────────────────────────────────────────────────┘
```

All LLM inference runs **locally via Ollama** — no data leaves the machine.

---

##  Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI 0.115, Uvicorn |
| Database | PostgreSQL + PostGIS, SQLAlchemy 2.0, Alembic |
| LLM Runtime | Ollama (Gemma 3 12B / 4B) |
| Geospatial | GeoAlchemy2, CesiumJS, OpenStreetMap |
| Graph Analysis | NetworkX |
| Computer Vision | OpenCV, Pillow, NumPy |
| Audio | Faster-Whisper |
| Data Collection | feedparser, BeautifulSoup4, NewsAPI |
| Frontend | Jinja2, vis.js, D3.js, CesiumJS |
| Scheduling | APScheduler 3.x |

---

##  Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+ with PostGIS extension
- [Ollama](https://ollama.com) with `gemma3:12b` and `gemma3:4b` models pulled

### 1. Clone & Install

```bash
git clone https://github.com/dagitirmert-coder/ai-intelligence-analysis-system.git
cd ai-intelligence-analysis-system
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials and optional API keys
```

```env
GEOINT_DATABASE_URL=postgresql+psycopg2://geoint:geoint@localhost:5432/geointdb
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_LARGE_MODEL=gemma3:12b
OLLAMA_SMALL_MODEL=gemma3:4b
```

### 3. Set Up Database

```bash
python setup_db.py          # Creates schema and PostGIS extension
alembic upgrade head        # Runs migrations
python seed_data.py         # (Optional) Load sample data
```

### 4. Pull LLM Models

```bash
ollama pull gemma3:12b
ollama pull gemma3:4b
```

### 5. Run

```bash
# Windows
baslat.bat

# or manually
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Open **http://localhost:8000** in your browser.

---

##  Repository Structure

```
├── app.py                      # FastAPI entry point
├── config.py                   # Configuration loader
├── worker.py                   # Background agent scheduler
├── api/                        # 30+ REST API routers
│   ├── person_api.py
│   ├── person_analysis_api.py  # PERSINT dossier + AI chat
│   ├── intelligence_api.py
│   ├── humint_api.py
│   ├── military_api.py         # COP mode
│   └── ...
├── core/                       # Business logic
│   ├── llm/                    # Ollama client, JSON repair
│   └── agents/                 # Autonomous agent tasks
├── db/                         # SQLAlchemy models & engine
├── templates/                  # Jinja2 HTML templates
├── static/                     # Frontend assets
├── seed_*.py                   # Sample data generators
└── screenshots/                # UI & architecture screenshots
```

---

##  Academic Context

This system is the software implementation accompanying the Master's thesis:

> **"Çoklu Kaynaklı Yapılandırılmamış İstihbarat Verilerinin Yapay Zekâ ile Tekilleştirilmesi ve Analizi Bilişim Sistemi"**
> *("AI-Based Deduplication and Analysis of Multi-Source Unstructured Intelligence Data")*
>
> Mert DAĞITIR — Hacettepe University, Institute of Informatics, 2026
> Advisor: Şahap Armağan TARIM

The thesis is available upon request via [Hacettepe University Bilişim Enstitüsü](https://bi.hacettepe.edu.tr).

---

##  Disclaimer

This system is developed for **academic research purposes**. All sample data used in the thesis and seed scripts is **entirely fictional**. The system is designed to process **publicly available open-source information (OSINT)** only. Use responsibly and in accordance with applicable laws and regulations, including GDPR (EU 2016/679) and KVKK (Law No. 6698).

---

##  License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
<sub>Built with ❤️ for academic research · Hacettepe University · 2026</sub>
</div>
