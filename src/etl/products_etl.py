import pandas as pd
from src.config import RAW_DATA_PATH 
from src.utils.file_loader import load_csv
from src.schema import PRODUCTS_FINAL_COLUMNS
from src.product_mapping import (SUBCATEGORY_KEYWORDS, CATEGORY_MAPPING,PRODUCT_OVERRIDE )

def load_products():
    zepto_product_path=RAW_DATA_PATH/"Zepto"/"zepto_product.csv"
    blinkit_products_path=RAW_DATA_PATH/"Blinkit"/"blinkit_products.csv"
    swiggy_products_path= RAW_DATA_PATH/"Swiggy instamart"/"swiggy_products.csv"
    swiggy_category_path = RAW_DATA_PATH/"Swiggy instamart"/"swiggy_categories.csv"
   
    zepto_df = load_csv(zepto_product_path)
    blinkit_df = load_csv(blinkit_products_path)
    swiggy_df = load_csv(swiggy_products_path)
    swiggy_category_df =load_csv(swiggy_category_path)
    
    return zepto_df, blinkit_df, swiggy_df ,swiggy_category_df

def validate_products(zepto_df,blinkit_df,swiggy_df,swiggy_category_df):
    datasets = {
    "Zepto": zepto_df,
    "Blinkit": blinkit_df,
    "Swiggy": swiggy_df, 
    "swiggy": swiggy_category_df ,}
    
    for platform ,platform_df in datasets.items():
        if platform_df.empty:
            raise ValueError(f"{platform} products DataFrame is empty.")

def add_category_details(swiggy_df, swiggy_category_df):
    
    # add categoryname and Sub_Category by merge swiggy_product and swiggy_categories table
    swiggy_df = swiggy_df.merge( swiggy_category_df, on="CategoryID", how="left" )
    
    # #remove categoryID form updated swiggy_df
    # swiggy_df = swiggy_df.drop(columns=["CategoryID"]) 
   
    return swiggy_df

def validate_source_schema(zepto_df, blinkit_df, swiggy_df):
    
    zepto_required_columns =[
        "product_id",
        "product_name",
        "category",
        "sub_category",
        "price"     
    ]
    
    blinkit_required_columns =[
        "product_id",
        "product_name",
        "category",
        "brand",
        "price",
        "mrp",
        "margin_percentage",
        'shelf_life_days',
        'min_stock_level',
        'max_stock_level'
    ]
    
    swiggy_required_columns=[
        'ProductID',
        'ProductName',
        'CategoryID',
        'UnitPrice',
        'StockQuantity',
        'SupplierID',
        "CategoryName" ,
        "Subcategory"
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
        
def remove_unnecessary_columns(zepto_df,blinkit_df,swiggy_df):
    
    # Remove columns from Blinkit
    blinkit_df=blinkit_df.drop(columns=["margin_percentage", 'min_stock_level', 'max_stock_level'])
    
    # Remove columns from swiggy
    swiggy_df=swiggy_df.drop(columns=[ 'CategoryID', 'StockQuantity', 'SupplierID'])
    
    return zepto_df,blinkit_df,swiggy_df
    
       
def standardize_columns(zepto_df, blinkit_df, swiggy_df):
    
    # zepto and blinkit do not have any rename column
    swiggy_df.rename(
        columns = {
            'ProductID':"product_id",
            'ProductName':"product_name",
            'UnitPrice' : "unit_price",
            'CategoryName' : 'category',
            "Subcategory" : 'sub_category',}
        ,inplace=True)
    
    return zepto_df, blinkit_df, swiggy_df

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
        for column in PRODUCTS_FINAL_COLUMNS:
            if column not in platform_df.columns:
                platform_df[column] = pd.NA
   
    return zepto_df, blinkit_df, swiggy_df

def get_sub_category(product_name):

    product_name = str(product_name).lower()
    words = product_name.split()

    for sub_category, keywords in SUBCATEGORY_KEYWORDS.items():

        keywords = sorted(keywords, key=len, reverse=True)

        for keyword in keywords:

            if " " in keyword:

                if keyword in product_name:
                    return sub_category

            else:

                if keyword in words:
                    return sub_category

    return "Uncategorized"

def get_category(sub_category):

    return CATEGORY_MAPPING.get( sub_category, "Uncategorized" )

def apply_product_override(df):
    """
    Override incorrect product classifications
    using PRODUCT_OVERRIDE.
    """
    for product_name, mapping in PRODUCT_OVERRIDE.items():

        mask = df["product_name"] == product_name

        df.loc[mask, "sub_category"] = mapping["sub_category"]
        df.loc[mask, "category"] = mapping["category"]

    return df

def standardize_values(zepto_df, blinkit_df, swiggy_df):
    """
    Standardize category and sub_category
    using product_name.
    """
    dataframes = [zepto_df, blinkit_df, swiggy_df]

    for df in dataframes:
        
        # Step 1: Classify sub_category
        df["sub_category"] = (
            df["product_name"]
            .apply(get_sub_category)  )

        # Step 2: Map category
        df["category"] = (
            df["sub_category"]
            .apply(get_category) )

        # Step 3: Apply manual overrides
        apply_product_override(df)

    return zepto_df, blinkit_df, swiggy_df

# def validate(zepto_df, blinkit_df, swiggy_df):
    
def validate_sub_category( zepto_df, blinkit_df, swiggy_df):
    pass
    


def main():
    
    zepto_df, blinkit_df, swiggy_df ,swiggy_category_df = load_products()
    
    validate_products(zepto_df,blinkit_df,swiggy_df,swiggy_category_df)
    
    swiggy_df =  add_category_details(swiggy_df, swiggy_category_df)
    
    validate_source_schema(zepto_df, blinkit_df, swiggy_df)
    
    zepto_df, blinkit_df, swiggy_df = remove_unnecessary_columns(zepto_df,blinkit_df,swiggy_df)
    
    zepto_df, blinkit_df, swiggy_df = standardize_columns( zepto_df, blinkit_df, swiggy_df )
    
    zepto_df, blinkit_df, swiggy_df = prepare_final_schema(zepto_df, blinkit_df, swiggy_df)
    
    zepto_df, blinkit_df, swiggy_df = standardize_values(zepto_df , blinkit_df, swiggy_df)
    
    validate_sub_category(zepto_df,blinkit_df,swiggy_df )
    
    
        

if __name__ == "__main__":
    main()
