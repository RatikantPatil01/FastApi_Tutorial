# We are bringing FastAPI tools to make our API
from fastapi import FastAPI, status

# This helps us show errors nicely
from fastapi.exceptions import HTTPException

# This helps check if user sends correct data
from pydantic import BaseModel


# This is our small toy box (database for now)
# It already has one book inside
books = [
    {
        "id": 1,
        "title": "Story Of KGF",
        "author": "Yash",
    }
]

# Creating our FastAPI app
app = FastAPI()


# --------------------------
# GET ALL BOOKS
# --------------------------

# When someone opens /get-books
# Show all books
@app.get("/get-books")
def get_books():

    # Return complete books list
    return books


# --------------------------
# CREATE BOOK STRUCTURE
# --------------------------

# This tells FastAPI:
# "Every new book must have these fields"
class Book(BaseModel):

    # Book must have ID
    id: int

    # Book must have title
    title: str

    # Book must have author
    author: str


# --------------------------
# GET SINGLE BOOK
# --------------------------

# Example:
# /get-book/1
@app.get("/get-book/{book_id}")
def get_book_by_id(book_id: int):

    # Look inside every book
    for book in books:

        # If ID matches
        if book["id"] == book_id:

            # Return success message
            return {
                "message": "Book Found Successfully",
                "data": book
            }

    # If loop finishes and nothing found
    # show error
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book Not Found"
    )


# --------------------------
# CREATE NEW BOOK
# --------------------------

# User sends new book data
@app.post("/create-book")
def create_book(book: Book):

    # Convert object → dictionary
    new_book = book.model_dump()

    # Put new book into toy box
    books.append(new_book)

    # Return success
    return {
        "message": "Book Added Successfully",
        "data": new_book
    }


# --------------------------
# UPDATE BOOK STRUCTURE
# --------------------------

# This tells what data can come
# while updating
class BookUpdate(BaseModel):

    id: int
    title: str
    author: str


# --------------------------
# UPDATE BOOK
# --------------------------

@app.put("/book-update/{book_id}")
def update_book(book_id: int, book_update: BookUpdate):

    # Search every book
    for book in books:

        # If book found
        if book["id"] == book_id:

            # Replace old title
            book["title"] = book_update.title

            # Replace old author
            book["author"] = book_update.author

            # Return updated book
            return {
                "message": "Book Updated Successfully",
                "data": book
            }

    # If no book found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book Id Not Found"
    )


# --------------------------
# DELETE BOOK
# --------------------------

@app.delete("/delete-book/{book_id}")
def delete_book(book_id: int):

    # Search every book
    for book in books:

        # If found
        if book["id"] == book_id:

            # Remove from list
            books.remove(book)

            # Return success
            return {
                "message": "Book Deleted Successfully!"
            }

    # If not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book Not Found"
    )