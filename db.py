from sqlmodel import SQLModel, create_engine
from config import DB_NAME

# Database setup
engine = create_engine(f"sqlite:///{DB_NAME}")

def create_tables():
    SQLModel.metadata.create_all(engine)