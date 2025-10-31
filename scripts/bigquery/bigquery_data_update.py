# bigquery_data_update.py
from google.cloud import bigquery
import glob
import os

# Environment variables
GCP_KEY_PATH = os.environ.get("GCP_KEY_PATH")
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
GCP_BUCKET_NAME = os.environ.get("GCP_BUCKET_NAME")
DATA_PATH = os.environ.get("DATA_PATH", "/opt/airflow/scripts")

# BigQuery parameters
dataset_id = "weather_dataset"
table_id = "Mumbai_weather_analysis"
csv_directory = os.path.join(DATA_PATH, "Transformed_weather_data")

# Define schema
Data_schema = [
    bigquery.SchemaField("Date", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("City", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("Max_temperature", "STRING"),
    bigquery.SchemaField("Min_temperature", "STRING"),
    bigquery.SchemaField("Avg_temperature", "STRING"),
    bigquery.SchemaField("Total_precipitation", "STRING"),
    bigquery.SchemaField("Avg_precipitation", "STRING")
]

# BigQuery client
client = bigquery.Client.from_service_account_json(GCP_KEY_PATH)

# Create dataset if not exists
try:
    client.get_dataset(dataset_id)
except:
    client.create_dataset(dataset_id)

table_ref = f"{GCP_PROJECT_ID}.{dataset_id}.{table_id}"

# Find CSV file
csv_file = glob.glob(os.path.join(csv_directory, "part-*.csv"))
if not csv_file:
    raise FileNotFoundError(f"No CSV found in {csv_directory}")
csv_file = csv_file[0]

# Load job config
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    schema=Data_schema,
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND
)

# Load CSV to BigQuery
with open(csv_file, 'rb') as f:
    job = client.load_table_from_file(f, table_ref, job_config=job_config)

job.result()
print(f"Appended data to {table_ref}")

