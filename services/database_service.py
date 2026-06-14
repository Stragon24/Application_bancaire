from calendar import monthrange
from database.database import SessionLocal
from database.models import (
    Transaction,
)
from sqlalchemy import func
from sqlalchemy import extract

from database.database import SessionLocal

from database.models import (
    Transaction,
    UserExclusion
)

import os

INTERNAL_TRANSFER_CATEGORY = ("Virements émis de comptes à comptes")

EXTERNAL_TRANSFER_CATEGORY = ("Virements émis")

IGNORED_CATEGORY = ("Prélèvements cartes débit différé et cartes crédit conso")

def get_existing_months():

    session = SessionLocal()

    rows = (
        session.query(
            extract("year", Transaction.date),
            extract("month", Transaction.date)
        )
        .distinct()
        .all()
    )

    session.close()

    return {
        (
            int(year),
            int(month)
        )
        for year, month in rows
    }

def get_user_exclusions():

    session = SessionLocal()

    rows = (
        session.query(
            UserExclusion
        )
        .order_by(
            UserExclusion.exclusion_type,
            UserExclusion.value
        )
        .all()
    )

    session.close()

    return rows

def get_excluded_categories():

    session = SessionLocal()

    rows = (
        session.query(
            UserExclusion.value
        )
        .filter(
            UserExclusion.exclusion_type
            == "category"
        )
        .all()
    )

    session.close()

    return [
        r[0]
        for r in rows
    ]

def get_excluded_labels():

    session = SessionLocal()

    rows = (
        session.query(
            UserExclusion.value
        )
        .filter(
            UserExclusion.exclusion_type
            == "label"
        )
        .all()
    )

    session.close()

    return [
        r[0]
        for r in rows
    ]

def add_exclusion(
    exclusion_type,
    value
):

    session = SessionLocal()

    exists = (
        session.query(
            UserExclusion
        )
        .filter(
            UserExclusion.exclusion_type
            == exclusion_type,
            UserExclusion.value
            == value
        )
        .first()
    )

    if not exists:

        session.add(
            UserExclusion(
                exclusion_type=exclusion_type,
                value=value
            )
        )

        session.commit()

    session.close()

def delete_exclusion(
    exclusion_id
):

    session = SessionLocal()

    row = session.get(
        UserExclusion,
        exclusion_id
    )

    if row:

        session.delete(row)

        session.commit()

    session.close()

def get_all_categories():

    session = SessionLocal()

    rows = (
        session.query(
            Transaction.category
        )
        .distinct()
        .order_by(
            Transaction.category
        )
        .all()
    )

    session.close()

    return [
        r[0]
        for r in rows
        if r[0]
    ]

def get_all_labels():

    session = SessionLocal()

    rows = (
        session.query(
            Transaction.label
        )
        .distinct()
        .order_by(
            Transaction.label
        )
        .all()
    )

    session.close()

    return [
        r[0]
        for r in rows
        if r[0]
    ]

def get_transfer_details(
    year,
    month,
    category,
    apply_exclusions=False
):

    session = SessionLocal()

    query = (
        session.query(
            Transaction.label,
            func.sum(Transaction.amount)
        )
        .filter(
            Transaction.category == category,
            extract(
                "year",
                Transaction.date
            ) == year,
            extract(
                "month",
                Transaction.date
            ) == month
        )
    )

    if apply_exclusions:

        excluded_labels = (
            get_excluded_labels()
        )

        query = query.filter(
            ~Transaction.label.in_(
                excluded_labels
            )
        )

    rows = (
        query
        .group_by(
            Transaction.label
        )
        .all()
    )

    session.close()

    return [
        (
            label,
            abs(amount)
        )
        for label, amount in rows
    ]

