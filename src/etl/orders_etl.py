# import necessary user-defined modules
import pandas as pd
from pandas import col
from src.config import RAW_DATA_PATH
from src.config import PROCESSED_DATA_PATH, ORDERS_FILE
from src.utils.file_loader import load_csv
from src.schema import ORDERS_FINAL_COLUMNS

# load orders data from raw data folder
def load_orders():
    zepto_orders_path = RAW_DATA_PATH /"zepto"/"zepto_order.csv"
    blinkit_orders_path = RAW_DATA_PATH /"Blinkit"/"blinkit_orders.csv"
    swiggy_orders_path = RAW_DATA_PATH /"swiggy instamart"/"swiggy_order.csv"
    zepto_df = load_csv(zepto_orders_path)
    blinkit_df = load_csv(blinkit_orders_path)
    swiggy_df = load_csv(swiggy_orders_path)

    return zepto_df, blinkit_df, swiggy_df

def validate_orders(zepto_df, blinkit_df, swiggy_df):
    datasets = {
    "Zepto": zepto_df,
    "Blinkit": blinkit_df,
    "Swiggy": swiggy_df, }
    
    # Validate that none of the DataFrames are empty
    for name, df in datasets.items():
        if df.empty:
            raise ValueError(f"{name} orders DataFrame is empty.")
        

def validate_source_schema(zepto_df, blinkit_df, swiggy_df):

    zepto_required_columns = [
        "order_id",
        "customer_id",
        "order_date",
        "order_status"
    ]

    blinkit_required_columns = [
        "order_id",
        "customer_id",
        "order_date",
        "promised_delivery_time",
        "actual_delivery_time",
        "delivery_status",
        "order_total",
        "payment_method",
        "delivery_partner_id",
        "store_id"
    ]
    
    swiggy_required_columns = [
        "OrderID",
        "CustomerID",
        "ProductID",
        "StoreID",
        "DeliveryPartnerID",
        "OrderDate",
        "DeliveryDate",
        "Quantity",
        "TotalPrice",
        "DiscountApplied",
        "DeliveryTimeMinutes",
        "OrderStatus",
        "PaymentMethodID",
        "TimeOfDay"
    ]
    
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
        
    
def standardize_columns(zepto_df, blinkit_df, swiggy_df):
    """
    Standardize column names according to the project's
    Data Modeling schema.
    """
    # Rename columns to match the project standard
    zepto_df.rename(columns={ "order_date": "order_datetime", }, inplace=True )
    
    blinkit_df.rename(
        columns={
            "promised_delivery_time": "promised_delivery_datetime",
            "actual_delivery_time": "actual_delivery_datetime",
            "order_date": "order_datetime",
            "order_total": "order_value",
        },
        inplace=True )
    
    swiggy_df.rename(
        columns={
            "OrderID": "order_id",
            "CustomerID": "customer_id",
            "ProductID": "product_id",
            "StoreID": "store_id",
            "DeliveryPartnerID": "delivery_partner_id",
            "OrderDate": "order_datetime",
            "DeliveryDate": "delivery_datetime",
            "Quantity": "quantity",
            "TotalPrice": "order_value",
            "DiscountApplied": "discount_applied",
            "DeliveryTimeMinutes": "delivery_time_minutes",
            "OrderStatus": "order_status",
            "PaymentMethodID": "payment_method_id",
            "TimeOfDay": "time_of_day"
        },
        inplace=True )
    
    return zepto_df, blinkit_df, swiggy_df

def standardize_values(zepto_df, blinkit_df, swiggy_df):

    # Standardize Zepto order_status
    zepto_df["order_status"] = (
        zepto_df["order_status"]
        .str.strip()
        .str.title()
    )

    # Standardize Swiggy order_status
    swiggy_df["order_status"] = (
        swiggy_df["order_status"]
        .str.strip()
        .str.title())

    return zepto_df, blinkit_df, swiggy_df

                
def prepare_final_schema(zepto_df, blinkit_df, swiggy_df):
    """
    Prepare all Orders DataFrames according to the final schema.
    """
    dataframes = {
        "Zepto": zepto_df,
        "Blinkit": blinkit_df,
        "Swiggy": swiggy_df }

    for platform, df in dataframes.items():
        # Add platform column
        df["platform"] = platform

        # Add missing columns
        for column in ORDERS_FINAL_COLUMNS:
            if column not in df.columns:
                df[column] = pd.NA
    
   
    return zepto_df, blinkit_df, swiggy_df

