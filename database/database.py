# import os

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# os.makedirs("Application_bancaire/data", exist_ok=True)

# DATABASE_URL = "sqlite:///Application_bancaire/data/finance.db"

# engine = create_engine(DATABASE_URL)

# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine
# )

# Base = declarative_base()

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Dossier racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Dossier data
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Base SQLite
DB_PATH = DATA_DIR / "finance.db"

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

print(f"Base SQLite : {DB_PATH}")