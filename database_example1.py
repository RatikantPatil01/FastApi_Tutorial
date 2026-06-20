# Import FastAPI -> this is the thing that creates our website/API
from fastapi import FastAPI, Depends

# Import database connection and function to connect with DB
from database import get_db, engine

# Session is used to talk with database
from sqlalchemy.orm import Session

# Import our database table model
import model

# BaseModel helps us check incoming data from user
from pydantic import BaseModel


# Create the FastAPI application
app = FastAPI()


# This is the shape of data we expect from user
# Example:
# {
#   "id":1,
#   "title":"Python",
#   "author":"John",
#   "public_date":"2026"
# }

class BookStore(BaseModel):

    # Book ID (unique number)
    id: int

    # Name of book
    title: str

    # Author name
    author: str

    # Published date
    public_date: str


# ---------------------------------------------
# CREATE BOOK
# POST → used to send new data
# URL → /books
# ---------------------------------------------

@app.post("/books")
def create_book(book: BookStore, db: Session = Depends(get_db)):

    # Create new book object using received data
    new_book = model.Book(
        id=book.id,
        title=book.title,
        author=book.author,
        public_date=book.public_date
    )

    # Put book inside database box
    db.add(new_book)

    # Save permanently
    db.commit()

    # Refresh so latest saved data comes back
    db.refresh(new_book)

    # Return saved book
    return new_book


# ---------------------------------------------
# GET SINGLE BOOK
# GET → used to read data
# URL Example:
# /get-book/1
# ---------------------------------------------

@app.get("/get-book/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):

    # Find first book where ID matches
    book = (
        db.query(model.Book)
        .filter(model.Book.id == book_id)
        .first()
    )

    # Send book back
    return book


# ---------------------------------------------
# GET ALL BOOKS
# URL:
# /get-all-book
# ---------------------------------------------

@app.get("/get-all-book")
def get_book(db: Session = Depends(get_db)):

    # Get all books from database
    book = db.query(model.Book).all()

    # Return list of books
    return book


# ---------------------------------------------
# UPDATE BOOK
# PUT → used to edit existing data
# URL Example:
# /update-book/1
# ---------------------------------------------

@app.put("/update-book/{book_id}")
def update_book(
    book: BookStore,
    book_id: int,
    db: Session = Depends(get_db)
):

    # Find matching ID
    # Change title, author, and date
    db.query(model.Book).filter(
        model.Book.id == book_id
    ).update({
        "title": book.title,
        "author": book.author,
        "public_date": book.public_date
    })

    # Save changes
    db.commit()

    return {"message": "Updated"}


# ---------------------------------------------
# DELETE BOOK
# DELETE → remove data
# URL Example:
# /delete-book/1
# ---------------------------------------------

@app.delete("/delete-book/{book_id}")
def update_book(
    book_id: int,
    db: Session = Depends(get_db)
):

    # Find book and remove it
    db.query(model.Book).filter(
        model.Book.id == book_id
    ).delete()

    # Save deletion
    db.commit()

    return {"message": "Deleted"}