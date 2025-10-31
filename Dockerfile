# -------------------------------
# Base image with Python + Airflow
# -------------------------------
FROM apache/airflow:2.9.1-python3.10

# Switch to root to install system dependencies (Java)
USER root

# Install OpenJDK 17 (required for PySpark)
RUN apt-get update && apt-get install -y openjdk-17-jdk && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set Java environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Copy project files into Airflow home directory
WORKDIR /opt/airflow
COPY . .

# Change file permissions so the airflow user can read/write
RUN chmod -R 777 /opt/airflow

# Switch back to airflow user
USER airflow

# Install Python dependencies as airflow user (✅ correct way)
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Environment variables for GCP and scripts
ENV AIRFLOW_HOME=/opt/airflow
ENV GCP_KEY_PATH=/opt/airflow/config/<your-key>.json
ENV GCP_BUCKET_NAME=raw_weather_data_backup
ENV GCP_PROJECT_ID=your-project-id
ENV DATA_PATH=/opt/airflow/scripts

# Default command
ENTRYPOINT ["airflow"]
CMD ["standalone"]
