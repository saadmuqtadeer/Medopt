# autocomplete_app/utils.py
import pandas as pd

def get_names_from_csv(file_path):
    # Load the CSV dataset using pandas
    df = pd.read_csv(file_path)

    # Extract the names from the name field
    names = df['name'].tolist()

    return names
