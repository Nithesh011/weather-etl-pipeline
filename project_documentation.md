# Project Documentation: Dynamic Weather ETL Pipeline

## Project Overview
This project develops an ETL pipeline to process daily weather data for Mumbai, India, using the Open-Meteo API, PySpark, Apache Airflow, Google Cloud Storage (GCS), and Google BigQuery. The pipeline extracts the previous day's weather data, transforms it into aggregated metrics (maximum and minimum temperatures, total precipitation), and loads the results into a BigQuery table, scheduled to run daily on a GCP virtual machine.

## Technical Details
- **Tools and Technologies**:
  - **Open-Meteo API**: Source of weather data.
  - **PySpark**: For data transformation and aggregation.
  - **Airflow**: For workflow orchestration.
  - **GCS**: For raw data backup.
  - **BigQuery**: For data storage and analysis.
- **Data Flow**:
  1. Extract: Fetch data and save to GCS.
  2. Transform: Filter to yesterday, compute metrics.
  3. Load: Append to BigQuery.

## Setup and Deployment
1. **Environment Setup**:
   - Deploy a GCP VM (e.g., e2-medium).
   - Install Python, Airflow, and required libraries (`pip install pyspark requests google-cloud-storage google-cloud-bigquery`).
2. **Configuration**:
   - Place a GCP service account key (JSON) in `/opt/airflow/` and update placeholders in `weather_etl_dag.py`.
3. **Run**:
   - Copy `weather_etl_dag.py` to the Airflow DAGs folder and start services.

## Challenges and Resolutions
- **Java Compatibility**: Initial Spark setup failed due to missing Java; resolved by setting `JAVA_HOME` to `/usr/lib/jvm/java-11-openjdk-amd64`.
- **Docker Issues**:
  - **Problem**: Attempted to use Docker for Airflow but faced port conflicts (e.g., 8080) and volume mounting errors on the VM.
  - **Solution**: Abandoned Docker, opted for a manual Airflow installation with `pip` and system services, ensuring compatibility with the GCP VM.
- **API Data Accuracy**: The API returned future dates; implemented a filter for yesterday’s data to ensure relevance.

## Future Improvements
- Switch to hourly data for a true average temperature.
- Implement incremental loading (`WRITE_APPEND`) instead of `WRITE_TRUNCATE` for historical tracking.
- Add error logging to Airflow for better monitoring.

## Contributors
- Nithesh [https://github.com/Nithesh011]
