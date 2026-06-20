# create_engine → creates connection with database
from sqlalchemy import create_engine

# sessionmaker → creates database sessions
# Session means opening conversation with database
from sqlalchemy.orm import sessionmaker

# declarative_base → helps create database tables using Python classes
from sqlalchemy.ext.declarative import declarative_base



# ----------------------------
# DATABASE DETAILS
# ----------------------------

# Database username
MYSQL_USER = "root"

# Database password
MYSQL_PASSWORD = "root"

# Database location
# localhost = database running on your own computer
MYSQL_HOST = "localhost"

# MySQL default port
MYSQL_PORT = "3306"

# Database name
MYSQL_DATABASE = "fastapi_db"



# ----------------------------
# CREATE DATABASE URL
# ----------------------------

# Combine everything into one database address
# mysql+pymysql://username:password@host:port/database

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}"
    f"/{MYSQL_DATABASE}"
)



# ----------------------------
# CREATE DATABASE CONNECTION
# ----------------------------

# Engine = actual connection road to database
engine = create_engine(DATABASE_URL)



# ----------------------------
# CREATE SESSION
# ----------------------------

# SessionLocal creates database sessions

SessionLocal = sessionmaker(

    # Do not automatically save changes
    autoflush=False,

    # We manually decide when to commit
    autocommit=False,

    # Connect session with engine
    bind=engine
)



# ----------------------------
# DATABASE ACCESS FUNCTION
# ----------------------------

# This function gives DB connection
# and closes it automatically

def get_db():

    # Open database connection
    db = SessionLocal()

    try:

        # Give connection to API
        yield db

    finally:

        # Close connection after work done
        db.close()



# ----------------------------
# CREATE BASE CLASS
# ----------------------------

# All database models inherit from this

Base = declarative_base()