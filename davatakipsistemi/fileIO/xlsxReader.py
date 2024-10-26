import pandas as pd

def read_excel_file(file_path):
    """
    Reads a given .xlsx file and returns its contents as a DataFrame.
    
    Parameters:
    file_path (str): The file path of the .xlsx file to read.
    
    Returns:
    pd.DataFrame or None: Returns the content as a DataFrame if the file is read successfully.
                          Returns None if an error occurs.
    
    """
    # Read the file
    try:
        data = pd.read_excel(file_path)
        return data
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None
