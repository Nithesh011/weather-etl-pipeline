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
   - GCP VM (e.g., e2-medium) with Ubuntu 20.04.
   - Python 3.8+ and Git installed.
2. **Configuration**:
   - Replace placeholders in `weather_etl_dag.py`:
     - `your-key.json` with your GCP service account key path.
     - `your-bucket` with your GCS bucket name.
     - `your-project-id` with your GCP project ID.
   - Upload the key to `/opt/airflow/` on the VM.
3. **Deployment**:
   - SSH into the VM: `gcloud compute ssh <instance-name>`.
   - Update the system: `sudo apt update && sudo apt upgrade -y`.
   - Install Python and Git: `sudo apt install python3.8 python3-pip git -y`.
   - Set up Airflow manually:
     - Create a virtual environment: `python3.8 -m venv /opt/airflow_env`.
     - Activate it: `source /opt/airflow_env/bin/activate`.
     - Install Airflow: `pip install apache-airflow==2.5.1`.
     - Initialize the database: `airflow db init`.
     - Create an admin user: `airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com`.
     - Configure `AIRFLOW_HOME=/opt/airflow` in `~/.bashrc` and source it: `source ~/.bashrc`.
     - Copy `airflow.cfg` to `/opt/airflow/` and edit `load_examples = False`.
     - Create the DAGs folder: `mkdir /opt/airflow/dags` and copy `weather_etl_dag.py` there.
     - Install dependencies: `pip install pyspark requests google-cloud-storage google-cloud-bigquery`.
   - Start Airflow services:
     - Webserver: `airflow webserver -p 8080 &` in one terminal.
     - Scheduler: `airflow scheduler &` in another terminal.
   - Access the UI at `http://<VM-external-IP>:8080` (get IP with `gcloud compute instances list`).
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

## Technical Documentation
### Tools and Technologies
- **Open-Meteo API**: Provides weather data.
- **PySpark**: Handles data transformation and aggregation.
- **Airflow**: Orchestrates the ETL workflow.
- **GCS**: Stores raw data backups.
- **BigQuery**: Stores and analyzes transformed data.

### Data Flow
1. **Extract**: Fetches data and saves it to GCS.
2. **Transform**: Filters to the previous day, computes metrics.
3. **Load**: Appends to BigQuery.

### Setup and Deployment Details
- Deploy a GCP VM and configure it with the above steps.
- Ensure the service account key is securely uploaded and placeholders are replaced.

### Challenges and Resolutions
- **Java Compatibility**: Spark failed due to missing Java; resolved by setting `JAVA_HOME` to `/usr/lib/jvm/java-11-openjdk-amd64`.
- **Docker Issues**: Attempted Docker for Airflow but encountered port conflicts (e.g., 8080) and volume mounting errors on the VM; switched to manual installation.
- **API Data Accuracy**: The API returned future dates; implemented a filter for yesterday’s data.

### Future Improvements
- Transition to hourly data for a true average temperature.
- Implement incremental loading (`WRITE_APPEND`) for historical tracking.
- Add error logging to Airflow for enhanced monitoring.

## Resume Highlight
- "Dynamic Weather ETL Pipeline (GCP, PySpark, Airflow, GCS, BigQuery) - Automated daily extraction, transformation, and loading of Mumbai weather data with unique ID, rounded temperature (°C), and precipitation (mm) metrics [https://github.com/Nithesh011/weather-etl-pipeline]"

## Contributors
- Nithesh [https://github.com/Nithesh011]
