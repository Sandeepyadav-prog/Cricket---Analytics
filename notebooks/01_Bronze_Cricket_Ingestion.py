# Databricks notebook source
file_path = "/Volumes/workspace/default/cricket_raw/deliveries.csv"

df = spark.read.option("header", True).option("inferSchema", True).csv(file_path)

display(df.limit(10))

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

# Add ingestion metadata
bronze_df = (
    df.withColumn("ingestion_timestamp", current_timestamp())
      .withColumn("source_file", lit("deliveries.csv"))
)

# Save as a Delta table
bronze_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.default.bronze_cricket_deliveries")

print("BRONZE LAYER CREATED SUCCESSFULLY!")

print("Total records:", bronze_df.count())

display(bronze_df.limit(10))