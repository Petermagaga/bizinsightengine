import pandas as pd
import re


def normalize_header(header):
    """
    Normalize headers for AI readability.
    """

    if pd.isna(header):
        return None

    header = str(header).strip().lower()

    header = re.sub(r"\s+", " ", header)
    header = re.sub(r"[^\w\s]", "", header)

    header = header.replace(" ", "_")

    return header


def detect_header_row(df):
    """
    Detect the best header row dynamically.

    Strategy:
    Choose the row with the most non-empty text values.
    """

    best_row = 0
    best_score = 0

    for idx in range(min(10, len(df))):

        row = df.iloc[idx]

        score = 0

        for value in row:

            if pd.notna(value):

                value = str(value).strip()

                # Text-heavy rows are likely headers
                if len(value) > 1:
                    score += 1

        if score > best_score:
            best_score = score
            best_row = idx

    return best_row

def parse_excel(file):
    """
    Intelligent parser for messy business Excel files.
    Supports multi-row headers.
    """

    # Read without headers
    raw_df = pd.read_excel(file, header=None)

    # Remove fully blank rows
    raw_df = raw_df.dropna(how="all")

    # Use first 2 rows as business headers
    header_row_1 = raw_df.iloc[0]
    header_row_2 = raw_df.iloc[1]

    columns = []

    current_parent = None

    for i in range(len(raw_df.columns)):

        parent = header_row_1.iloc[i]
        child = header_row_2.iloc[i]

        # Forward-fill parent category
        if pd.notna(parent):
            current_parent = normalize_header(parent)

        child_clean = normalize_header(child)

        # Combine parent + child
        if current_parent and child_clean:
            column_name = f"{current_parent}_{child_clean}"

        elif child_clean:
            column_name = child_clean

        elif current_parent:
            column_name = f"{current_parent}_{i}"

        else:
            column_name = f"column_{i}"

        columns.append(column_name)

    # Actual data starts after header rows
    df = raw_df.iloc[2:].copy()

    df.columns = columns

    # Remove fully blank rows
    df = df.dropna(how="all")

    # Remove fully blank columns
    df = df.dropna(axis=1, how="all")

    records = df.to_dict(orient="records")

    return records