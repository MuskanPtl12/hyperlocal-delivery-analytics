import pandas as pd
from src.config import RAW_DATA_PATH 
from src.config import PROCESSED_DATA_PATH, DELIVERIES_FILE 
from src.utils.file_loader import load_csv
from src.schema import DELIVERY_FINAL_COLUMNS

def load_deliveries():
    zepto_deliveries_path=RAW_DATA_PATH/"Zepto"/"zepto_delivery.csv"
    blinkit_deliveries_path=RAW_DATA_PATH/"Blinkit"/"blinkit_delivery_performance.csv"
    blinkit_order_path=RAW_DATA_PATH/"Blinkit"/"blinkit_orders.csv"
    swiggy_deliveries_path= RAW_DATA_PATH/"swiggy instamart"/"swiggy_order.csv"
   
    zepto_df = load_csv(zepto_deliveries_path)
    blinkit_df = load_csv(blinkit_deliveries_path)
    blinkit_order_df = load_csv(blinkit_order_path, usecols=["order_id", "order_date"])
    swiggy_df = load_csv(swiggy_deliveries_path, usecols=["OrderID", "DeliveryPartnerID","DeliveryDate","DeliveryTimeMinutes","OrderStatus"])
    
    return zepto_df, blinkit_df ,blinkit_order_df, swiggy_df

def validate_deliveries(zepto_df,blinkit_df,blinkit_order_df,swiggy_df):
    datasets = {
    "Zepto": zepto_df,
    "Blinkit": blinkit_df,
    "Blinkit Orders": blinkit_order_df,
    "Swiggy": swiggy_df,}
    
    # Validate that all DataFrames are not empty
    for platform ,platform_df in datasets.items():
        if platform_df.empty:
            raise ValueError(f"{platform} deliveries DataFrame is empty.")
        
def validate_source_schema(zepto_df, blinkit_df,blinkit_order_df, swiggy_df):
    
    zepto_required_columns =[
        "delivery_id",
        "order_id",
        "delivery_time_mins",
        "delivery_status",
        "distance_km"
    ]
    
    blinkit_required_columns =[
        "order_id",
        "delivery_partner_id",
        "promised_time",
        "actual_time",
        "delivery_time_minutes",
        "distance_km",
        "delivery_status",
        "reasons_if_delayed"
    ]
    
    blinkit_order_required_columns =[
        "order_id",
        "order_date"
    ]
    
    swiggy_required_columns =[
        "OrderID", 
        "DeliveryPartnerID", 
        "DeliveryDate", 
        "DeliveryTimeMinutes", 
        "OrderStatus"
    ]
    
    
    datasets = {
    "Zepto": (zepto_df, zepto_required_columns),
    "Blinkit": (blinkit_df, blinkit_required_columns),
    "Blinkit Orders": (blinkit_order_df, blinkit_order_required_columns),
    "Swiggy": (swiggy_df, swiggy_required_columns),}
    
    # Validate that all required columns are present in each DataFrame
    
    for column in zepto_required_columns:
        if column not in zepto_df.columns:
            raise ValueError(f"Zepto DataFrame is missing required column: {column}") 

    for column in blinkit_required_columns:
        if column not in blinkit_df.columns:
            raise ValueError(f"Blinkit DataFrame is missing required column: {column}")

    for column in blinkit_order_required_columns:
        if column not in blinkit_order_df.columns:
            raise ValueError(f"Blinkit Orders DataFrame is missing required column: {column}")

    for column in swiggy_required_columns:
        if column not in swiggy_df.columns:
            raise ValueError(f"Swiggy DataFrame is missing required column: {column}")
    
def add_details(blinkit_df, blinkit_order_df):
    
    # add order_date by merge blinkit_delivery_performance and blinkit_orders table
    blinkit_df = blinkit_df.merge( blinkit_order_df, on="order_id", how="left" )
   
    return blinkit_df   

    
def standardize_column_names(zepto_df, blinkit_df, swiggy_df):
    # Standardize column names for Zepto
    zepto_df = zepto_df.rename(columns={
        
        "delivery_time_mins": "delivery_time_minutes"
    })
    
    # Standardize column names for Blinkit
    blinkit_df = blinkit_df.rename(columns={
        "promised_time": "promised_delivery_datetime",
        "actual_time": "actual_delivery_datetime",
        "reasons_if_delayed": "delay_reason"
    })
    
    # Standardize column names for Swiggy
    swiggy_df = swiggy_df.rename(columns={
        "OrderID": "order_id", 
        "DeliveryPartnerID": "delivery_partner_id",  
        "DeliveryDate": "actual_delivery_datetime", 
        "DeliveryTimeMinutes": "delivery_time_minutes", 
        "OrderStatus": "order_status"
    })

    return zepto_df, blinkit_df, swiggy_df

def update_deliverytime_minutes(blinkit_df):
    
    datetime_columns = [
    "order_date",
    "actual_delivery_datetime" ]
    
    # Convert the specified columns to datetime format
    blinkit_df[datetime_columns] = ( blinkit_df[datetime_columns] .apply(pd.to_datetime, errors="coerce"))
    
    # Calculate delivery_time_minutes as the difference between actual_delivery_datetime and order_date in minutes
    blinkit_df["delivery_time_minutes"] = (blinkit_df["actual_delivery_datetime"] - blinkit_df["order_date"]).dt.total_seconds().div(60).round().astype("Int64")
    
    # Drop the order_date column as it is no longer needed
    blinkit_df = blinkit_df.drop(columns=["order_date"])
    
    return blinkit_df

