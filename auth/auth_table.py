# Import engine (database connection)
# Import Base (contains all table information)
from auth_database import engine, Base


# Import model file
# Very important:
# This loads all table classes (like Book)
# so SQLAlchemy knows what tables to create
import models



# --------------------------------
# CREATE TABLES IN DATABASE
# --------------------------------

# Base.metadata
# → Contains information about all models

# create_all()
# → Create tables if they do not exist

# bind=engine
# → Use this database connection

Base.metadata.create_all(bind=engine)