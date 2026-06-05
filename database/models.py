from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime
)

from datetime import datetime

from database.database import Base


class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)

    date = Column(Date)

    label = Column(String(500))

    suggested_label = Column(String(500))

    category = Column(String(255))

    category_parent = Column(String(255))

    amount = Column(Float)

    comment = Column(String(1000))

    account_num = Column(String(255))

    account_label = Column(String(255))


class ImportedFile(Base):

    __tablename__ = "imported_files"

    id = Column(Integer, primary_key=True)

    filename = Column(String(500))

    file_hash = Column(String(64), unique=True)

    imported_at = Column(
        DateTime,
        default=datetime.utcnow
    )