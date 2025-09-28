from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, sum, col, lit, max, min, round, concat, row_number
from pyspark.sql.window import Window
from google.cloud import storage, bigquery

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define DAG
with DAG(
    'weather_etl',
    default_args=default_args,
    description='A DAG to ETL Mumbai weather data',
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    def extract():
        try:
            url = "https://api.open-meteo.com/v1/forecast?latitude=19.07&longitude=72.88&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=Asia/Kolkata&past_days=3"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                with open('/tmp/weather_data.json', 'w') as f:
                    json.dump(data, f)
                client = storage.Client.from_service_account_json('/opt/airflow/subtle-seer-472708-q3-ba2b22424184.json')  # Replace with your key path
                bucket = client.get_bucket('myweather-data-backup')  # Replace with your bucket
                blob_name = f'weather_raw_{datetime.now().strftime("%Y-%m-%d")}.json'
                blob = bucket.blob(blob_name)
                blob.upload_from_string(json.dumps(data))
                print(f"Extracted and saved to GCS: {blob_name}")
            else:
                print("API error:", response.status_code)
                raise Exception("API request failed")
        except Exception as e:
            print(f"Extract error: {str(e)}")
            raise

    def transform():
        try:
            os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-11-openjdk-amd64'
            spark = SparkSession.builder.appName('WeatherETL').config("spark.driver.memory", "1g").config("spark.executor.memory", "1g").getOrCreate()
            df = spark.read.json('/tmp/weather_data.json')
            df_daily = df.selectExpr("explode(arrays_zip(daily.time, daily.temperature_2m_max, daily.temperature_2m_min, daily.precipitation_sum)) as daily_data")
            df_exploded = df_daily.select(
                col("daily_data.time").alias("date"),
                col("daily_data.temperature_2m_max").alias("max_temp"),
                col("daily_data.temperature_2m_min").alias("min_temp"),
                col("daily_data.precipitation_sum").alias("precipitation")
            )
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            df_exploded = df_exploded.filter(col("date") == yesterday)
            end_date = df_exploded.agg(max("date").alias("end_date")).collect()[0]["end_date"]
            analysis = df_exploded.agg(
                max("max_temp").alias("max_temp"),
                min("min_temp").alias("min_temp"),
                sum("precipitation").alias("total_precipitation")
            ).withColumn("city", lit("Mumbai")).withColumn("end_date", lit(end_date))
            window_spec = Window.orderBy(lit(1))
            analysis = analysis.withColumn("id", row_number().over(window_spec) - 1 + 1)
            analysis = analysis.select("id", "city", "max_temp", "min_temp", "total_precipitation", "end_date") \
                .withColumn("max_temp", concat(round(col("max_temp"), 2), lit("°C"))) \
                .withColumn("min_temp", concat(round(col("min_temp"), 2), lit("°C"))) \
                .withColumn("total_precipitation", concat(round(col("total_precipitation"), 2), lit(" mm")))
            analysis.coalesce(1).write.mode('overwrite').csv('/tmp/transformed_weather', header=True)
            print("Transformed!")
        except Exception as e:
            print(f"Transform error: {str(e)}")
            raise

    def load():
        try:
            client = bigquery.Client.from_service_account_json('/opt/airflow/subtle-seer-472708-q3-ba2b22424184.json')  # Replace with your key path
            dataset_id = 'weather_dataset'
            try:
                client.get_dataset(dataset_id)
            except:
                client.create_dataset(dataset_id)
            table_id = 'subtle-seer-472708-q3.weather_dataset.weather_analysis'  # Replace with your Project ID
            for file in os.listdir('/tmp/transformed_weather'):
                if file.startswith('part-') and file.endswith('.csv'):
                    csv_file = f'/tmp/transformed_weather/{file}'
                    break
            else:
                raise Exception("No CSV found in /tmp/transformed_weather")
            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.CSV,
                skip_leading_rows=1,
                autodetect=True,
                write_disposition='WRITE_TRUNCATE'
            )
            with open(csv_file, 'rb') as source_file:
                job = client.load_table_from_file(source_file, table_id, job_config=job_config)
            job.result()
            print("Loaded to BigQuery!")
        except Exception as e:
            print(f"Load error: {str(e)}")
            raise

    # Define tasks
    extract_task = PythonOperator(task_id='extract', python_callable=extract)
    transform_task = PythonOperator(task_id='transform', python_callable=transform)
    load_task = PythonOperator(task_id='load', python_callable=load)

    # Set task dependencies
    extract_task >> transform_task >> load_task
