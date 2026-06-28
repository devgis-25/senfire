# 🚒 Teranga Rescue GIS

**Interactive WebGIS application analyzing fire station coverage across Senegal.**

Built with open geospatial data (OpenStreetMap + WorldPop 2020), this project maps
fire station service areas and identifies underserved populations across all 14 regions
of Senegal.

---

## 🔍 Key Findings

| Metric | Value |
|--------|-------|
| Fire stations mapped | 28 |
| Population within 5km of a station | 5.56M (33%) |
| Population beyond 5km | 11.14M (67%) |
| Territory covered | 1,262 km² (0.6%) |
| Territory uncovered | 195,581 km² (99.4%) |

> **2 out of 3 Senegalese people have no rapid access to fire services.**

---

## ✨ Features

- 🗺 Interactive map with toggleable layers (coverage zones, buffers, regions)
- 📊 Regional priority scoring system (0–100 scale)
- 🔍 Nearest fire station finder — click anywhere on the map
- 📈 National and per-region statistics
- 🎨 Responsive dark UI built for desktop and mobile

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Data preparation | QGIS, QuickOSM, WorldPop |
| Spatial database | PostgreSQL + PostGIS |
| Backend | Django, GeoDjango, Django REST Framework |
| Geospatial API | djangorestframework-gis |
| Frontend | MapLibre GL JS, HTML/CSS/JS |
| Spatial analysis | GeoPandas, Shapely, pyproj |
| Data sources | OpenStreetMap, WorldPop 2020 |
| Projection | EPSG:32628 (UTM Zone 28N) |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL 17 + PostGIS 3.5
- QGIS 3.x (for data preparation only)

### Installation

```bash
# Clone the repository
git clone https://github.com/devgis-25/senfire.git
cd teranga-rescue-gis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Database Setup

```bash
# Create PostGIS database
createdb senfire
psql -d senfire -c "CREATE EXTENSION postgis;"

# Import spatial data
ogr2ogr -f "PostgreSQL" "PG:host=localhost dbname=senfire user=postgres" \
  data/processed/casernes.gpkg -nln casernes -t_srs EPSG:32628

# Run Django migrations
cd backend
python manage.py migrate
python manage.py createsuperuser
```

### Run

```bash
python manage.py runserver
# Open http://127.0.0.1:8000
```

---

## 📡 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/casernes/` | All fire stations (GeoJSON) |
| `GET /api/regions/` | Administrative regions (GeoJSON) |
| `GET /api/zone-desservie/` | Covered zones (GeoJSON) |
| `GET /api/zone-non-desservie/` | Uncovered zones (GeoJSON) |
| `GET /api/stats/` | National statistics |
| `GET /api/region-stats/` | Per-region priority scores |
| `GET /api/casernes/proche/?lat=XX&lng=XX` | Nearest fire stations |

---

## 📁 Project Structure

senfire/

├── backend/

│   ├── api/

│   │   ├── models.py

│   │   ├── views.py

│   │   ├── serializers.py

│   │   ├── urls.py

│   │   └── admin.py

│   ├── config/

│   │   ├── settings.py

│   │   └── urls.py

│   └── templates/

│       └── index.html

├── data/

│   └── processed/    # GeoPackage files (not included in repo)

├── docs/             # Screenshots and notes

├── requirements.txt

└── README.md




---

## 🌍 Data Sources

- **Fire stations** — OpenStreetMap contributors (ODbL license)
- **Administrative boundaries** — OpenStreetMap (ODbL license)
- **Population data** — WorldPop 2020, University of Southampton
- **Projection** — EPSG:32628, UTM Zone 28N (optimal for Senegal)

---

## 👤 Author

**Oumar** — Fullstack Developer & WebGIS Engineer, Dakar, Senegal

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/oumar-thiombane-a0a51721b/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/devgis-25)

---

## 📄 License

MIT License — feel free to use, modify, and share.