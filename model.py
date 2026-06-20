# Import Column → used to create columns inside table
# Integer → numbers
# VARCHAR → text
from sqlalchemy import Column, Integer, VARCHAR

# Import Base
# Base is the parent class which tells SQLAlchemy:
# "This class should become a database table"
from database import Base

# Create Book table blueprint
# Every book we save will follow this structure
class Book(Base):

    # Actual table name inside database
    # Database will create:
    # books
    __tablename__ = "books"


    # Create ID column
    # Integer → only numbers
    # primary_key=True → unique identity for every row
    # index=True → searching becomes faster
    id = Column(Integer,primary_key=True,index=True)


    # Create title column
    # VARCHAR(255) → text allowed up to 255 letters
    title = Column(VARCHAR(255))

    # Create author column
    author = Column(VARCHAR(255))


    # Create publication date column
    # Stored as text here
    public_date = Column(VARCHAR(255))