import json
import numpy as np
import pandas as pd

def make_json_safe(row: dict):
    clean = {}

    for key, value in row.items():
        if pd.isna(value):
            clean[key] = None

        elif isinstance(value, (np.integer,)):
            clean[key] = int(value)

        elif isinstance(value, (np.floating,)):
            clean[key] = float(value)

        elif isinstance(value, (pd.Timestamp,)):
            clean[key] = value.isoformat()

        elif isinstance(value, (str, int, float, bool)) or value is None:
            clean[key] = value

        else:
            clean[key] = str(value)

    # Validate JSON before returning
    json.dumps(clean)

    return clean