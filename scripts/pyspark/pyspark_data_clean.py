# pyspark_data_clean.py
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from datetime import datetime, timedelta
import os

# Environment variable for data path
DATA_PATH = os.environ.get("DATA_PATH", "/opt/airflow/scripts")

# Spark session
spark = SparkSession.builder.appName("Weather_ETL")\
    .config("spark.driver.memory", "1g")\
    .config("spark.executor.memory", "1g").getOrCreate()

# Dates and city
yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y')
city = "Mumbai"

# Read JSON
json_file = os.path.join(DATA_PATH, f"weather_date-{(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')}.json")
df = spark.read.option("multiline", "True").json(json_file)

# Zip and explode hourly data
df_zip = df.select(F.arrays_zip('hourly.temperature_2m', 'hourly.precipitation').alias('zipped'))
df_explode = df_zip.select(F.explode('zipped').alias("row"))
df_clean = df_explode.select(F.col('row.temperature_2m'), F.col('row.precipitation'))

# Aggregations
df_transform = df_clean.agg(
    F.round(F.max('temperature_2m'), 2).alias('Max_temperature'),
    F.round(F.min('temperature_2m'), 2).alias('Min_temperature'),
    F.round(F.avg('temperature_2m'), 2).alias('Avg_temperature'),
    F.round(F.sum('precipitation'), 2).alias('Total_precipitation'),
    F.round(F.avg('precipitation'), 2).alias('Avg_precipitation')
)

# Add metadata and units
df_final = df_transform \
    .withColumn('Date', F.lit(yesterday_date)) \
    .withColumn('City', F.lit(city)) \
    .withColumn('Max_temperature', F.concat(F.col('Max_temperature'), F.lit('°C'))) \
    .withColumn('Min_temperature', F.concat(F.col('Min_temperature'), F.lit('°C'))) \
    .withColumn('Avg_temperature', F.concat(F.col('Avg_temperature'), F.lit('°C'))) \
    .withColumn('Total_precipitation', F.concat(F.col('Total_precipitation'), F.lit('mm'))) \
    .withColumn('Avg_precipitation', F.concat(F.col('Avg_precipitation'), F.lit('mm'))) \
    .select('Date','City','Max_temperature','Min_temperature','Avg_temperature',
            'Total_precipitation','Avg_precipitation')

# Write CSV
output_dir = os.path.join(DATA_PATH, "Transformed_weather_data")
df_final.coalesce(1).write.mode('overwrite').option('header', True).csv(output_dir)
print("Transformed!")

