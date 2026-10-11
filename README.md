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

The project uses SQLite for local storage. The database file is created at `data/retail_sales.db` when the pipeline runs.

Two tables are maintained:

- `sales` — validated sales records, including the calculated `total_sales` field.
- `rejected_sales` — records that fail validation, including their rejection reasons.

Before loading each dataset, the pipeline clears the existing records from the corresponding table and inserts the current run's records.

The SQLite database file is generated locally and is not tracked in Git.

## Generated Reports

- `valid_sales.csv` — validated sales records
- `rejected_sales.csv` — rejected records
- `product_sales_summary.csv` — sales summarized by product
- `city_sales_summary.csv` — sales summarized by city
- `city_transaction_count.csv` — transaction counts by city

## How to Run

### Prerequisites

- Python 3.12 or a compatible Python 3 version
- pip (Python package installer)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Kailash-x1251x/retail-sales-etl.git
   cd retail-sales-etl
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   ```

3. Activate the virtual environment (macOS/Linux):

   ```bash
   source .venv/bin/activate
   ```

4. Install the required dependency:

   ```bash
   python -m pip install pandas
   ```

### Run the Pipeline

Execute the following command from the project root:

```bash
python src/main.py
```

The pipeline reads `data/raw_sales.csv`, validates and transforms the records, generates CSV reports in `data/processed/`, and loads valid and rejected records into the SQLite database.

### Output

Generated CSV files are saved in `data/processed/`. The SQLite database is created locally in the `data/` directory.

