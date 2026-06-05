from database.database import SessionLocal
from database.models import (
    Transaction,
    ImportedFile
)
from sqlalchemy import func
from datetime import date

import os

def get_all_transactions():

    session = SessionLocal()

    transactions = (
        session.query(Transaction)
        .order_by(Transaction.date.desc())
        .all()
    )

    result = []

    for t in transactions:

        result.append({
            "date": t.date,
            "label": t.label,
            "suggested_label": t.suggested_label,
            "category": t.category,
            "category_parent": t.category_parent,
            "amount": t.amount,
            "comment": t.comment,
            "account_num": t.account_num,
            "account_label": t.account_label
        })

    session.close()

    return result

def save_transactions(transactions):

    session = SessionLocal()

    imported = 0

    for t in transactions:

        transaction = Transaction(
            date=t["date"],
            label=t["label"],
            suggested_label=t["suggested_label"],
            category=t["category"],
            category_parent=t["category_parent"],
            amount=t["amount"],
            comment=t["comment"],
            account_num=t["account_num"],
            account_label=t["account_label"]
        )

        session.add(transaction)
        imported += 1

    session.commit()
    session.close()

    return imported


def is_file_already_imported(
    session,
    file_hash
):

    return (
        session.query(ImportedFile)
        .filter(
            ImportedFile.file_hash == file_hash
        )
        .first()
        is not None
    )


def register_imported_file(
    session,
    file_path,
    file_hash
):

    imported_file = ImportedFile(
        filename=os.path.basename(
            file_path
        ),
        file_hash=file_hash
    )

    session.add(imported_file)

    session.commit()

def get_dashboard_stats():

    session = SessionLocal()

    today = date.today()

    current_month = today.month
    current_year = today.year

    transactions = session.query(Transaction).all()

    total_transactions = len(transactions)

    revenues = (
        session.query(
            func.sum(Transaction.amount)
        )
        .filter(
            Transaction.amount > 0
        )
        .scalar()
        or 0
    )

    expenses = (
        session.query(
            func.sum(Transaction.amount)
        )
        .filter(
            Transaction.amount < 0
        )
        .scalar()
        or 0
    )

    monthly_revenues = (
        session.query(
            func.sum(Transaction.amount)
        )
        .filter(
            Transaction.amount > 0,
            func.strftime('%Y', Transaction.date) == str(current_year),
            func.strftime('%m', Transaction.date) == f"{current_month:02d}"
        )
        .scalar()
        or 0
    )

    monthly_expenses = (
        session.query(
            func.sum(Transaction.amount)
        )
        .filter(
            Transaction.amount < 0,
            func.strftime('%Y', Transaction.date) == str(current_year),
            func.strftime('%m', Transaction.date) == f"{current_month:02d}"
        )
        .scalar()
        or 0
    )

    session.close()

    return {
        "total_transactions": total_transactions,
        "revenues": revenues,
        "expenses": abs(expenses),
        "monthly_revenues": monthly_revenues,
        "monthly_expenses": abs(monthly_expenses),
        "balance": revenues + expenses
    }