import pandas as pd
from datetime import datetime


def parse_amount(value):

    if pd.isna(value):
        return 0.0

    value = str(value)

    value = value.replace(" ", "")
    value = value.replace(",", ".")

    return float(value)


def parse_date(value):

    if pd.isna(value):
        return None

    return datetime.strptime(
        str(value),
        "%Y-%m-%d"
    ).date()


def import_csv(file_path):

    df = pd.read_csv(
        file_path,
        sep=";",
        encoding="utf-8"
    )

    transactions = []

    for _, row in df.iterrows():

        transactions.append({
            "date": parse_date(row["dateVal"]),
            "label": str(row["label"]),
            "suggested_label": str(row["suggestedLabel"]),    
            "category": str(row["category"]),
            "category_parent": str(row["categoryParent"]),        
            "amount": parse_amount(row["amount"]),       
            "comment": str(row["comment"]),      
            "account_num": str(row["accountNum"]),
            "account_label": str(row["accountLabel"])
        })

    return transactions