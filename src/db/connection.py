from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def get_engine():
    db_user = os.getenv("DB_USER")
    db_name = os.getenv("DB_NAME")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    if not all([db_user, db_name, db_host, db_port]):
        raise ValueError("One or more database environment variables are missing")

    return create_engine(
        f"postgresql+psycopg2://{db_user}@{db_host}:{db_port}/{db_name}"
    )
