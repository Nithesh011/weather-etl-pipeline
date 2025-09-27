from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests, json, os
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, min, sum, col, lit
from google.cloud import bigquery, storage

def extract():
    try:
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        url = f"https://api.open-meteo.com/v1/forecast?latitude=19.07&longitude=72.88&hourly=temperature_2m,precipitation&timezone=Asia/Kolkata&past_days=1"  # Hourly data for yesterday
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code}")
        data = response.json()
        # Save to local temp file
        with open('/tmp/weather_data.json', 'w') as f:
            json.dump(data, f)
        # Save to GCS for backup
        client = storage.Client.from_service_account_json('your-key.json')  # Replace with your key
        bucket = client.get_bucket('your-bucket')  # Replace with your bucket
        blob_name = f'weather_raw_{datetime.now().strftime("%Y-%m-%d")}.json'
        blob = bucket.blob(blob_name)
        blob.upload_from_string(json.dumps(data))
        print(f"Extracted and saved to GCS: {blob_name}")
    except Exception as e:
        print(f"Extract error: {str(e)}")
        raise

def transform():
    try:
        os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-11-openjdk-amd64'
        spark = SparkSession.builder.appName('WeatherETL').config("spark.driver.memory", "1g").config("spark.executor.memory", "1g").getOrCreate()
        df = spark.read.json('/tmp/weather_data.json')
        df_hourly = df.selectExpr("explode(arrays_zip(hourly.time, hourly.temperature_2m, hourly.precipitation)) as hourly_data")
        df_exploded = df_hourly.select(
            col("hourly_data.time").alias("time"),
            col("hourly_data.temperature_2m").alias("temperature"),
            col("hourly_data.precipitation").alias("precipitation")
        )
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        df_filtered = df_exploded.filter(col("time").startswith(yesterday))  # Filter to yesterday's hours
        analysis = df_filtered.agg(
            avg("temperature").alias("avg_temperature"),
            min("temperature").alias("min_temperature"),
            sum("precipitation").alias("total_precipitation")
        ).withColumn("city", lit("Mumbai")).withColumn("date", lit(yesterday))
        analysis.coalesce(1).write.mode('overwrite').csv('/tmp/transformed_weather', header=True)
        print("Transformed!")
    except Exception as e:
        print(f"Transform error: {str(e)}")
        raise


def load():
    try:
        client = bigquery.Client.from_service_account_json('your-key.json')  # Replace with your key
        dataset_id = 'weather_dataset'
        try:
            client.get_dataset(dataset_id)
        except:
            client.create_dataset(dataset_id)
        table_id = 'your-project-id.weather_dataset.weather_analysis'  # Replace with your Project ID
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
            write_disposition='WRITE_APPEND'  # Append daily for history
        )
        with open(csv_file, 'rb') as source_file:
            job = client.load_table_from_file(source_file, table_id, job_config=job_config)
        job.result()
        print("Loaded!")
    except Exception as e:
        print(f"Load error: {str(e)}")
        raise

with DAG('weather_etl', start_date=datetime(2025, 1, 1), schedule_interval='@daily', catchup=False) as dag:
    extract_task = PythonOperator(task_id='extract', python_callable=extract)
    transform_task = PythonOperator(task_id='transform', python_callable=transform)
    load_task = PythonOperator(task_id='load', python_callable=load)
    extract_task >> transform_task >> load_task
