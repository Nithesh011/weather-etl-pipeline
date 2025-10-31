# Weather ETL Pipeline — Mumbai (Hourly → BigQuery)

A production-style ETL pipeline that extracts hourly weather data (previous day) for **Mumbai** using Open-Meteo, transforms it with **PySpark** (min / max / avg temperatures, precipitation totals / averages), and loads results into **BigQuery**. The pipeline is orchestrated by **Apache Airflow** inside Docker.

---

## 📂 Contents
- `dags/` — Airflow DAG (`weather_etl_dag.py`)
- `etl/` or `scripts/` — extraction, transformation, and load scripts
  - `scripts/extract/` — API extraction (`extract_api_data.py`)
  - `scripts/pyspark/` — PySpark transformations (`pyspark_data_clean.py`)
  - `scripts/bigquery/` — BigQuery upload (`bigquery_data_update.py`)
- `notebooks/` — experiment notebooks (optional)
- `config/` — local-only secrets (do **not** commit)
- `architecture.png` — pipeline diagram
- `ENVIRONMENT.md` — environment variable reference
- `requirements.txt` — Python dependencies
- `Dockerfile` — container image for Airflow runtime
- `requirements_and_failures.md` — troubleshooting notes and package issues

---

## ⚡ Quick Start (Local / Dev)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nithesh011/weather-etl-pipeline.git
   cd weather-etl-pipeline
````

2. **Create `.env` file** (see `ENVIRONMENT.md` for details)

   ```bash
   cp .env.template .env
   # fill in values (do NOT include service account JSON in repo)
   ```

3. **Build the Docker image**

   ```bash
   docker build -t weather-etl-airflow .
   ```

4. **Run the container**

   ```bash
   docker run -d --name weather_airflow -p 8080:8080 \
     -e GCP_KEY_PATH=/opt/airflow/config/<KEY>.json \
     -e GCP_BUCKET_NAME=<YOUR_BUCKET> \
     -e GCP_PROJECT_ID=<YOUR_PROJECT_ID> \
     -e DATA_PATH=/opt/airflow/scripts \
     -v $(pwd):/opt/airflow:rw \
     -v $(pwd)/config/<KEY>.json:/opt/airflow/config/<KEY>.json:ro \
     weather-etl-airflow
   ```

5. **Access the Airflow UI**

   * Open `http://<VM_IP>:8080`
   * Enable and trigger the `weather_data_mumbai` DAG

---

## 🔐 Environment & Secrets

Do **not commit** service account JSON files.
Use the `config/` folder locally and ensure `.gitignore` includes:

```
config/*.json
.env
```

For production, prefer **GCP Secret Manager** or **Airflow Connections** instead of mounting JSON keys directly.
See `ENVIRONMENT.md` for environment variable details.

---

## 🧪 Development & Testing

* **Format code:** `black .`
* **Lint code:** `ruff .` (or `flake8`)
* **Run tests:** `pytest tests/`

Suggested commands in `Makefile`:
`make build`, `make test`, `make lint`

---

## 🚀 Production Notes

* Use Airflow **Variables / Connections** for GCP credentials and parameters
* Add **retries** and **SLAs** for tasks; alert on failures (email / Slack)
* Use **partitioned tables** in BigQuery for daily inserts
* Prefer appending to BigQuery using `load_table_from_file()` with proper dedup keys

---

## 🏗️ Architecture

See `architecture.png` for the pipeline flow:
**Extract → Transform → Upload → BigQuery**

The diagram shows:

* Raw JSON storage in GCS
* Transformation via PySpark
* Final destination: BigQuery

---

## 🤝 Contributing

1. Fork the repository
2. Create a branch: `feature/<name>`
3. Run formatters & tests locally
4. Commit and open a Pull Request

---

## 📬 Contact

**Nithesh Kumar**
[LinkedIn Profile](https://www.linkedin.com/in/nithesh11)

```

---

