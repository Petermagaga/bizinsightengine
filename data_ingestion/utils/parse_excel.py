import pandas as pd
import re


def normalize_header(header):
    """
    Normalize headers into AI-friendly names.
    """

    if pd.isna(header):
        return None

    header = str(header).strip().lower()

    # Remove special characters
    header = re.sub(r"[^\w\s]", "", header)

    # Normalize spaces
    header = re.sub(r"\s+", "_", header)

    return header


def parse_excel(file):
    """
    Intelligent parser for messy business Excel files.

    Supports:
    - Multi-row headers
    - Merged cells
    - Empty columns
    - Business spreadsheet structures
    """

    # Read raw sheet with no assumed headers
    raw_df = pd.read_excel(file, header=None)

    # Remove fully empty rows
    raw_df = raw_df.dropna(how="all")

    # Safety check
    if len(raw_df) < 2:
        return []

    # First row = parent headers
    header_row_1 = raw_df.iloc[0]

    # Second row = child headers
    header_row_2 = raw_df.iloc[1]

    columns = []
    current_parent = None

    for i in range(len(raw_df.columns)):

        parent = header_row_1.iloc[i]
        child = header_row_2.iloc[i]

        # Forward-fill merged section headers
        if pd.notna(parent):
            current_parent = normalize_header(parent)

        child_clean = normalize_header(child)

        # Create semantic business column names
        if current_parent and child_clean:
            column_name = f"{current_parent}_{child_clean}"

        elif child_clean:
            column_name = child_clean

        elif current_parent:
            column_name = f"{current_parent}_{i}"

        else:
            column_name = f"column_{i}"

        columns.append(column_name)

    # Data starts after 2 header rows
    df = raw_df.iloc[2:].copy()

    # Assign semantic columns
    df.columns = columns

    # Remove empty rows
    df = df.dropna(how="all")

    # Remove empty columns
    df = df.dropna(axis=1, how="all")

    return df.to_dict(orient="records")