def get_monthly_savings(
    year,
    apply_exclusions=False
):

    session = SessionLocal()

    result = []

    for month in range(1, 13):

        revenues_query = (
            session.query(
                func.sum(Transaction.amount)
            )
            .filter(
                Transaction.amount > 0,
                extract("year", Transaction.date) == year,
                extract("month", Transaction.date) == month,
                Transaction.category != IGNORED_CATEGORY
            )
        )

        expenses_query = (
            session.query(
                func.sum(Transaction.amount)
            )
            .filter(
                Transaction.amount < 0,
                extract("year", Transaction.date) == year,
                extract("month", Transaction.date) == month,
                Transaction.category != IGNORED_CATEGORY
            )
        )

        if apply_exclusions:

            excluded_categories = (
                get_excluded_categories()
            )

            excluded_labels = (
                get_excluded_labels()
            )

            revenues_query = revenues_query.filter(
                ~Transaction.category.in_(
                    excluded_categories
                )
            )

            revenues_query = revenues_query.filter(
                ~Transaction.label.in_(
                    excluded_labels
                )
            )

            expenses_query = expenses_query.filter(
                ~Transaction.category.in_(
                    excluded_categories
                )
            )

            expenses_query = expenses_query.filter(
                ~Transaction.label.in_(
                    excluded_labels
                )
            )

        revenues = (
            revenues_query.scalar()
            or 0
        )

        expenses = abs(
            expenses_query.scalar()
            or 0
        )

        result.append(
            (
                month,
                revenues - expenses
            )
        )

    session.close()

    return result

def get_transactions_by_period(
    year,
    month
):

    session = SessionLocal()

    transactions = (
        session.query(Transaction)
        .filter(
            extract(
                "year",
                Transaction.date
            ) == year,
            extract(
                "month",
                Transaction.date
            ) == month,
            Transaction.category != IGNORED_CATEGORY
        )
        .order_by(
            Transaction.date.desc()
        )
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
    apply_exclusions=False
):

    session = SessionLocal()

    revenues_query = (
        session.query(
            func.sum(Transaction.amount)
        )
        .filter(
            Transaction.amount > 0,
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month,
            Transaction.category != IGNORED_CATEGORY
        )
    )

    expenses_query = (
        session.query(
            func.sum(Transaction.amount)
        )
        .filter(
            Transaction.amount < 0,
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month,
            Transaction.category != IGNORED_CATEGORY
        )
    )

    if apply_exclusions:

        excluded_categories = (
            get_excluded_categories()
        )

        excluded_labels = (
            get_excluded_labels()
        )

        revenues_query = revenues_query.filter(
            ~Transaction.category.in_(
                excluded_categories
            )
        )

        revenues_query = revenues_query.filter(
            ~Transaction.label.in_(
                excluded_labels
            )
        )

        expenses_query = expenses_query.filter(
            ~Transaction.category.in_(
                excluded_categories
            )
        )

        expenses_query = expenses_query.filter(
            ~Transaction.label.in_(
                excluded_labels
            )
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

def get_category_expenses_month(year, month, apply_exclusions=False):

    session = SessionLocal()

    query = (
        session.query(
            Transaction.category,
            func.sum(Transaction.amount)
        )
        .filter(
            Transaction.amount < 0,
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month,
            Transaction.category != IGNORED_CATEGORY
        )
    )

    if apply_exclusions:

        excluded_categories = (
            get_excluded_categories()
        )

        excluded_labels = (
            get_excluded_labels()
        )

        query = query.filter(
            ~Transaction.category.in_(
                excluded_categories
            )
        )

        query = query.filter(
            ~Transaction.label.in_(
                excluded_labels
            )
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
    apply_exclusions=False
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
                extract("month", Transaction.date) == month,
                Transaction.category != IGNORED_CATEGORY
            )
        )

        if apply_exclusions:

            excluded_categories = (
                get_excluded_categories()
            )

            excluded_labels = (
                get_excluded_labels()
            )

            query = query.filter(
                ~Transaction.category.in_(
                    excluded_categories
                )
            )

            query = query.filter(
                ~Transaction.label.in_(
                    excluded_labels
                )
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

    existing_months = get_existing_months()

    ignored_months = set()

    imported = 0

    for t in transactions:

        transaction_month = (
            t["date"].year,
            t["date"].month
        )

        if transaction_month in existing_months:

            ignored_months.add(
                transaction_month
            )

            continue

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

    return (
        imported,
        ignored_months
    )