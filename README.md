# supply-chain-inventory-analytics
End-to-End Supply Chain &amp; Inventory Analytics Pipeline built with Python, SQL, and Streamlit.
# 📦 Supply Chain & Inventory Analytics Pipeline

An end-to-end operational analytics solution designed to process daily warehouse inventory data, track order fulfillment, and trigger automated stockout risk alerts.

## 🎯 Business Problem
Warehouse operations often suffer from poor inventory visibility, leading to unpredicted stockouts or excess holding costs. This project automates data ingestion, processes warehouse metrics, and surfaces actionable KPIs for operational teams.

## 🛠️ Tech Stack & Architecture
- **Language:** Python 3.x (Pandas, NumPy, SQLAlchemy)
- **Database:** SQLite / SQL (CTEs, Window Functions, Aggregations)
- **Interface:** Streamlit (Web Dashboard)
- **Data Architecture:** Relative project-based ingestion (`data/` directory pipeline)

## 📁 Project Structure
```text
supply-chain-inventory-analytics/
│
├── data/                       # Operational CSV datasets
│   ├── products.csv
│   ├── inventory.csv
│   └── orders.csv
│
├── scripts/                    # Core logic and queries
│   ├── etl_pipeline.py         # Data cleaning & SQLite ingestion
│   └── analysis_queries.sql    # Analytical SQL queries (KPIs)
│
├── app.py                      # Streamlit dashboard interface
├── requirements.txt            # Python dependencies
└── README.md
