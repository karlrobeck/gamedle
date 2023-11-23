from typing import Any, Generator
from sqlmodel import Session
from api.database.models import engine


def getSession() -> Generator[Session, Any, None]:
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
