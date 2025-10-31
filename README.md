# Weather ETL Pipeline — Mumbai (Hourly → BigQuery)

A production-ready ETL pipeline that extracts hourly weather data (previous day) for **Mumbai** using the **Open-Meteo API**, transforms it with **PySpark** (min/max/avg temperatures and precipitation stats), and loads the processed data into **Google BigQuery**.  
The workflow is automated and orchestrated using **Apache Airflow** running inside Docker.

---

## 📁 Repository Structure

```
weather-etl-pipeline/
├── architecture.png                 # Pipeline architecture diagram
├── dags/
│   └── weather_data_mumbai_dag.py   # Airflow DAG definition
├── Dockerfile                       # Container image for Airflow runtime
├── ENVIRONMENT.md                   # Environment variable and setup reference
├── notebook/
│   └── weather_etl_pipeline.ipynb   # Jupyter notebook for experimentation
├── project_documentation.md         # Detailed project overview and workflow
├── requirements.txt                 # Python dependencies
├── sample_result.csv                # Sample output file generated after ETL
├── scripts/
│   ├── extract/
│   │   └── extract_api_data.py      # Data extraction from Open-Meteo API
│   ├── pyspark/
│   │   └── pyspark_data_clean.py    # PySpark transformations and aggregations
│   └── bigquery/
│       └── bigquery_data_update.py  # Data loading into BigQuery
└── .gitignore                       # Files and folders excluded from Git
```

---

## ⚙️ Quick Start (Local / Dev Setup)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nithesh011/weather-etl-pipeline.git
   cd weather-etl-pipeline
   ```

2. **Create and configure environment variables**
   Refer to `ENVIRONMENT.md` for details on required variables.

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

5. **Access Airflow UI**
   * Open `http://<VM_IP>:8080`
   * Enable and trigger the **`weather_data_mumbai`** DAG

---

## 🔐 Environment & Secrets

* Do **not commit** service account JSON files.
* Use a local `config/` folder to store credentials.
* Ensure `.gitignore` includes:

  ```
  config/*.json
  .env
  ```

For production, prefer **GCP Secret Manager** or **Airflow Connections** to manage credentials securely.

---

## 🧪 Development & Testing

* **Format code:** `black .`
* **Lint code:** `ruff .` or `flake8`
* **Run tests (if added):** `pytest tests/`

---

## 🧱 Architecture Overview

Refer to `[architecture.png](architecture.png)` for a visual overview of the ETL workflow:

**Extract → Transform → Load → BigQuery**

1. **Extract:** Fetch hourly weather data for Mumbai from Open-Meteo API.
2. **Transform:** Process raw data with PySpark to compute key metrics.
3. **Load:** Store the final cleaned and aggregated data in BigQuery.

---

## 🗂️ Sample Output

A sample of the transformed dataset can be found in `sample_result.csv`.

---

## 🧾 Project Documentation

For a deeper understanding of workflow logic, Airflow DAG structure, and execution details, refer to `[project_documentation.md](project_documentation.md) `.

---

## 📬 Contact

**Nithesh Kumar**
[LinkedIn Profile](https://www.linkedin.com/in/nithesh11)

---
 
