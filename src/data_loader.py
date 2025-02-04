import pandas as pd
from pathlib import Path


def load_data_file(file_path):
    """Load a data file based on its extension (.csv or .xlsx).
    
    Args:
        file_path (str): Path to the data file to load.
        
    Returns:
        pd.DataFrame: DataFrame containing the data with columns 'Object' and 'Waarde'.
    """
    file = Path(file_path)
    if not file.exists():
        raise FileNotFoundError(f"File not found at: {file_path}")

    ext = file.suffix.lower()
    if ext == '.csv':
        df = pd.read_csv(file)
    elif ext in ['.xlsx', '.xls']:
        df = pd.read_excel(file)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

    # Assume the file's structure: first column "Object" and third column "Waarde"
    df = pd.DataFrame({
        'Object': df.iloc[:, 0].astype(str),
        'Waarde': df.iloc[:, 2]
    })
    return df
