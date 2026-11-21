# 🏏 Cricket Performance and Analytics

### An End-to-End Data Engineering and Business Intelligence Platform

## 📌 Project Overview
Cricket Performance and Analytics is an end-to-end data engineering and business intelligence project that analyzes IPL ball-by-ball match data to identify batting trends, bowling performance, team results, and venue-based scoring patterns.

The project uses Python, Apache Spark, Databricks, Delta Lake, and Microsoft Power BI to transform raw cricket data into meaningful analytical insights.

## 🎯 Objectives
- Analyze IPL batting and bowling performance.
- Compare team wins, losses, and winning percentages.
- Explore venue-wise scoring patterns.
- Perform data extraction, cleaning, and transformation.
- Implement the Medallion Architecture.
- Build interactive Power BI dashboards.

## 🛠️ Technology Stack
- Python – Data extraction and preprocessing
- Apache Spark / PySpark – Data processing
- Databricks – Cloud data engineering platform
- Delta Lake – Data storage
- Microsoft Power BI – Interactive dashboards
- GitHub – Project version control and documentation

## 🏗️ Data Engineering Architecture
The project follows the Medallion Architecture:

1. **Bronze Layer:** Ingestion of raw cricket datasets.
2. **Silver Layer:** Data cleaning, validation, and transformation.
3. **Gold Layer:** Analytical aggregations for business intelligence.

## 📂 Repository Structure

```text
Cricket-Analytics/
│
├── extraction/
│   ├── extract_data.py
│   ├── extract_matches.py
│   └── README.md
│
├── notebooks/
│   ├── 01_Bronze_Cricket_Ingestion.py
│   ├── 02_Silver_Cricket_Cleaning.py
│   ├── 03_Gold_Cricket_Analytics.py
│   └── README.md
│
├── dashboard/
│   ├── Cricket_Analytics_Dashboard.pbix
│   ├── powerbi_data/
│   │   ├── gold_batting_stats.csv
│   │   ├── gold_bowling_stats.csv
│   │   ├── gold_team_innings.csv
│   │   ├── gold_venue_stats.csv
│   │   ├── gold_phase_analysis.csv
│   │   └── gold_team_performance.csv
│   └── README.md
│
├── docs/
│   └── README.md
│
└── README.md
```

## 📊 Power BI Dashboard

The interactive dashboard contains four analytical sections:

- Season Overview
- Batting Analytics
- Bowling Analytics
- Team & Venue Analytics

## 📂 Dataset Source

Cricsheet IPL ball-by-ball JSON data.

Source: https://cricsheet.org/

## 👥 Project Team

**Project Title:** Cricket Performance and Analytics: An End-to-End Data Engineering and Business Intelligence Platform

**Team Name:** Team Cloud Crusaders

## 🚀 Expected Outcome

The project transforms raw IPL cricket data into structured analytical datasets and interactive visualizations, supporting data-driven exploration of player, team, season, and venue performance.
