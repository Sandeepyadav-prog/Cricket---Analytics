# Databricks notebook source

# Load data from Bronze Delta table
bronze_df = spark.table(
    "workspace.default.bronze_cricket_deliveries"
)

# Check total records
print("BRONZE DATA LOADED SUCCESSFULLY!")
print("Total Bronze Records:", bronze_df.count())

# Display first 10 records
display(bronze_df.limit(10))


# COMMAND ----------


from pyspark.sql.functions import col, trim

# Start with Bronze data
silver_df = bronze_df

# 1. Remove duplicate deliveries
silver_df = silver_df.dropDuplicates(
    ["match_id", "innings", "over", "ball"]
)

# 2. Remove records with missing essential values
silver_df = silver_df.filter(
    col("match_id").isNotNull() &
    col("batter").isNotNull() &
    col("bowler").isNotNull() &
    col("batting_team").isNotNull() &
    col("bowling_team").isNotNull()
)

# 3. Remove invalid negative run values
silver_df = silver_df.filter(
    (col("batter_runs") >= 0) &
    (col("extras") >= 0) &
    (col("total_runs") >= 0)
)

# 4. Clean text columns
for column_name in [
    "batter", "bowler", "batting_team", "bowling_team"
]:
    silver_df = silver_df.withColumn(
        column_name,
        trim(col(column_name))
    )

# 5. Display cleaning results
print("SILVER DATA CLEANING COMPLETED!")
print("Original Bronze records:", bronze_df.count())
print("Clean Silver records:", silver_df.count())
print(
    "Records removed:",
    bronze_df.count() - silver_df.count()
)

display(silver_df.limit(10))


# COMMAND ----------


# Save cleaned data as a Delta table
silver_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.default.silver_cricket_deliveries")

print("====================================")
print("SILVER DELTA TABLE CREATED!")
print("====================================")

print(
    "Total Silver Records:",
    spark.table(
        "workspace.default.silver_cricket_deliveries"
    ).count()
)
