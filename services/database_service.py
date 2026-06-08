from calendar import monthrange
from database.database import SessionLocal
from database.models import (
    Transaction,
    ImportedFile
)
from sqlalchemy import func
from sqlalchemy import extract

from database.database import SessionLocal

import os

INTERNAL_TRANSFER_CATEGORY = (
    "Virements émis de comptes à comptes"
)

def get_transactions_by_period(year, month):

    session = SessionLocal()

    transactions = (
        session.query(Transaction)
        .filter(
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month
        )
        .order_by(Transaction.date.desc())
        .all()
    )

    session.close()

    return transactions

def get_available_years():

    session = SessionLocal()

    years = (
        session.query(
            extract("year", Transaction.date)
        )
        .distinct()
        .all()
    )

    session.close()

    return sorted(
        [
            int(y[0])
            for y in years
        ],
        reverse=True
    )

def get_dashboard_month_stats(
    year,
    month,
    exclude_internal=False
):

    session = SessionLocal()

    revenues_query = (
        session.query(
            func.sum(Transaction.amount)
        )
        .filter(
            Transaction.amount > 0,
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month
        )
    )

    expenses_query = (
        session.query(
            func.sum(Transaction.amount)
        )
        .filter(
            Transaction.amount < 0,
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month
        )
    )

    if exclude_internal:

        revenues_query = revenues_query.filter(
            Transaction.category
            != INTERNAL_TRANSFER_CATEGORY
        )

        expenses_query = expenses_query.filter(
            Transaction.category
            != INTERNAL_TRANSFER_CATEGORY
        )

    revenues = (
        revenues_query.scalar()
        or 0
    )

    expenses = (
        expenses_query.scalar()
        or 0
    )

    session.close()

    expenses = abs(expenses)

    return {
        "revenues": revenues,
        "expenses": expenses,
        "balance": revenues - expenses
    }

def get_category_expenses_month(year, month, exclude_internal=False):

    session = SessionLocal()

    query = (
        session.query(
            Transaction.category,
            func.sum(Transaction.amount)
        )
        .filter(
            Transaction.amount < 0,
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month
        )
    )

    if exclude_internal:

        query = query.filter(
            Transaction.category !=
            INTERNAL_TRANSFER_CATEGORY
        )

    rows = (
        query
        .group_by(Transaction.category)
        .all()
    )

    session.close()

    return [
        (cat, abs(amount))
        for cat, amount in rows
    ]

def get_monthly_expenses_year(
    year,
    exclude_internal=False
):

    session = SessionLocal()

    data = []

    for month in range(1, 13):

        query = (
            session.query(
                func.sum(Transaction.amount)
            )
            .filter(
                Transaction.amount < 0,
                extract("year", Transaction.date) == year,
                extract("month", Transaction.date) == month
            )
        )

        if exclude_internal:

            query = query.filter(
                Transaction.category
                != INTERNAL_TRANSFER_CATEGORY
            )

        amount = (
            query.scalar()
            or 0
        )

        data.append(
            (
                month,
                abs(amount)
            )
        )

    session.close()

    return data

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

import os


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