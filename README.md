# 🔍 AI-Powered Data Quality & Reporting Automation

> A Django-based web application that automates data quality monitoring using ML-driven anomaly detection, scheduled reporting, and a real-time dashboard — built with Docker and CI/CD via GitHub Actions.

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10, Django 4.x |
| REST API | Django REST Framework |
| ML / Detection | Scikit-learn (Isolation Forest), Pandas, NumPy |
| Task Queue | Celery + Redis |
| Scheduling | django-celery-beat |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Frontend | HTML5, CSS3, Vanilla JS, Chart.js |

---

## ✨ Features

- 📂 **CSV Upload** — Upload any dataset via the dashboard or REST API
- 🤖 **ML Anomaly Detection** — Isolation Forest automatically flags outliers across all numeric columns
- 📊 **Real-time Dashboard** — Visualize reports, anomaly scores, and status breakdowns with live charts
- ⏰ **Scheduled Reports** — Celery Beat runs quality checks on all datasets automatically on a schedule
- ⚡ **Async Processing** — Background task execution via Celery workers (non-blocking)
- 🐳 **Docker Ready** — Full stack runs in containers with a single command
- ✅ **CI/CD Pipeline** — GitHub Actions runs all tests automatically on every commit

---

## 🏗️ Project Structure
## ⚙️ Getting Started

### Prerequisites

- Python 3.10+
- Docker and Docker Compose
- Git

---

### Option A — Run with Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/data-quality-automation.git
cd data-quality-automation

# 2. Create the .env file
cat > .env << EOF
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
EOF

# 3. Build and start all services
docker-compose up --build
```

Visit http://localhost:8000 — the dashboard loads automatically.

---

### Option B — Run Locally

```bash
# 1. Clone and set up virtual environment
git clone https://github.com/YOUR_USERNAME/data-quality-automation.git
cd data-quality-automation
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Start Redis (Mac)
brew services start redis

# 5. Start Django server (Terminal 1)
python manage.py runserver

# 6. Start Celery worker (Terminal 2)
celery -A core worker --loglevel=info

# 7. Start Celery Beat scheduler (Terminal 3)
celery -A core beat --loglevel=info
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/datasets/ | List all datasets |
| POST | /api/datasets/ | Create a new dataset |
| GET | /api/datasets/{id}/ | Retrieve a dataset |
| POST | /api/datasets/{id}/run-check/ | Run synchronous anomaly check |
| POST | /api/datasets/{id}/run-check-async/ | Run async anomaly check |
| GET | /api/records/ | List all data records |
| POST | /api/records/ | Create a data record |
| GET | /api/reports/ | List all anomaly reports |
| POST | /api/upload-csv/ | Upload a CSV file as a dataset |

---

## 🤖 How the ML Detection Works

The project uses Isolation Forest — an unsupervised ML algorithm that detects anomalies by isolating observations in a random forest structure.

- Score greater than 0 — Normal record
- Score less than 0 — Anomaly flagged

Key parameters:
- contamination=0.1 — expects ~10% of records to be anomalies
- random_state=42 — reproducible results
- Handles missing values automatically (fills with column mean)

---

## 📊 Example — Real Dataset Results

Uploaded a 102-row infrastructure dataset with project metrics:

| Record | Project | Issue Detected |
|--------|---------|---------------|
| #6 | PRJ100006 | 1 ticket opened, 2 closed — inconsistent counts |
| #42 | PRJ100042 | Usage cost $3,425 — above normal range |
| #54 | PRJ100054 | Usage cost $6,377 — major cost spike |
| #61 | PRJ100061 | Usage cost $8,326 — highest anomaly score |

The model correctly identified cost spikes nearly 4x the dataset average.

---

## 🧪 Running Tests

```bash
python manage.py test data_quality.tests --verbosity=2
```

Tests cover:
- Dataset CRUD API endpoints
- DataRecord creation
- ML anomaly detector logic
- Full end-to-end run-check endpoint

---

## 🔄 CI/CD Pipeline

Every push to main or develop automatically:
1. Spins up Ubuntu and Redis on GitHub Actions
2. Installs all Python dependencies
3. Runs Django migrations
4. Executes the full test suite

---

## 🐳 Docker Services

| Service | Description |
|---------|-------------|
| web | Django application server |
| redis | Message broker for Celery |
| celery_worker | Processes async anomaly detection tasks |
| celery_beat | Triggers scheduled quality checks |

---

## 📈 Dashboard Features

- Stats Cards — Total datasets, records, reports, and anomalies at a glance
- Bar Chart — Anomalies found per report
- Doughnut Chart — Report status breakdown
- Datasets Table — All datasets with one-click Run Check button
- Reports Table — Status badges and anomaly counts
- Anomaly Detail — Per-record scores with visual score bars
- CSV Upload — Upload and analyse a dataset directly from the UI
- Auto-refresh — Dashboard updates every 30 seconds

---

## 🔮 Potential Improvements

- PostgreSQL for production database
- JWT authentication for API security
- PDF / CSV export of anomaly reports
- Email alerts when anomalies are detected
- Support for additional ML models (Z-score, DBSCAN)

---

## 👩‍💻 Author

**Deeksha Pingalay Subasankara**
[GitHub](https://github.com/YOUR_USERNAME) · [LinkedIn](https://linkedin.com/in/YOUR_LINKEDIN)

---

## 📄 License

This project is open source and available under the MIT License.
