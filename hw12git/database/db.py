from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///hw12rest.db"
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
