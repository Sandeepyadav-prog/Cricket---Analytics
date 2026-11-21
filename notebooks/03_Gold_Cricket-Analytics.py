# Databricks notebook source

silver_df = spark.table(
    "workspace.default.silver_cricket_deliveries"
)

print("GOLD LAYER: SOURCE DATA LOADED")
print("Total records:", silver_df.count())

display(silver_df.limit(10))


# COMMAND ----------


from pyspark.sql.functions import (
    col, sum, count, countDistinct, avg, max, when, round
)

gold_batting = silver_df.groupBy(
    "season", "batter"
).agg(
    sum("batter_runs").alias("total_runs"),
    count("*").alias("delivery_records"),
    sum(when(col("batter_runs") == 4, 1).otherwise(0)).alias("fours"),
    sum(when(col("batter_runs") == 6, 1).otherwise(0)).alias("sixes"),
    sum(when(col("player_out") == col("batter"), 1).otherwise(0)).alias("dismissals")
).withColumn(
    "runs_per_100_delivery_records",
    round(
        col("total_runs") * 100 / 
        when(col("delivery_records") > 0, col("delivery_records")),
        2
    )
)

gold_batting.write.format("delta").mode("overwrite").saveAsTable(
    "workspace.default.gold_batting_stats"
)

print("GOLD BATTING TABLE CREATED!")
display(gold_batting.orderBy(col("total_runs").desc()).limit(20))


# COMMAND ----------


gold_team = silver_df.groupBy(
    "match_id",
    "season",
    "date",
    "venue",
    "batting_team",
    "innings"
).agg(
    sum("total_runs").alias("innings_total_runs"),
    count("*").alias("delivery_records"),
    sum("is_wicket").alias("wickets_lost")
)

gold_team.write.format("delta").mode("overwrite").saveAsTable(
    "workspace.default.gold_team_innings"
)

print("GOLD TEAM INNINGS TABLE CREATED!")
display(gold_team.orderBy(col("innings_total_runs").desc()).limit(20))


# COMMAND ----------


gold_venue = gold_team.groupBy(
    "venue"
).agg(
    countDistinct("match_id").alias("matches_played"),
    round(avg("innings_total_runs"), 2).alias("average_innings_score"),
    max("innings_total_runs").alias("highest_innings_score")
)

gold_venue.write.format("delta").mode("overwrite").saveAsTable(
    "workspace.default.gold_venue_stats"
)

print("GOLD VENUE TABLE CREATED!")
display(gold_venue.orderBy(col("average_innings_score").desc()))


# COMMAND ----------

spark.sql("SHOW TABLES IN workspace.default").show(truncate=False)

# COMMAND ----------


from pyspark.sql.functions import sum, col, count

gold_bowling = silver_df.groupBy(
    "season", "bowler"
).agg(
    sum("is_wicket").alias("wickets"),
    sum("total_runs").alias("runs_conceded"),
    count("*").alias("delivery_records")
)

gold_bowling.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.default.gold_bowling_stats")

print("GOLD BOWLING TABLE CREATED!")

display(
    gold_bowling.orderBy(
        col("wickets").desc()
    ).limit(20)
)


# COMMAND ----------


from pyspark.sql.functions import (
    when, col, sum, count, round
)

# Classify each delivery into match phases
phase_df = silver_df.withColumn(
    "match_phase",
    when(col("over").between(0, 5), "Powerplay")
    .when(col("over").between(6, 14), "Middle Overs")
    .when(col("over").between(15, 19), "Death Overs")
    .otherwise("Other")
)

# Calculate phase-wise performance
gold_phase = phase_df.groupBy(
    "season",
    "batting_team",
    "match_phase"
).agg(
    sum("total_runs").alias("total_runs"),
    sum("is_wicket").alias("total_wickets"),
    count("*").alias("delivery_records"),
    round(
        sum("total_runs") / count("*"),
        2
    ).alias("runs_per_delivery_record")
)

# Save Gold table
gold_phase.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.default.gold_phase_analysis")