def prepare_final_schema(zepto_df, blinkit_df, swiggy_df):
    """
    Prepare all Orders DataFrames according to the final schema.
    """
    dataframes = {
        "Zepto": zepto_df,
        "Blinkit": blinkit_df,
        "Swiggy": swiggy_df }

    for platform, platform_df in dataframes.items():
        # Add platform column
        platform_df["platform"] = platform

        # Add missing columns
        for column in DELIVERY_FINAL_COLUMNS:
            if column not in platform_df.columns:
                platform_df[column] = pd.NA
   
    return zepto_df, blinkit_df, swiggy_df

def standardize_values(zepto_df , blinkit_df):
    
    DELIVERY_STATUS_MAPPING = {
    # Blinkit
    "On Time": "On Time",
    "Slightly Delayed": "Slightly Delayed",
    "Significantly Delayed": "Late",

    # Zepto
    "Delivered On Time": "On Time",
    "Delivered Late": "Late"  }
    
    # Standardize delivery_status values for Zepto and Blinkit
    blinkit_df["delivery_status"] = blinkit_df["delivery_status"].map(DELIVERY_STATUS_MAPPING).fillna(blinkit_df["delivery_status"])
    
    # Standardize delivery_status values for Zepto 
    zepto_df["delivery_status"] = zepto_df["delivery_status"].map(DELIVERY_STATUS_MAPPING).fillna(zepto_df["delivery_status"])
    
    return zepto_df, blinkit_df

def reorder_columns(zepto_df, blinkit_df, swiggy_df):

    zepto_df = zepto_df[DELIVERY_FINAL_COLUMNS]
    blinkit_df = blinkit_df[DELIVERY_FINAL_COLUMNS]
    swiggy_df = swiggy_df[DELIVERY_FINAL_COLUMNS]

    return zepto_df, blinkit_df, swiggy_df

def standardize_datetype(zepto_df, blinkit_df, swiggy_df):
    columns= {
        "string_columns" :["delivery_id","delivery_partner_id","order_id","delivery_status","order_status","delay_reason"],
        
        "int_columns" : ["delivery_time_minutes"],
        
        "float_columns" : ["distance_km"] ,
        
        "datetime_columns" : ["actual_delivery_datetime","promised_delivery_datetime"]  }
    
    dataframes = [zepto_df, blinkit_df, swiggy_df]
    
    # Standardize data types for each DataFrame based on the specified columns
    for platform_df in dataframes:
    
        for dtypee , column in columns.items():
            
            if dtypee=="string_columns":
                platform_df[column] = platform_df[column].astype(str)
            
            elif dtypee=="int_columns":
                platform_df[column] = platform_df[column].apply( pd.to_numeric, errors="coerce" ).astype("Int64")
                            
            elif dtypee=="float_columns":
                platform_df[column] = platform_df[column].apply( pd.to_numeric, errors="coerce" ).astype("Float64")
                
            elif dtypee=="datetime_columns":
                platform_df[column] = platform_df[column].apply(pd.to_datetime, errors="coerce")
            
    return zepto_df,blinkit_df,swiggy_df

def build_delivery_dataset(zepto_df, blinkit_df, swiggy_df):

    #Append all Orders DataFrames into a single DataFrame.
    
    final_delivery_df = pd.concat([zepto_df, blinkit_df, swiggy_df], ignore_index=True)
    
    return final_delivery_df

def validate_final_schema(final_delivery_df,zepto_df, blinkit_df, swiggy_df):
    
    # Validate that the final DataFrame has the expected columns
    if list(final_delivery_df.columns) != DELIVERY_FINAL_COLUMNS:
        raise ValueError(
            f"Expected columns: {DELIVERY_FINAL_COLUMNS}\n"
            f"Actual columns: {list(final_delivery_df.columns)}" )
        
    # validate missing rows   
    expected = len(zepto_df) + len(blinkit_df) + len(swiggy_df)
    actual = len(final_delivery_df)
    if expected != actual:
        raise ValueError(
            f"Row count mismatch. Expected {expected} rows but found {actual}." )
    
def save_orders(final_delivery_df):
    """
    Save the cleaned delivery dataset.
    """
    output_file = PROCESSED_DATA_PATH / DELIVERIES_FILE

    final_delivery_df.to_csv( output_file, index=False )

    print(f"Delivery dataset saved successfully at:\n{output_file}")
        
        
def main():
    
    zepto_df, blinkit_df,blinkit_order_df, swiggy_df = load_deliveries()
    
    validate_deliveries(zepto_df, blinkit_df,blinkit_order_df, swiggy_df)
    
    validate_source_schema(zepto_df, blinkit_df,blinkit_order_df, swiggy_df)
    
    blinkit_df  = add_details(blinkit_df, blinkit_order_df)
    
    zepto_df, blinkit_df, swiggy_df = standardize_column_names(zepto_df, blinkit_df, swiggy_df)
    
    blinkit_df = update_deliverytime_minutes(blinkit_df)
    
    zepto_df, blinkit_df, swiggy_df = prepare_final_schema(zepto_df, blinkit_df, swiggy_df)
    
    zepto_df, blinkit_df = standardize_values(zepto_df , blinkit_df)
    
    zepto_df, blinkit_df, swiggy_df = reorder_columns(zepto_df, blinkit_df, swiggy_df)
    
    zepto_df, blinkit_df, swiggy_df = standardize_datetype(zepto_df, blinkit_df, swiggy_df)
    
    final_delivery_df = build_delivery_dataset(zepto_df, blinkit_df, swiggy_df)
    
    validate_final_schema(final_delivery_df, zepto_df, blinkit_df, swiggy_df)
    
    save_orders(final_delivery_df)

if __name__ == "__main__":
    main()
        
    