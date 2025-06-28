from fastapi import Body, FastAPI
import uvicorn

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title One part 2", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title five", "author": "Author Five", "category": "english"},
    {"title": "Title Seven", "author": "Author Six", "category": "math"},
    {"title": "Title Six", "author": "Author Six", "category": "math"},
]


@app.get("/")
async def first_api():
    return {"message": "hello World"}


@app.get("/books")
async def get_books_list() -> list:

    return BOOKS


@app.get("/books/{book_title}")
async def get_book_by_path(book_title: str) -> dict:

    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book

    return {"message": "Book is not present", "status code": 404}


@app.get("/books/")
async def get_book_by_query(category: str):
    booksToReturn = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            booksToReturn.append(book)

    if booksToReturn:
        return booksToReturn

    return {"message": "book is not present", "status code": 404}


@app.get("/books/{book_author}/")
async def get_books_by_param_and_query(book_author: str, category: str):
    booksToReturn = []
    for book in BOOKS:
        if (
            book.get("category").casefold() == category.casefold()
            and book.get("author").casefold() == book_author.casefold()
        ):
            booksToReturn.append(book)

    if booksToReturn:
        return booksToReturn

    return {"message": "book is not present", "status code": 404}


@app.get("/booksByAuthor/")
async def get_books_author_name(book_author: str) -> list[dict]:
    booksToReturn = []
    for book in BOOKS:
        if book.get("author").casefold() == book_author.casefold():
            booksToReturn.append(book)

    if booksToReturn:
        return booksToReturn

    return [{"message": "book si not present", "status code": 404}]


@app.post("/books/createBook")
async def create_book(new_book=Body()) -> dict:

    BOOKS.append(new_book)

    return {"message": "book succefully added", "book": new_book}


@app.put("/books/updateBook")
async def update_book(update_book=Body()) -> dict:

    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == update_book.get("title").casefold():
            BOOKS[i] = update_book
            return {"message": "book got updated successfuly"}

    return {"message": "book not found", "status code": 404}


@app.delete("books/deleteBook/{book_title}")
async def delete_book(book_title: str) -> dict:

    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            BOOKS.remove(book_title)

            return {"message": "book got deleted"}

    return {"message": "book not found", "status code": 404}


if __name__ == "__main__":
    # to reload use app as an import to enable reload
    uvicorn.run("books:app", host="0.0.0.0", port=8000, reload=True)

    # uvicorn.run(app, host="0.0.0.0", port=8000)
