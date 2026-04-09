from sqlmodel import Session, func, select
from database import engine, create_db_and_tables
from models import Book, Member

#Books

#Standard Add (Input: int, Output: Book Object)
def add_book(title:str, author:str, year:int):
    if year > 2026:
        raise ValueError("BUSINESS RULE VIOLATION: Books from the future (post-2026) are not allowed.")
    
    with Session(engine) as session:
        book = Book(title=title, author=author, year=year)
        session.add(book)
        session.commit()
        session.refresh(book)
        return book
    

#Quick Add (Input: str, Output: dict) - A VARIAÇÃO
def add_book_from_string(title: str, author:str, year_str:str):
    try:
        year_int = int(year_str)
        book = add_book(title,author,year_int)

        return {
            "status": "success",
            "summary": f"{book.title} by {book.author} ({book.year})"
        }
    
    except ValueError:
        return {"status": "error", "message": "Invalid year format"}
    

def get_all_books():
    with Session(engine) as session:
        statement = select(Book)
        results = session.exec(statement)
        return results.all()
    

def get_book(book_id:int):
    with Session(engine) as session:
        book = session.get(Book, book_id)
        return book
    

def delete_book(book_id:int):
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if book:
            session.delete(book)
            session.commit()
            return True
        return False
    
def update_book(book_id:int, title:str=None, author:str=None, year:int=None):
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if book:
            if title:
                book.title = title
            if author:
                book.author = author
            if year:
                book.year = year
            session.add(book)
            session.commit()
            session.refresh(book)
            return book
        return None
    



#Members

def add_member(name:str, email:str):
    with Session(engine) as session:
        member = Member(name=name, email=email)
        session.add(member)
        session.commit()
        session.refresh(member)
        return member
    
def get_all_members():
    with Session(engine) as session:
        statement = select(Member)
        results = session.exec(statement)
        return results.all()
    
def get_member(member_id:int):
    with Session(engine) as session:
        member = session.get(Member, member_id)
        return member
    
def delete_member(member_id:int):
    with Session(engine) as session:
        member = session.get(Member, member_id)
        if member:
            session.delete(member)
            session.commit()
            return True
        return False
    
def update_member(member_id:int, name:str=None, email:str=None):
    with Session(engine) as session:
        member = session.get(Member, member_id)
        if member:
            if name:
                member.name = name
            if email:
                member.email = email
            session.add(member)
            session.commit()
            session.refresh(member)
            return member
        return None



#Borrowings  
 
def borrow_book(member_id:int, book_id:int):
    with Session(engine) as session:
        member = session.get(Member, member_id)
        book = session.get(Book, book_id)
        
        if not member:
            return "member_not_found"
        
        if not book:
            return "book_not_found"
        
        if book.owner_id is not None:
            return "already_borrowed"
        
        statement = select(func.count(Book.id)).where(Book.owner_id == member_id)
        count = session.exec(statement).one()

        if count >= 3:
            return "limit_reached"
        
        book.owner_id = member_id
        session.add(book)
        session.commit()
        session.refresh(book)
        return "success"
    
def get_borrowed_books(member_id:int):
    with Session(engine) as session:
        member = session.get(Member, member_id)
        if member:
            statement = select(Book).where(Book.owner_id == member_id)
            results = session.exec(statement)
            return results.all()
        return None
    
def get_book_owner(book_id:int):
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if book and book.owner_id:
            owner = session.get(Member, book.owner_id)
            return owner
        return None

def return_book(member_id:int , book_id:int):
    with Session(engine) as session:
        book = session.get(Book, book_id)
        member = session.get(Member,member_id)
        if not member:
            return "member_not_found"
        
        if not book:
            return "book_not_found"

        if book.owner_id != member_id:
            return "not_borrowed_by_member"
        
        book.owner_id = None
        session.add(book)
        session.commit()
        session.refresh(book)
        return "success"
    

def get_all_borrowings():
    with Session(engine) as session:
        
        statement = select(Book, Member).where(Book.owner_id == Member.id)
        results = session.exec(statement).all()
        
        borrowings = []
        for book, member in results:
            borrowings.append({
                "book_id": book.id,
                "book_title": book.title,
                "member_id": member.id,
                "member_name": member.name
            })
        return borrowings
    
if __name__ == "__main__":
    create_db_and_tables()