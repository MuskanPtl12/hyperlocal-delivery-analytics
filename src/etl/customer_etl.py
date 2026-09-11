# import necessary user-defined modules
import re

import pandas as pd
from src.config import RAW_DATA_PATH
from src.config import PROCESSED_DATA_PATH, CUSTOMERS_FILE
from src.utils.file_loader import load_csv
from src.schema import CUSTOMER_FINAL_COLUMNS

# load customers data from raw data folder
def load_customers():
    zepto_customers_path = RAW_DATA_PATH /"zepto"/"zepto_customer.csv"
    blinkit_customers_path = RAW_DATA_PATH /"Blinkit"/"blinkit_customers.csv"
    swiggy_customers_path = RAW_DATA_PATH /"swiggy instamart"/"swiggy_customers.csv"
    swiggy_address_path = RAW_DATA_PATH /"swiggy instamart"/"swiggy_address.csv"
    zepto_df = load_csv(zepto_customers_path)
    blinkit_df = load_csv(blinkit_customers_path)
    swiggy_df = load_csv(swiggy_customers_path)
    swiggy_address_df = load_csv(swiggy_address_path)

    return zepto_df, blinkit_df, swiggy_df, swiggy_address_df

def validate_customers(zepto_df, blinkit_df, swiggy_df, swiggy_address_df):
    datasets = {
    "Zepto": zepto_df,
    "Blinkit": blinkit_df,
    "Swiggy": swiggy_df,
    "Swiggy Address": swiggy_address_df }
    
    # Validate that none of the DataFrames are empty
    for name, df in datasets.items():
        if df.empty:
            raise ValueError(f"{name} customer DataFrame is empty.")


def validate_source_schema(zepto_df, blinkit_df, swiggy_df, swiggy_address_df):

    zepto_required_columns = [
    'customer_id', 'city',
    'state', 'created_date']

    blinkit_required_columns = [
    'customer_id', 'address', 'area',
    'pincode', 'registration_date', 'customer_segment']
    
    swiggy_required_columns = [
    'CustomerID', 'AddressID',
    'CustomerSegment', 'RegistrationDate']
    
    swiggy_address_required_columns = [
    'AddressID', 'Pincode', 'StreetAddress',
    'CityName', 'StateName']
       
    
    # Validate that all required columns are present in each DataFrame
    for column in zepto_required_columns:
        if column not in zepto_df.columns:
            raise ValueError(f"Zepto DataFrame is missing required column: {column}") 
    for column in blinkit_required_columns:
        if column not in blinkit_df.columns:
            raise ValueError(f"Blinkit DataFrame is missing required column: {column}")
    for column in swiggy_required_columns:
        if column not in swiggy_df.columns:
            raise ValueError(f"Swiggy DataFrame is missing required column: {column}")
    for column in swiggy_address_required_columns:
        if column not in swiggy_address_df.columns:
            raise ValueError(f"Swiggy Address DataFrame is missing required column: {column}")

def merge_swiggy_customer_address(swiggy_df, swiggy_address_df):
    # Merge swiggy_df and swiggy_address_df on AddressID
    swiggy_df = pd.merge(swiggy_df, swiggy_address_df, on='AddressID', how='left')
    
    # Drop the AddressID column from the merged DataFrame
    swiggy_df = swiggy_df.drop(columns=['AddressID'])
    
    return swiggy_df

def standardize_columns(zepto_df, blinkit_df, swiggy_df):
    # Standardize column names across all DataFrames
    zepto_df = zepto_df.rename(columns={
        'customer_id': 'customer_id',
        'city': 'customer_city',
        'state': 'customer_state',
        'created_date': 'customer_registration_date'
    })

    blinkit_df = blinkit_df.rename(columns={
        'customer_id': 'customer_id',
        'address': 'customer_address',
        'area': 'customer_area',
        'pincode': 'customer_pincode',
        'registration_date': 'customer_registration_date',
        'customer_segment': 'customer_segment',
    })

    swiggy_df = swiggy_df.rename(columns={
        'CustomerID': 'customer_id',
        'CustomerSegment': 'customer_segment', 
        'RegistrationDate': 'customer_registration_date',
        'Pincode': 'customer_pincode',
        'StreetAddress': 'customer_address',
        'CityName': 'customer_city',
        'StateName': 'customer_state'
    })

    return zepto_df, blinkit_df, swiggy_df

def extract_city(blinkit_df):

    # Extract city from the address column
    blinkit_df['customer_city'] = (
        blinkit_df['customer_address']
        .str.extract(r'(?:,|\n)\s*([A-Za-z ]+?)[-\s]*\d{6}\s*$', expand=False)
        .str.strip()
    )
    return blinkit_df

def prepare_final_schema(zepto_df, blinkit_df, swiggy_df):
    """
    Prepare all CUSTOMERS DataFrames according to the final schema.
    """
    dataframes = {
        "Zepto": zepto_df,
        "Blinkit": blinkit_df,
        "Swiggy": swiggy_df }
    
    for platform, df in dataframes.items():
        # Add platform column
        df["platform"] = platform

        # Add missing columns
        for column in CUSTOMER_FINAL_COLUMNS:
            if column not in df.columns:
                df[column] = pd.NA

    return zepto_df, blinkit_df, swiggy_df


