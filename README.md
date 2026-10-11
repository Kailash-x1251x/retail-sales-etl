# Retail Sales ETL Pipeline

## Project Overview

This project demonstrates an end-to-end ETL (Extract, Transform, Load) pipeline using Python, pandas, and SQLite.

The pipeline processes retail sales data from a CSV file, performs data quality checks, separates valid and rejected records, generates sales summaries, and loads the processed data into a SQLite database.

## Project Objectives

- Extract retail sales data from a CSV file.
- Validate records and identify data quality issues.
- Transform valid data into useful sales summaries.
- Save processed data and reports as CSV files.
- Load valid and rejected records into SQLite tables.

## Technologies Used

- **Python** — pipeline implementation
- **pandas** — data processing and transformation
- **SQLite** — local relational database
- **SQL** — querying and analyzing sales data
- **Git and GitHub** — version control and project hosting

## Project Structure

```text
retail-sales-etl/
├── data/
│   ├── raw_sales.csv
│   └── processed/
│       ├── valid_sales.csv
│       ├── rejected_sales.csv
│       ├── product_sales_summary.csv
│       ├── city_sales_summary.csv
│       └── city_transaction_count.csv
├── src/
│   ├── main.py
│   ├── database.py
│   └── test_database.py
├── .gitignore
└── README.md
```

## ETL Workflow

1. **Extract:** Read the raw retail sales data from a CSV file.
2. **Validate:** Identify duplicate transactions, missing values, invalid dates, and invalid quantities.
3. **Transform:** Separate valid and rejected records and calculate sales summaries.
4. **Load:** Save processed outputs as CSV files and load the valid and rejected records into SQLite tables.

## Data Quality Handling

The pipeline identifies records that fail validation and separates them from valid records. This helps prevent invalid data from being included in sales analysis.

## Database

The pipeline uses SQLite and maintains two tables:

- `sales` — valid sales records
- `rejected_sales` — records rejected during validation

## Generated Reports

- `valid_sales.csv` — validated sales records
- `rejected_sales.csv` — rejected records
- `product_sales_summary.csv` — sales summarized by product
- `city_sales_summary.csv` — sales summarized by city
- `city_transaction_count.csv` — transaction counts by city

## How to Run

1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install pandas.
4. Run the pipeline using `src/main.py`.

Detailed commands and setup instructions will be added as the project is finalized.
