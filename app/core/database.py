import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/workflow"
)

# Retry connection
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()
        print("Database connected!")
        break
    except Exception as e:
        print("Database not ready, retrying...")
        time.sleep(2)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()