def reorder_columns(zepto_df, blinkit_df, swiggy_df):

    zepto_df = zepto_df[CUSTOMER_FINAL_COLUMNS]
    blinkit_df = blinkit_df[CUSTOMER_FINAL_COLUMNS]
    swiggy_df = swiggy_df[CUSTOMER_FINAL_COLUMNS]

    return zepto_df, blinkit_df, swiggy_df

def build_customers_dataset(zepto_df, blinkit_df, swiggy_df):

    #Append all Customers DataFrames into a single DataFrame.
    
    final_customers_df = pd.concat([zepto_df, blinkit_df, swiggy_df], ignore_index=True)
    
    return final_customers_df

def value_standardize(final_customers_df):
    """
    Standardize text values in the final customer DataFrame.
    """

    # Remove leading and trailing spaces
    text_columns = [
        "platform",
        "customer_city",
        "customer_state",
        "customer_segment"
    ]

    for column in text_columns:
        if column in final_customers_df.columns:
            final_customers_df[column] = final_customers_df[column].str.strip()

    # Apply Title Case where appropriate
    title_columns = [
        "platform",
        "customer_city",
        "customer_state",
        "customer_segment"
    ]

    for column in title_columns:
        if column in final_customers_df.columns:
            final_customers_df[column] = final_customers_df[column].str.title()

    # Standardize customer segment values
    segment_mapping = {
        "Premium": "High Value",
        "Regular": "Frequent Shopper",
        "New": "New User",
        "Lapsed": "Inactive" }

    final_customers_df["customer_segment"] = (
        final_customers_df["customer_segment"].replace(segment_mapping) )

    return final_customers_df

def standardize_data_types(final_customer_df):

    string_columns = [
        "platform",
        "customer_id",
        "customer_city",
        "customer_state",
        "customer_segment" ]

    int_columns = [
        "customer_pincode"  ]

    datetime_columns = [
        "customer_registration_date" ]

    # Convert into string columns
    for column in string_columns:
        if column in final_customer_df.columns:
            final_customer_df[column] = final_customer_df[column].astype("string")

    # Convert into integer columns
    for column in int_columns:
        if column in final_customer_df.columns:
            final_customer_df[column] = (
                pd.to_numeric(
                    final_customer_df[column],
                    errors="coerce"
                ).astype("Int64")
            )

    # Convert into datetime columns
    for column in datetime_columns:
        if column in final_customer_df.columns:
            final_customer_df[column] = pd.to_datetime(
                final_customer_df[column],
                format="%Y-%m-%d",
                errors="coerce"
            )

    return final_customer_df

# def validate(final_customers_df):
#     print(final_customers_df[final_customers_df["platform"] == "Blinkit"].value_counts("customer_segment"))


def validate_final_schema(final_customers_df,zepto_df, blinkit_df, swiggy_df):
    # Validate that the final DataFrame has the expected columns
    if list(final_customers_df.columns) != CUSTOMER_FINAL_COLUMNS:
        raise ValueError(
            f"Expected columns: {CUSTOMER_FINAL_COLUMNS}\n"
            f"Actual columns: {list(final_customers_df.columns)}" )
    
    # validate missing rows   
    expected = len(zepto_df) + len(blinkit_df) + len(swiggy_df)
    actual = len(final_customers_df)
    if expected != actual:
        raise ValueError(
            f"Row count mismatch. Expected {expected} rows but found {actual}." )
    
        
def save_customers(final_customers_df):
    """
    Save the cleaned customers dataset.
    """
    output_file = PROCESSED_DATA_PATH / CUSTOMERS_FILE

    final_customers_df.to_csv( output_file, index=False )

    print(f"Customers dataset saved successfully at:\n{output_file}")

def main():
    
    zepto_df, blinkit_df, swiggy_df, swiggy_address_df = load_customers()
    
    validate_customers(zepto_df, blinkit_df, swiggy_df, swiggy_address_df)
    
    validate_source_schema(zepto_df, blinkit_df, swiggy_df, swiggy_address_df)
    
    swiggy_df = merge_swiggy_customer_address(swiggy_df, swiggy_address_df)
    
    zepto_df, blinkit_df, swiggy_df = standardize_columns(zepto_df, blinkit_df, swiggy_df)
    
    blinkit_df = extract_city(blinkit_df)
    
    zepto_df, blinkit_df, swiggy_df = prepare_final_schema(zepto_df, blinkit_df, swiggy_df)
    
    zepto_df, blinkit_df, swiggy_df = reorder_columns(zepto_df, blinkit_df, swiggy_df)
    
    final_customers_df = build_customers_dataset(zepto_df, blinkit_df, swiggy_df)
    
    final_customers_df = value_standardize(final_customers_df)
    
    final_customers_df = standardize_data_types(final_customers_df)
    
    validate_final_schema(final_customers_df, zepto_df, blinkit_df, swiggy_df)
    
    save_customers(final_customers_df)
    
    
if __name__ == "__main__":
    main()