def standardize_data_types(zepto_df, blinkit_df, swiggy_df):
    
    string_columns = [
    "platform",
    "order_id",
    "customer_id",
    "product_id",
    "store_id",
    "delivery_partner_id",
    "order_status",
    "payment_method_id",
    "time_of_day"  ]
    
    float_columns = [ "order_value","discount_applied" ]
    
    int_columns = [ "quantity", "delivery_time_minutes" ]

    datetime_columns = [
    "order_datetime",
    "promised_delivery_datetime",
    "actual_delivery_datetime" ]
    
    dataframes = [zepto_df, blinkit_df, swiggy_df]

    for platform_df in dataframes:
        
        # Convert  into string columns
        for column in string_columns:
            if column in platform_df.columns:
                platform_df[column] = platform_df[column].astype(str)
                
        # Convert  into float columns
        for column in float_columns:
            if column in platform_df.columns:
                platform_df[column] = pd.to_numeric(platform_df[column], errors='coerce')
                
        # Convert  into integer columns
        for column in int_columns:
            if column in platform_df.columns:
                platform_df[column] = pd.to_numeric(platform_df[column], errors='coerce').astype('Int64')  # Use 'Int64' for nullable integer type

        # Convert into datetime columns
        for column in datetime_columns:
            if column in platform_df.columns:
                platform_df[column] = pd.to_datetime( platform_df[column],  format="%Y-%m-%d %H:%M:%S", errors="coerce" )
                
    return zepto_df, blinkit_df, swiggy_df

def reorder_columns(zepto_df, blinkit_df, swiggy_df):

    zepto_df = zepto_df[ORDERS_FINAL_COLUMNS]
    blinkit_df = blinkit_df[ORDERS_FINAL_COLUMNS]
    swiggy_df = swiggy_df[ORDERS_FINAL_COLUMNS]

    return zepto_df, blinkit_df, swiggy_df

def build_orders_dataset(zepto_df, blinkit_df, swiggy_df):

    #Append all Orders DataFrames into a single DataFrame.
    
    final_orders_df = pd.concat([zepto_df, blinkit_df, swiggy_df], ignore_index=True)
    
    return final_orders_df 

def create_derived_features(final_orders_df ):
    
    # Zepto has no reliable order time
    final_orders_df.loc[ final_orders_df["platform"] == "Zepto", "time_of_day" ] = pd.NA
    
    valid_platform_mask = final_orders_df["platform"] != "Zepto"
    
    # Extract hour from order_datetime
    hours = final_orders_df["order_datetime"].dt.hour
    
    # Morning (06:00 - 11:59)
    morning_mask = (hours >= 6) & (hours < 12)
    final_orders_df.loc[ valid_platform_mask & morning_mask, "time_of_day" ] = "Morning"
    
    # Afternoon (12:00 - 15:59)
    afternoon_mask = (hours >= 12) & (hours < 16)
    final_orders_df.loc[ valid_platform_mask & afternoon_mask, "time_of_day" ] = "Afternoon"

    # Evening (16:00 - 18:59)
    evening_mask = (hours >= 16) & (hours < 19)
    final_orders_df.loc[ valid_platform_mask & evening_mask, "time_of_day" ] = "Evening"

    # Night (19:00 - 23:59)
    night_mask = (hours >= 19) & (hours <= 23)
    final_orders_df.loc[ valid_platform_mask & night_mask, "time_of_day" ] = "Night"

    # Late Night (00:00 - 05:59)
    late_night_mask = (hours >= 0) & (hours < 6)
    final_orders_df.loc[ valid_platform_mask & late_night_mask, "time_of_day" ] = "Late Night"
        
    return final_orders_df
            

def validate_final_schema(final_orders_df):
    # Validate that the final DataFrame has the expected columns
    if list(final_orders_df.columns) != ORDERS_FINAL_COLUMNS:
        raise ValueError(
            f"Expected columns: {ORDERS_FINAL_COLUMNS}\n"
            f"Actual columns: {list(final_orders_df.columns)}" )


def save_orders(final_orders_df):
    """
    Save the cleaned orders dataset.
    """
    output_file = PROCESSED_DATA_PATH / ORDERS_FILE

    final_orders_df.to_csv( output_file, index=False )

    print(f"Orders dataset saved successfully at:\n{output_file}")

def main():
    
    zepto_df, blinkit_df, swiggy_df = load_orders()
    
    validate_orders(zepto_df, blinkit_df, swiggy_df)
    
    validate_source_schema(zepto_df, blinkit_df, swiggy_df)
    
    zepto_df, blinkit_df, swiggy_df = standardize_columns( zepto_df, blinkit_df, swiggy_df )
    
    zepto_df, blinkit_df, swiggy_df = prepare_final_schema(zepto_df, blinkit_df, swiggy_df)
    
    zepto_df, blinkit_df, swiggy_df = standardize_data_types(zepto_df, blinkit_df, swiggy_df)
    
    zepto_df, blinkit_df, swiggy_df = reorder_columns(zepto_df, blinkit_df, swiggy_df)
    
    final_orders_df = build_orders_dataset(zepto_df, blinkit_df, swiggy_df)
    
    final_orders_df = create_derived_features(final_orders_df)
    
    validate_final_schema(final_orders_df)
    
    save_orders(final_orders_df)
    
if __name__ == "__main__":
    main()
