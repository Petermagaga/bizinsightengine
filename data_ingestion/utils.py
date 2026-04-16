import pandas as pd

def parse_excel(file):
    try:
        df =pd.read_excel(file)
        data =df.to_dict(orient="records")
        return data
    except Exception as e:
        raise ValueError(f"Error processing file: {str(e)}")