print("MATCH PHASE ANALYSIS CREATED!")

display(gold_phase.orderBy("season", "batting_team", "match_phase"))


# COMMAND ----------


# Read match-level CSV data
matches_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("/Volumes/workspace/default/cricket_raw/matches.csv")
)

print("MATCH DATA LOADED SUCCESSFULLY!")
print("Total matches:", matches_df.count())

display(matches_df.limit(10))


# COMMAND ----------


matches_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.default.bronze_cricket_matches")

print("MATCH DATA SAVED AS DELTA TABLE!")


# COMMAND ----------


from pyspark.sql.functions import (
    col, lit, when, sum, round, trim, lower
)

# Load match-level data
matches_df = spark.table(
    "workspace.default.bronze_cricket_matches"
)

# Create records for Team 1
team1 = matches_df.select(
    col("season"),
    col("team1").alias("team"),
    col("winner"),
    col("result_type")
)

# Create records for Team 2
team2 = matches_df.select(
    col("season"),
    col("team2").alias("team"),
    col("winner"),
    col("result_type")
)

# Combine both teams
team_matches = team1.unionByName(team2)

# Remove missing team names
team_matches = team_matches.filter(
    col("team").isNotNull() &
    (trim(col("team")) != "")
)

# Calculate match outcomes
team_matches = (
    team_matches
    .withColumn(
        "win",
        when(col("winner") == col("team"), 1).otherwise(0)
    )
    .withColumn(
        "tie",
        when(lower(trim(col("result_type"))) == "tie", 1).otherwise(0)
    )
    .withColumn(
        "no_result",
        when(
            lower(trim(col("result_type"))).isin(
                "no result", "no_result", "draw"
            ), 1
        ).otherwise(0)
    )
    .withColumn(
        "loss",
        when(
            (col("winner").isNotNull()) &
            (trim(col("winner")) != "") &
            (col("winner") != col("team")),
            1
        ).otherwise(0)
    )
)

print("TEAM MATCH RECORDS PREPARED!")
display(team_matches.limit(10))


# COMMAND ----------



gold_team_performance = team_matches.groupBy(
    "season", "team"
).agg(
    sum(lit(1)).alias("matches_recorded"),
    sum("win").alias("wins"),
    sum("loss").alias("losses"),
    sum("tie").alias("ties"),
    sum("no_result").alias("no_results")
)

gold_team_performance = (
    gold_team_performance
    .withColumn(
        "decisive_matches",
        col("wins") + col("losses")
    )
    .withColumn(
        "win_percentage",
        round(
            when(
                col("decisive_matches") > 0,
                col("wins") * 100 / col("decisive_matches")
            ).otherwise(0),
            2
        )
    )
)

gold_team_performance.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.default.gold_team_performance")

print("TEAM PERFORMANCE TABLE CREATED!")

display(
    gold_team_performance.orderBy(
        col("win_percentage").desc()
    )
)


# COMMAND ----------

spark.table(
    "workspace.default.gold_team_performance"
).show(30, truncate=False)

# COMMAND ----------


export_path = "/Volumes/workspace/default/cricket_raw/powerbi_exports"

dbutils.fs.mkdirs(export_path)

print("POWER BI EXPORT FOLDER CREATED!")


# COMMAND ----------


# Export batting analytics
batting_df = spark.table(
    "workspace.default.gold_batting_stats"
)

batting_df.coalesce(1).write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(export_path + "/gold_batting_stats")

print("BATTING DATA EXPORTED SUCCESSFULLY!")


# COMMAND ----------


gold_tables = [
    "gold_bowling_stats",
    "gold_team_innings",
    "gold_venue_stats",
    "gold_phase_analysis",
    "gold_team_performance"
]

for table_name in gold_tables:
    table_df = spark.table(
        "workspace.default." + table_name
    )

    table_df.coalesce(1).write \
        .mode("overwrite") \
        .option("header", True) \
        .csv(export_path + "/" + table_name)

    print(table_name, "exported successfully!")

print("ALL GOLD TABLES EXPORTED!")
