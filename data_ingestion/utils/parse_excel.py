import pandas as pd
import re


def normalize_header(header):

    if pd.isna(header):
        return None

    header = str(header).strip().lower()

    header = re.sub(r"[^\w\s]", "", header)
    header = re.sub(r"\s+", "_", header)

    return header


def is_mostly_empty(row):

    empty_count = row.isna().sum()

    return empty_count >= (len(row) * 0.7)


def detect_header_row(df):

    """
    Find the row most likely to contain headers.
    """

    best_row = 0
    best_score = 0

    for idx in range(min(10, len(df))):

        row = df.iloc[idx]

        score = 0

        for value in row:

            if pd.notna(value):

                text = str(value).strip()

                if len(text) > 1:
                    score += 1

                # penalize date-like rows
                if "date:" in text.lower():
                    score -= 2

        if score > best_score:
            best_score = score
            best_row = idx

    return best_row


def parse_excel(file):

    raw_df = pd.read_excel(file, header=None)

    raw_df = raw_df.dropna(how="all")

    if raw_df.empty:
        return []

    # -----------------------------
    # Detect header row dynamically
    # -----------------------------
    header_row_index = detect_header_row(raw_df)

    header_row = raw_df.iloc[header_row_index]

    columns = []

    used_names = set()

    for idx, value in enumerate(header_row):

        column_name = normalize_header(value)

        if not column_name:
            column_name = f"column_{idx}"

        # avoid duplicate names
        if column_name in used_names:
            column_name = f"{column_name}_{idx}"

        used_names.add(column_name)

        columns.append(column_name)

    # -----------------------------
    # Actual data starts after header
    # -----------------------------
    data_df = raw_df.iloc[header_row_index + 1:].copy()

    data_df.columns = columns

    # remove empty rows
    data_df = data_df.dropna(how="all")

    records = []

    current_date = None

    for _, row in data_df.iterrows():

        row_dict = {}

        row_values = row.to_dict()

        # detect date rows
        first_value = str(
            list(row_values.values())[0]
        ).strip()

        if "date:" in first_value.lower():

            current_date = (
                first_value
                .replace("DATE:", "")
                .strip()
            )

            continue

        for key, value in row_values.items():

            # skip nan
            if pd.isna(value):
                value = None

            row_dict[key] = value

        row_dict["production_date"] = current_date

        records.append(row_dict)

    return records