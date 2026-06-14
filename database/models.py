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

class UserExclusion(Base):

    __tablename__ = "user_exclusions"

    id = Column(
        Integer,
        primary_key=True
    )

    exclusion_type = Column(
        String(50)
    )
    # category
    # label

    value = Column(
        String(500)
    )
    
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
