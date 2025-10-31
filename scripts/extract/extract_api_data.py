# extract_api_data.py
import requests
import json
import os
from google.cloud import storage
from datetime import datetime, timedelta

# Environment variables
GCP_KEY_PATH = os.environ.get("GCP_KEY_PATH")
GCP_BUCKET_NAME = os.environ.get("GCP_BUCKET_NAME")
DATA_PATH = os.environ.get("DATA_PATH", "/opt/airflow/scripts")  # default Docker path

# Calculate yesterday date
yesterday = datetime.now() - timedelta(days=1)
yesterday_date = yesterday.strftime('%Y-%m-%d')

# Location and timezone
latitude = 19.07
longitude = 72.88
timezone = "Asia/Kolkata"

# API URL
api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,precipitation&start_date={yesterday_date}&end_date={yesterday_date}&timezone={timezone}"

# Fetch data
result = requests.get(api_url)
if result.status_code == 200:
    data = result.json()
    
    # Save JSON locally
    local_file = os.path.join(DATA_PATH, f"weather_date-{yesterday_date}.json")
    with open(local_file, "w") as f:
        json.dump(data, f, indent=2)

    # Upload to GCS
    client = storage.Client.from_service_account_json(GCP_KEY_PATH)
    bucket = client.get_bucket(GCP_BUCKET_NAME)
    blob_name = f'weather_raw_{yesterday_date}.json'
    blob = bucket.blob(blob_name)
    blob.upload_from_string(json.dumps(data))
    print(f"Extracted and saved to GCS: {blob_name}")
else:
    print("Failed to fetch data:", result.status_code)

