from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Processed Output Files
ORDERS_FILE = "clean_orders.csv"
CUSTOMERS_FILE = "clean_customers.csv"
PRODUCTS_FILE = "clean_products.csv"
DELIVERIES_FILE = "clean_deliveries.csv"
RATING_FILE = "clean_ratings.csv"


# Data Folder
DATA_PATH = PROJECT_ROOT / "data"

# Raw Data
RAW_DATA_PATH = DATA_PATH / "raw"

# Processed Data
PROCESSED_DATA_PATH = DATA_PATH / "processed"

# External Data
EXTERNAL_DATA_PATH = DATA_PATH / "external"

