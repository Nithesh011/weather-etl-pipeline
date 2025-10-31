
# Environment variables - how to set and where used

## Required environment variables (for Docker runtime)

- GCP_KEY_PATH — Absolute path inside container where service account JSON is mounted.
  Example: /opt/airflow/config/subtle-seer-...json

- GCP_BUCKET_NAME — GCS bucket used for raw JSON uploads.
  Example: raw_weather_data_backup

- GCP_PROJECT_ID — GCP project id for BigQuery.
  Example: subtle-seer-472708-q3

- DATA_PATH — Shared folder path for JSON & CSV inside container; scripts read/write here.
  Example: /opt/airflow/scripts

## How to pass with docker run
Example:
docker run -d --name weather_airflow -p 8080:8080 \
  -e GCP_KEY_PATH=/opt/airflow/config/<KEY>.json \
  -e GCP_BUCKET_NAME=raw_weather_data_backup \
  -e GCP_PROJECT_ID=subtle-seer-... \
  -e DATA_PATH=/opt/airflow/scripts \
  -v /home/<user>/weather-etl-pipeline:/opt/airflow:rw \
  -v /home/<user>/weather-etl-pipeline/config/<key>.json:/opt/airflow/config/<key>.json:ro \
  weather-etl-airflow

## Local / Colab testing
In Colab or local Python, set with os.environ[...] like:
import os
os.environ["GCP_KEY_PATH"] = "/content/config/<KEY>.json"
os.environ["GCP_BUCKET_NAME"] = "raw_weather_data_backup"
os.environ["GCP_PROJECT_ID"] = "my-project"
os.environ["DATA_PATH"] = "/content"
EOF
