from sqlmodel import SQLModel, create_engine, Session
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "database.db")
DATABASE_URL = f"sqlite:///{DB_FILE}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
