import pandas as pd

def load_csv(file_path, **kwargs):
    """
    Load a CSV file and return a pandas DataFrame.
    Parameters
    ----------
    file_path : str
        Path to the CSV file.
    Returns
    -------
    pandas.DataFrame
        Loaded DataFrame.
    """

    df = pd.read_csv(file_path, **kwargs)

    return df