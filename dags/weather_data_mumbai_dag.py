from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "Nithesh",
    "depends_on_past": False,           # correct key name
    "retries": 2,
    "retry_delay": timedelta(seconds=2), # corrected timedelta syntax
    "start_date": datetime(2025, 10, 25)
}

with DAG(
    dag_id="weather_data_mumbai",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False
) as dag:

    # 1️⃣ Extract task
    extract_task = BashOperator(
        task_id="extract_data_from_API",
        bash_command='python3 /opt/airflow/scripts/extract/extract_api_data.py'
    )

    # 2️⃣ PySpark transformation task
    pyspark_task = BashOperator(
        task_id='pyspark_data_transformation',
        bash_command='python3 /opt/airflow/scripts/pyspark/pyspark_data_clean.py'
    )

    # 3️⃣ BigQuery load task
    bigquery_task = BashOperator(
        task_id='load_data_to_bigquery',
        bash_command='python3 /opt/airflow/scripts/bigquery/bigquery_data_update.py'
    )

    # Set task sequence
    extract_task >> pyspark_task >> bigquery_task
