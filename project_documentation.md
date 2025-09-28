# Project Documentation: Dynamic Weather ETL Pipeline

## Project Overview
This project develops an ETL pipeline to process daily weather data for Mumbai, India, using the Open-Meteo API, PySpark, Apache Airflow, Google Cloud Storage (GCS), and Google BigQuery. The pipeline extracts the previous day's weather data, transforms it into aggregated metrics (maximum and minimum temperatures, total precipitation), and loads the results into a BigQuery table, scheduled to run daily on a GCP virtual machine using Dockerized Airflow.

## Technical Details
- **Tools and Technologies**:
  - **Open-Meteo API**: Source of weather data.
  - **PySpark**: For data transformation and aggregation.
  - **Airflow**: For workflow orchestration, deployed via Docker.
  - **GCS**: For raw data backup.
  - **BigQuery**: For data storage and analysis.
- **Data Flow**:
  1. Extract: Fetch data and save to GCS.
  2. Transform: Filter to yesterday, compute metrics.
  3. Load: Append to BigQuery.

## Setup and Deployment
1. **Environment Setup**:
   - Deploy a GCP VM (e.g., e2-medium) with Ubuntu 20.04.
   - Install Docker: `sudo apt-get update && sudo apt-get install docker.io -y`.
   - Start Docker: `sudo systemctl start docker && sudo systemctl enable docker`.
   - Pull and run Airflow: `sudo docker run -d -p 8080:8080 -v /path/to/dags:/opt/airflow/dags apache/airflow`.
   - Install Python dependencies inside the container via a `requirements.txt` file with `pyspark==3.4.0`, `requests`, `google-cloud-storage`, `google-cloud-bigquery`, and run `pip install -r requirements.txt`.
   - Install Java: `sudo apt-get install openjdk-11-jdk -y` and set `JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64`.
   - Install Google Cloud SDK: `curl https://sdk.cloud.google.com | bash` and initialize with `gcloud init`.
2. **Configuration**:
   - Place a GCP service account key (JSON) in the mounted `/opt/airflow/` volume and update placeholders in `weather_etl_dag.py`.
3. **Run**:
   - Copy `weather_etl_dag.py` to the mounted DAGs folder and trigger the DAG via the Airflow UI.

## Challenges and Resolutions
- **Java Compatibility**: Initial Spark setup failed due to missing Java; resolved by setting `JAVA_HOME` to `/usr/lib/jvm/java-11-openjdk-amd64`.
- **Docker Issues**:
  - **Problem**: Faced port conflicts (e.g., 8080 already in use) and volume mounting errors when running the Airflow container on the VM.
  - **Solution**: Adjusted the Docker run command with proper port mapping (`-p 8080:8080`) and ensured the `/path/to/dags` volume was correctly mounted, resolving the issues.
- **API Data Accuracy**: The API returned future dates; implemented a filter for yesterday’s data to ensure relevance.

## Future Improvements
- Switch to hourly data for a true average temperature.
- Implement incremental loading (`WRITE_APPEND`) instead of `WRITE_TRUNCATE` for historical tracking.
- Add error logging to Airflow for better monitoring.

## Contributors
- Nithesh [https://github.com/Nithesh011]
