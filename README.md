
# Dynamic Weather ETL Pipeline

## Overview
This project implements a fully automated ETL (Extract, Transform, Load) pipeline to fetch and process daily weather data for Mumbai, India, using the Open-Meteo API, PySpark, Apache Airflow, Google Cloud Storage (GCS), and Google BigQuery. The pipeline runs daily, extracting the previous day's weather data, transforming it into aggregated metrics, and loading the results into a BigQuery table for historical analysis. This project showcases data engineering skills, including cloud integration, data transformation, and workflow orchestration, suitable for a portfolio piece.

## Architecture
The pipeline follows this flow (see [architecture.png](architecture.png)):
- **Extract**: Fetches daily weather data from the Open-Meteo API and backs it up to GCS.
- **Transform**: Uses PySpark to filter data to the previous day, computes maximum and minimum temperatures, and calculates total precipitation.
- **Load**: Appends transformed data to a BigQuery table.
- **Orchestration**: Apache Airflow schedules and manages the pipeline on a GCP virtual machine.

## Setup Instructions
1. **Prerequisites**:
   - GCP account with a service account key (JSON file).
   - GCP VM (e.g., e2-medium) with Airflow installed.
   - Python 3.8+ with required libraries (`pyspark`, `requests`, `google-cloud-storage`, `google-cloud-bigquery`).
2. **Configuration**:
   - Replace placeholders in `weather_etl_dag.py`:
     - `your-key.json` with your GCP service account key path.
     - `your-bucket` with your GCS bucket name.
     - `your-project-id` with your GCP project ID.
   - Upload the key to `/opt/airflow/` on the VM.
3. **Deployment**:
   - Copy `weather_etl_dag.py` to the Airflow DAGs folder (e.g., `/opt/airflow/dags/`).
   - Start Airflow services (`airflow webserver` and `airflow scheduler`).
   - Trigger the `weather_etl` DAG via the Airflow UI.

## Results
The output is stored in `sample_results.csv` and includes:
- `id`: Unique identifier starting from 1.
- `city`: Mumbai.
- `max_temp`: Maximum temperature (rounded to 2 decimals, in °C).
- `min_temp`: Minimum temperature (rounded to 2 decimals, in °C).
- `total_precipitation`: Total precipitation (rounded to 2 decimals, in mm).
- `end_date`: Date of the data (previous day).

Sample row: `1,Mumbai,25.20°C,17.36°C,3.70 mm,2025-09-27`.

## Challenges and Solutions
- **Java Dependency**: Encountered Java compatibility issues on the GCP VM; resolved by setting `JAVA_HOME` to `/usr/lib/jvm/java-11-openjdk-amd64`.
- **Docker Issue**: Initial attempts to use Docker for Airflow failed due to port conflicts and volume mounting issues on the VM; switched to manual Airflow installation.
- **API Data Mismatch**: The Open-Meteo API returned future dates; filtered to yesterday’s data to ensure accuracy.

## Resume Highlight
- "Dynamic Weather ETL Pipeline (GCP, PySpark, Airflow, GCS, BigQuery) - Automated daily extraction, transformation, and loading of Mumbai weather data with unique ID, rounded temperature (°C), and precipitation (mm) metrics [https://github.com/Nithesh011/weather-etl-pipeline]"

## Project Documentation
For detailed insights, including setup steps and challenges, refer to [project_documentation.md](project_documentation.md).


## License
MIT License - Free to use and modify.
