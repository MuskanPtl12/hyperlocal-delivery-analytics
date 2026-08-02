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
    
    
    for platform ,platform_df in datasets.items():
        if platform_df.empty:
            raise ValueError(f"{platform} deliveries DataFrame is empty.")
        
# def add_details(blinkit_df, blinkit_order_df):
    
#     # add order_date by merge blinkit_delivery_performance and blinkit_orders table
#     blinkit_df = blinkit_df.merge( blinkit_order_df, on="order_id", how="left" )
   
#     return blinkit_df
        

        
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
        "OrderStatus": "delivery_status"
    })

    return zepto_df, blinkit_df, swiggy_df

def update_deliverytime_minutes(blinkit_df):
    
    datetime_columns = [
    "order_date",
    "actual_delivery_datetime" ]

    blinkit_df[datetime_columns] = ( blinkit_df[datetime_columns] .apply(pd.to_datetime, errors="coerce"))
    
    blinkit_df["delivery_time_minutes"] = (blinkit_df["actual_delivery_datetime"] - blinkit_df["order_date"]).dt.total_seconds().div(60).round().astype("Int64")
    
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

def standardize_values(zepto_df , blinkit_df, swiggy_df):
    # Standardize values for Zepto
    zepto_df["delivery_status"] = zepto_df["delivery_status"].replace({
        "Delivered": "Delivered",
        "Not Delivered": "Not Delivered"
    })
    
    # Standardize values for Blinkit
    blinkit_df["delivery_status"] = blinkit_df["delivery_status"].replace({
        "Delivered": "Delivered",
        "Not Delivered": "Not Delivered"
    })
    
    # Standardize values for Swiggy
    swiggy_df["delivery_status"] = swiggy_df["delivery_status"].replace({
        "Delivered": "Delivered",
        "Not Delivered": "Not Delivered"
    })

    return zepto_df, blinkit_df, swiggy_df
    
def validate(zepto_df, blinkit_df, swiggy_df):
    datasets = {
        "Zepto": zepto_df,
        "Blinkit": blinkit_df,
        "Swiggy": swiggy_df,
        }
    for platform, platform_df in datasets.items():
        print(sorted(platform_df["delivery_status"].unique()))
        print(8*"___________")
        
        
def main():
    zepto_df, blinkit_df,blinkit_order_df, swiggy_df = load_deliveries()
    
    validate_deliveries(zepto_df, blinkit_df,blinkit_order_df, swiggy_df)
    
    # blinkit_df,blinkit_order_df =add_details(blinkit_df, blinkit_order_df)
    
    validate_source_schema(zepto_df, blinkit_df,blinkit_order_df, swiggy_df)
    
    blinkit_df  =add_details(blinkit_df, blinkit_order_df)
    
    zepto_df, blinkit_df, swiggy_df = standardize_column_names(zepto_df, blinkit_df, swiggy_df)
    
    blinkit_df = update_deliverytime_minutes(blinkit_df)
    
    zepto_df, blinkit_df, swiggy_df= prepare_final_schema(zepto_df, blinkit_df, swiggy_df)
    
    # zepto_df, blinkit_df, swiggy_df = standardize_values(zepto_df , blinkit_df, swiggy_df)
    
    validate(zepto_df, blinkit_df, swiggy_df)

if __name__ == "__main__":
    main()
        
    