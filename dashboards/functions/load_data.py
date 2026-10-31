import pandas as pd


def load_csv(file_path: str) -> pd.DataFrame:
    """ 
    Load a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: The loaded DataFrame.
    """
    df = pd.DataFrame()
    try:
        df = pd.read_csv(file_path)
    except:
        print(f"No se encontró el archivo: {file_path}")
    
    return df