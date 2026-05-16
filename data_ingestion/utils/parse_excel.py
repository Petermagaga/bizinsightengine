import pandas as pd
import re


def normalize_header(header):
    """
    Normalize Excel headers into AI-friendly names.
    Example:
    'Opening Balance' -> 'opening_balance'
    """

    if pd.isna(header):
        return None

    header = str(header).strip().lower()

    # Replace spaces and symbols
    header = re.sub(r"[^\w\s]", "", header)
    header = re.sub(r"\s+", "_", header)

    return header


def parse_excel(file):
    """
    Parse Excel while preserving business structure.
    """

    # Read Excel
    df = pd.read_excel(file)

    # Remove fully blank rows
    df = df.dropna(how="all")

    # Remove fully blank columns
    df = df.dropna(axis=1, how="all")

    # Normalize headers
    normalized_columns = []

    for i, col in enumerate(df.columns):

        normalized = normalize_header(col)

        if not normalized:
            normalized = f"column_{i}"

        normalized_columns.append(normalized)

    df.columns = normalized_columns

    # Convert to records
    records = df.to_dict(orient="records")

    return records