
from pathlib import Path
import pandas as pd
from database import initialize_database, load_dataframe

# Locate the project folder
project_dir = Path(__file__).resolve().parent.parent

# Define output directory for the summary files
output_dir = project_dir / "data" / "processed"


def load_data():
    """Load raw sales data from the CSV file."""
    file_path = project_dir / "data" / "raw_sales.csv"
    df = pd.read_csv(file_path)
    return df




def validate_data(df):
    """Validate sales records and separate valid and rejected rows."""

    # Work on a copy so the original DataFrame remains unchanged
    df = df.copy()

    # Preserve original dates before converting them
    raw_transaction_date = df["transaction_date"].copy()

    # Convert dates into datetime values
    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        errors="coerce"
    )

    # Check for duplicate transaction IDs
    duplicate_id = df.duplicated(
        subset=["transaction_id"],
        keep=False
    )

    # Check for missing required fields
    required_fields = [
        "transaction_id",
        "product",
        "quantity",
        "unit_price",
        "city",
    ]

    missing_required = (
        df[required_fields].isna().any(axis=1)
        |
        df[required_fields]
        .astype("string")
        .apply(lambda column: column.str.strip().eq(""))
        .any(axis=1)
        |
        raw_transaction_date.isna()
        |
        raw_transaction_date.astype("string").str.strip().eq("")
    )

    # Check for invalid quantities
    invalid_quantity = (
        df["quantity"].notna()
        & (df["quantity"] <= 0)
    )

    # Check for missing or negative unit prices
    invalid_price = (
        df["unit_price"].isna()
        | (df["unit_price"] < 0)
    )

    # Check for invalid dates
    invalid_date = df["transaction_date"].isna()

    # Prepare rejection reasons
    reasons = pd.Series("", index=df.index, dtype="string")

    checks = [
        (duplicate_id, "Duplicate transaction ID"),
        (missing_required, "Missing required field"),
        (invalid_quantity, "Invalid quantity"),
        (invalid_price, "Invalid unit price"),
        (invalid_date, "Invalid transaction date"),
    ]

    for mask, reason in checks:
        reasons.loc[mask] = reasons.loc[mask].apply(
            lambda existing: (
                f"{existing}; {reason}" if existing else reason
            )
        )

    # Separate valid and rejected records
    rejected_mask = reasons.ne("")

    valid_df = df.loc[~rejected_mask].copy()
    rejected_df = df.loc[rejected_mask].copy()

    # Attach rejection reasons
    rejected_df["rejection_reason"] = reasons.loc[rejected_mask]

    # Return both DataFrames to the caller
    return valid_df, rejected_df



def transform_data(valid_df):
    """Calculate total sales for each valid transaction."""

    valid_df = valid_df.copy()

    valid_df["total_sales"] = (
        valid_df["quantity"] * valid_df["unit_price"]
    )

    return valid_df



def save_data(valid_df, rejected_df):
    """Save valid and rejected records to processed CSV files."""

    # Create the directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save valid and rejected records
    valid_df.to_csv(output_dir / "valid_sales.csv", index=False)
    rejected_df.to_csv(output_dir / "rejected_sales.csv", index=False)

    print("\nValid and rejected records saved successfully.")


def create_product_summary(valid_df):
    """Calculate total sales for each product."""

    product_summary = (
        valid_df.groupby("product", as_index=False)["total_sales"]
        .sum()
    )

    return product_summary



def create_city_summary(valid_df):
    """Calculate total sales for each city."""

    city_summary = (
        valid_df.groupby("city", as_index=False)["total_sales"]
        .sum()
    )

    return city_summary


def create_city_transaction_count(valid_df):
    """Count valid transactions for each city."""

    city_transaction_count = (
        valid_df.groupby("city", as_index=False)["transaction_id"]
        .count()
        .rename(columns={"transaction_id": "transaction_count"})
    )

    return city_transaction_count




# Load raw sales data
df = load_data()

# Validate the data
valid_df, rejected_df = validate_data(df)

# Transform valid sales data
valid_df = transform_data(valid_df)


# Display validation results
print("\nFinal validation results:")
print("Input rows:", len(df))
print("Valid rows:", len(valid_df))
print("Rejected rows:", len(rejected_df))

print("\nRejected records:")
print(rejected_df[["transaction_id", "rejection_reason"]])




# Save valid and rejected records
save_data(valid_df, rejected_df)





# Create product-level sales summary
product_summary = create_product_summary(valid_df)

# Save product-level sales summary
product_summary.to_csv(
    output_dir / "product_sales_summary.csv",
    index=False
)

print("\nProduct summary saved successfully.")





# Create city-level sales summary
city_summary = create_city_summary(valid_df)

print("\nTotal sales by city:")
print(city_summary)

# Save city-level sales summary
city_summary.to_csv(
    output_dir / "city_sales_summary.csv",
    index=False
)

print("\nCity summary saved successfully.")





# Create valid transaction counts by city
city_transaction_count = create_city_transaction_count(valid_df)

print("\nValid transaction count by city:")
print(city_transaction_count)

# Save transaction counts by city
city_transaction_count.to_csv(
    output_dir / "city_transaction_count.csv",
    index=False
)

print("\nTransaction count saved successfully.")




# Initialize the database and create tables
initialize_database()

# Load valid and rejected records into separate tables
load_dataframe(valid_df, "sales")
load_dataframe(rejected_df, "rejected_sales")

print("\nValid and rejected records loaded into SQLite successfully.")
