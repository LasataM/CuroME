from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Password 'nalld@2005' becomes 'nalld%402005'
# Use %40 instead of @ for the password
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:nalld%402005@localhost:5432/curomedb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()