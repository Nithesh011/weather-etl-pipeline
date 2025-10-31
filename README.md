
# Weather ETL Pipeline

**Short summary**  
A production-style ETL pipeline that extracts hourly weather data (previous day) for Mumbai from Open-Meteo, transforms it with PySpark (min/max/avg temperatures, total & avg precipitation), and loads results into BigQuery. The pipeline is orchestrated by Apache Airflow running in a Docker container.

---

## Repository structure

.
├── Dockerfile
├── requirements.txt
├── README.md
├── requirements_and_failures.md
├── architecture.png
├── project_documentation.md
├── dags/
│ └── weather_etl_dag.py
├── scripts/
│ ├── extract/
│ │ └── extract_api_data.py
│ ├── pyspark/
│ │ └── pyspark_data_clean.py
│ └── bigquery/
│ └── bigquery_data_update.py
├── config/ # STORE KEYS LOCALLY (do NOT commit)
└── notebooks/ # optional: experiment notebooks (archival)

yaml
Copy code

---

## Quick start (development, on your GCP VM)

> **Important:** Do not commit your service account JSON. Place it under `config/` locally and ensure `.gitignore` prevents accidental commits.

1. Build the Docker image (from repo root):
```bash
sudo docker build -t weather-etl-airflow .
Run the container (example — replace placeholders):

bash
Copy code
sudo docker run -d --name weather_airflow -p 8080:8080 \
  -e GCP_KEY_PATH=/opt/airflow/config/<YOUR_KEY>.json \
  -e GCP_BUCKET_NAME=<YOUR_BUCKET> \
  -e GCP_PROJECT_ID=<YOUR_PROJECT_ID> \
  -e DATA_PATH=/opt/airflow/scripts \
  -v /home/<YOUR_USER>/weather-etl-pipeline:/opt/airflow:rw \
  -v /home/<YOUR_USER>/weather-etl-pipeline/config/<YOUR_KEY>.json:/opt/airflow/config/<YOUR_KEY>.json:ro \
  weather-etl-airflow
Open Airflow UI:

cpp
Copy code
http://<VM_IP>:8080
Login with the admin user you created (admin / admin or whichever you set).

Enable and trigger the weather_data_mumbai DAG.

Environment & config
Config folder

Create a config/ folder locally and put your service-account JSON there.

Do not commit the JSON to GitHub.

Environment variables used

GCP_KEY_PATH: path inside container to service JSON (e.g. /opt/airflow/config/key.json)

GCP_BUCKET_NAME: GCS bucket for raw JSON

GCP_PROJECT_ID: GCP project id

DATA_PATH: path inside container where scripts read/write (default /opt/airflow/scripts)

Pass these using -e when running docker run. See run command above.

Contact / Author
Nithesh Kumar
EOF

yaml
Copy code

---

### 2) Create/overwrite `.gitignore`
```bash
cat > .gitignore <<'EOF'
# Ignore keys and environment
config/*.json
.env
.venv/
__pycache__/
*.pyc
.DS_Store

# Airflow local files
airflow-webserver.log
airflow-webserver.err
airflow.db
EOF
3) Create ENVIRONMENT.md (explains env vars)
bash
Copy code
cat > ENVIRONMENT.md <<'EOF'
# Environment variables - how to set and where used

## Required environment variables (for Docker runtime)

- GCP_KEY_PATH — Absolute path inside container where service account JSON is mounted.
  Example: /opt/airflow/config/subtle-seer-...json

- GCP_BUCKET_NAME — GCS bucket used for raw JSON uploads.
  Example: raw_weather_data_backup

- GCP_PROJECT_ID — GCP project id for BigQuery.
  Example: subtle-seer-472708-q3

- DATA_PATH — Shared folder path for JSON & CSV inside container; scripts read/write here.
  Example: /opt/airflow/scripts

## How to pass with docker run
Example:
docker run -d --name weather_airflow -p 8080:8080 \
  -e GCP_KEY_PATH=/opt/airflow/config/<KEY>.json \
  -e GCP_BUCKET_NAME=raw_weather_data_backup \
  -e GCP_PROJECT_ID=subtle-seer-... \
  -e DATA_PATH=/opt/airflow/scripts \
  -v /home/<user>/weather-etl-pipeline:/opt/airflow:rw \
  -v /home/<user>/weather-etl-pipeline/config/<key>.json:/opt/airflow/config/<key>.json:ro \
  weather-etl-airflow

## Local / Colab testing
In Colab or local Python, set with os.environ[...] like:
import os
os.environ["GCP_KEY_PATH"] = "/content/config/<KEY>.json"
os.environ["GCP_BUCKET_NAME"] = "raw_weather_data_backup"
os.environ["GCP_PROJECT_ID"] = "my-project"
os.environ["DATA_PATH"] = "/content"

