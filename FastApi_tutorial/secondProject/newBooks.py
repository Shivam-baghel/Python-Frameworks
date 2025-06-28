from typing import Optional
from fastapi import Body, FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

import uvicorn

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_year: int

    def __init__(self, id, title, author, description, rating, published_year):

        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_year = published_year


class BookRequest(BaseModel):

    id: Optional[int] = Field(description="Id is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_year: int = Field(ge=1500, le=2025)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithShivam",
                "description": "A new descriptio;n of a book",
                "rating": 4,
                "published year": 2023,
            }
        }
    }


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book", 5, 2000),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "A great Book", 5, 2002),
    Book(3, "Master Endpoints", "codingwithroby", "A very nice book", 5, 2003),
    Book(4, "HP1", "Author 1", "Book description", 2, 2012),
    Book(5, "HP2", "Author 2", "Book description", 3, 2011),
    Book(6, "HP3", "Author 3", "Book description", 1, 2023),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail=book_not_found())


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    bookToReturn = []
    for book in BOOKS:
        if book.rating == book_rating:
            bookToReturn.append(book)

    if bookToReturn:
        return bookToReturn
    else:
        return book_not_found()


@app.get("/booksByDate", status_code=status.HTTP_200_OK)
async def get_books_by_date(date: int = Query(gt=1500, lt=2026)):
    bookTorReturn = []

    for book in BOOKS:
        if book.published_year == date:
            bookTorReturn.append(book)

    if bookTorReturn:
        return bookTorReturn
    return book_not_found()


@app.post("/createBook", status_code=status.HTTP_201_CREATED)
async def create_book(request_book: BookRequest):

    new_book = Book(**request_book.model_dump())
    BOOKS.append(update_book_id(new_book))
    return {"status code": 200, "book": new_book}


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for bk in range(len(BOOKS)):
        if BOOKS[bk].id == book.id:
            BOOKS[bk] = book
            book_changed = True

    if not book_changed:
        raise HTTPException(status_code=404, detail=book_not_found())


@app.delete("/Books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_change = True
            break

    if not book_change:
        raise HTTPException(status_code=404, detail=book_not_found())


def update_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book


def book_not_found() -> dict:

    return {"messgae": "Book not found", "status code": 404}


if __name__ == "__main__":

    uvicorn.run("newBooks:app", host="0.0.0.0", port=8000, reload=True)
