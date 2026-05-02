
import pandas as pd

def parse_excel(file):
    df = pd.read_excel(file)

    
    data = df.to_dict(orient="records")

    return data