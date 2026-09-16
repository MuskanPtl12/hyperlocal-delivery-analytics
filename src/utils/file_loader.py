
from pathlib import Path
import pandas as pd


def load_csv(file_path, **kwargs):
    """
    Load a CSV file and return a pandas DataFrame.
    Raises FileNotFoundError if the file does not exist.
    """
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"CSV file not found: {path}")
    
    df = pd.read_csv(path, **kwargs)
    return df