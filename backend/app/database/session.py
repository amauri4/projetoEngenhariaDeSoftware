from contextlib import contextmanager
from database.base import SessionLocal

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
