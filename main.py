from fastapi import FastAPI
from database import create_db_and_tables
import core

app = FastAPI()

#@app.get("/")
#async def root():
#    return {"message": "Hello World"}


# Criar a base de dados ao iniciar
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def home():
    return {"status": "Online"}



@app.get("/books", tags=["Books"])
def get_all_books():
    return core.get_all_books()

    

@app.get("/books/{book_id}", tags=["Books"])
def get_book(book_id: int):
    book = core.get_book(book_id)
    if book:
        return book
    return {"error": "Book not found"}


@app.post("/books", tags=["Books"])
def add_book(title: str, author: str, year: int):
    book = core.add_book(title, author, year)
    return{
        "status": "Book added",
        "book": book
    }



@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(book_id: int):
    success = core.delete_book(book_id)
    if success:
        return {"message": "Book deleted"}
    return {"error": "Book not found"}



@app.put("/books/{book_id}", tags=["Books"])
def update_book(book_id: int, title: str = None, author: str = None, year: int = None):
    book = core.update_book(book_id, title, author, year)
    if book:
        return book
    return {"error": "Book not found"}


#Members

@app.get("/members", tags=["Members"])
def get_all_members():
    return core.get_all_members()


@app.get("/members/{member_id}" ,tags=["Members"])
def get_member(member_id:int):
    member = core.get_member(member_id)
    if member:
        return member
    return {"error" : "Member not found"}



@app.post("/members", tags=["Members"])
def add_member(name:str, email:str):
    member = core.add_member(name,email)
    return{
        "status" : "Member added",
        "member" : member
    }


@app.delete("/members/{member_id}", tags=["Members"])
def delete_member(member_id:int):
    sucess = core.delete_member(member_id)
    if sucess:
        return {"message": "Member deleted"}
    return {"error": "Member not found"}


@app.put("/members/{member_id}", tags=["Members"])
def update_member(member_id:int, name:str = None, email:str = None):
    member = core.update_member(member_id,name,email)
    if member:
        return member
    return {"error": "Member not found"}



#Borrowings

@app.get("/borrowings" , tags=["Borrowings"])
def get_all_borrowings():
    return core.get_all_borrowings()

@app.get("/members/{member_id}/books", tags=["Borrowings"])
def get_member_books(member_id:int):
    books = core.get_borrowed_books(member_id)
    if books is not None:
        return books
    return {"error": "Member not found"}

@app.get("/books/{book_id}/borrower", tags=["Borrowings"])
def get_book_borrower(book_id:int):
    borrower = core.get_book_owner(book_id)
    if borrower is not None:
        return borrower
    return {"error": "Book not found or not borrowed"}

@app.post("/members/{member_id}/borrow/{book_id}", tags=["Borrowings"])
def borrow_book(member_id:int, book_id:int):
    result = core.borrow_book(member_id, book_id)
    if result == "success":
        return {"message": "Book borrowed successfully"}
    elif result == "book_not_found":
        return {"error": "Book not found"}
    elif result == "member_not_found":
        return {"error": "Member not found"}
    elif result == "already_borrowed":
        return {"error": "Book is already borrowed"}
    elif result == "limit_reached":
        return {"error: Member has reached the limit of 3 books"}
    else:
        return {"error": "An unexpected error occurred"}
    


@app.post("/members/{member_id}/return/{book_id}", tags=["Borrowings"])
def return_book(member_id:int, book_id:int):
    result = core.return_book(member_id, book_id)
    if result == "success":
        return {"message": "Book returned successfully"}
    elif result == "book_not_found":
        return {"error": "Book not found"}
    elif result == "member_not_found":
        return {"error": "Member not found"}
    elif result == "not_borrowed_by_member":
        return {"error": "This book was not borrowed by this member"}
    else:
        return {"error": "An unexpected error occurred"}
    