
import math
from datetime import datetime, date
from decimal import Decimal


def clean_row(row):
    cleaned = {}

    for k, v in row.items():

        if isinstance(v, (datetime, date)):
            cleaned[k] = v.isoformat()

        elif isinstance(v, Decimal):
            cleaned[k] = float(v)

        elif isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            cleaned[k] = None

        elif isinstance(v, (int, float, str, bool)) or v is None:
            cleaned[k] = v

        else:
            cleaned[k] = str(v)

    return cleaned