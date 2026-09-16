import pandas as pd
from src.config import RAW_DATA_PATH
from src.config import PROCESSED_DATA_PATH, RATING_FILE
from src.utils.file_loader import load_csv
from src.schema import CUSTOMER_FINAL_COLUMNS, RATING_FINAL_COLUMNS

# load rating data from raw data folder
def load_rating():
    # swiggy does not have Rating data, so we will not load it here
    zepto_rating_path = RAW_DATA_PATH /"Zepto"/"zepto_rating.csv"
    blinkit_rating_path = RAW_DATA_PATH /"Blinkit"/"blinkit_customer_feedback.csv"
    
    blinkit_df = load_csv(blinkit_rating_path)
    zepto_df = load_csv(zepto_rating_path)

    return zepto_df, blinkit_df

def validate_ratings(zepto_df, blinkit_df):
    datasets = {
    "Zepto": zepto_df,
    "Blinkit": blinkit_df
    }
    
    # Validate that none of the DataFrames are empty
    for name, df in datasets.items():
        if df.empty:
            raise ValueError(f"{name} rating DataFrame is empty.")

def validate_source_schema(zepto_df, blinkit_df):

    zepto_required_columns = ['rating_id', 'order_id', 'rating','review']

    blinkit_required_columns = [
    'feedback_id',
    'order_id',
    'rating', 
    'feedback_text'] 
       
    
    # Validate that all required columns are present in each DataFrame
    for column in zepto_required_columns:
        if column not in zepto_df.columns:
            raise ValueError(f"Zepto DataFrame is missing required column: {column}") 
    for column in blinkit_required_columns:
        if column not in blinkit_df.columns:
            raise ValueError(f"Blinkit DataFrame is missing required column: {column}")
        
def standardize_columns(zepto_df, blinkit_df):
    
    # Standardize column names across all DataFrames
    zepto_df = zepto_df.rename(columns={
        'rating_id': 'rating_id',
        'order_id': 'order_id',
        'rating': 'rating',
        'review': 'feedback'
        })
    
    blinkit_df = blinkit_df.rename(columns={
        'feedback_id': 'rating_id',
        'order_id': 'order_id',
        'rating': 'rating',
        'feedback_text': 'feedback'
        })  

    return zepto_df, blinkit_df


def prepare_final_schema(zepto_df, blinkit_df):
    """
    Prepare all Rating DataFrames according to the final schema.
    """
    dataframes = {
        "Zepto": zepto_df,
        "Blinkit": blinkit_df}
    
    for platform, df in dataframes.items():
        # Add platform column
        df["platform"] = platform

    # Add missing columns
    for column in RATING_FINAL_COLUMNS:
        if column not in df.columns:
            df[column] = pd.NA
            

    return zepto_df, blinkit_df

def reorder_columns(zepto_df, blinkit_df):

    zepto_df = zepto_df[RATING_FINAL_COLUMNS]
    blinkit_df = blinkit_df[RATING_FINAL_COLUMNS]

    return zepto_df, blinkit_df

def build_ratings_dataset(zepto_df, blinkit_df):

    #Append all Ratings DataFrames into a single DataFrame.
    
    final_ratings_df = pd.concat([zepto_df, blinkit_df], ignore_index=True)
   
    return final_ratings_df

def value_standardize(final_ratings_df):
    # Standardize values in the final ratings DataFrame
    column= [
    "platform", 
    "feedback" ]
    
    for col in column:
        if col in final_ratings_df.columns:
            final_ratings_df[col] = final_ratings_df[col].str.strip()
              
    return final_ratings_df

def standardize_data_types(final_ratings_df):
    string_columns = ["platform", "rating_id", "order_id", "feedback"]
    
    integer_columns = ["rating"]
    
     # Convert into string columns
    for column in string_columns:
        if column in final_ratings_df.columns:
            final_ratings_df[column] = final_ratings_df[column].astype("string")
    
    # Convert into integer columns
    for column in integer_columns:
        if column in final_ratings_df.columns:
            final_ratings_df[column] = (
                pd.to_numeric(
                    final_ratings_df[column],
                    errors="coerce"
                ).astype("Int64")  )
                
    return final_ratings_df    


def validate_final_schema(final_ratings_df,zepto_df, blinkit_df):
    # Validate that the final DataFrame has the expected columns
    if list(final_ratings_df.columns) != RATING_FINAL_COLUMNS:
        raise ValueError(
            f"Expected columns: {RATING_FINAL_COLUMNS}\n"
            f"Actual columns: {list(final_ratings_df.columns)}" )
    
    # validate missing rows   
    expected = len(zepto_df) + len(blinkit_df)
    actual = len(final_ratings_df)
    if expected != actual:
        raise ValueError(
            f"Row count mismatch. Expected {expected} rows but found {actual}." )
   
   
def save_ratings(final_ratings_df):
    """
    Save the cleaned ratings dataset.
    """
    output_file = PROCESSED_DATA_PATH / RATING_FILE

    final_ratings_df.to_csv( output_file, index=False )

    print(f"Ratings dataset saved successfully at:\n{output_file}")

def main():
    
    zepto_df, blinkit_df = load_rating()
    
    validate_ratings(zepto_df, blinkit_df)
    
    validate_source_schema(zepto_df, blinkit_df)

    zepto_df, blinkit_df = standardize_columns(zepto_df, blinkit_df)
    
    zepto_df, blinkit_df = prepare_final_schema(zepto_df, blinkit_df)
    
    zepto_df, blinkit_df = reorder_columns(zepto_df, blinkit_df)
    
    final_ratings_df = build_ratings_dataset(zepto_df, blinkit_df)
    
    final_ratings_df = value_standardize(final_ratings_df)
    
    final_ratings_df = standardize_data_types(final_ratings_df)
    
    validate_final_schema(final_ratings_df, zepto_df, blinkit_df)
    
    save_ratings(final_ratings_df)

if __name__ == "__main__":
    main()
