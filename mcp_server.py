"""
MCP Server using FastMCP
Exposes: five tools, one resource, one prompt
Run with: python mcp_server.py
"""

from fastmcp import FastMCP
import core
mcp = FastMCP("Library-Server")

#TOOLS

#Books
@mcp.tool()
def get_all_books() -> str:
    """List all books in the database. Returns a formatted string with titles, authors and years."""
    books = core.get_all_books()
    if not books:
        return "No books found in the library."
    return "\n".join([f"{book.id}: '{book.title}' by {book.author} ({book.year})" for book in books])
    

@mcp.tool()
def get_book(book_id: int) -> str:
    """Get details of a book by its ID."""
    book = core.get_book(book_id)
    if not book:
        return f"Book with ID {book_id} not found."
    return f"{book.id}: '{book.title}' by {book.author} ({book.year})"



@mcp.tool()
def add_book(title: str, author: str, year: int) -> str:
    """Add a new book to the library."""
    book = core.add_book(title, author, year)
    return f"Book '{title}' added successfully with ID {book.id}!" if book else "Error adding book."


@mcp.tool()
def add_book_string(title: str, author: str, year_str: str):
    """
    SIMILAR OPERATION: Quick method that accepts the year as text 
    and returns a JSON-like dictionary summary.
    """
    return core.add_book_from_string(title, author, year_str)
    

@mcp.tool()
def delete_book(book_id: int) -> str:
    """Delete a book by its ID."""
    book = core.get_book(book_id)
    if not book:
        return f"Book with ID {book_id} not found."
    core.delete_book(book_id)
    return f"Book with ID {book_id} deleted successfully!"



@mcp.tool()
def update_book(book_id: int, title: str = None, author: str = None, year: int = None) -> str:
    """Update book details by its ID."""
    book = core.get_book(book_id)
    if not book:
        return f"Book with ID {book_id} not found."
    updated_book = core.update_book(book_id, title, author, year)
    if updated_book:
        return f"Book with ID {book_id} updated successfully to '{updated_book.title}' by {updated_book.author} ({updated_book.year})!"
    return "Error: Failed to update book."



#Members

@mcp.tool()
def get_all_members() -> str:
    """List all members in the database."""
    members = core.get_all_members()
    if not members:
        return "There are no registered members."
    return "\n".join([
        f"ID {member.id}: Name: {member.name} | Email: {member.email}" 
        for member in members
    ])

@mcp.tool()
def get_member(member_id:int) -> str:
    """Get details of a member by its ID."""
    member = core.get_member(member_id)
    if not member:
        return f"Member with ID {member_id} not found"
    return f"ID {member.id}: Name: {member.name } | Email : {member.email}"


@mcp.tool()
def add_member(name:str, email:str) -> str:
    """Add a new member. Both name and email are strictly required."""
    member = core.add_member(name,email)
    if not member:
        return "Error: Could not add member to the database."
        
    return f"Success: Member '{member.name}' added with ID {member.id}."
   

@mcp.tool()
def delete_member(member_id: int) -> str:
    """Delete a member by its ID."""
    member = core.get_member(member_id)
    if not member:
        return f"Member with ID {member_id} not found."
    core.delete_member(member_id)
    return f"Member with ID {member_id} deleted successfully!"



@mcp.tool()
def update_member(member_id: int, name: str = None, email: str = None ) -> str:
    """Update member details by its ID."""
    member = core.get_member(member_id)
    if not member:
        return f"Member with ID {member_id} not found."
    
    updated_member = core.update_member(member_id,name,email)
    if updated_member:
        return f"Success: Member {member_id} updated. New name: {updated_member.name} | New email: {updated_member.email}"
    
    return "Error: Failed to update member."

 
#Borrowings

@mcp.tool()
def get_all_borrowing() -> str:
    """List all active borrowings in the database (who has which book)."""
    borrowings = core.get_all_borrowings()
    if not borrowings:
        return "There are no active borrowings at the moment."
    
    lines = [
        f"Book: '{b['book_title']}' (ID: {b['book_id']}) -> Member: {b['member_name']} (ID: {b['member_id']})"
        for b in borrowings
    ]

    return "Active Borrowings:\n" + "\n".join(lines)


@mcp.tool()
def get_member_books(member_id: int) -> str:
    """List all books currently borrowed by a specific member."""
    member = core.get_member(member_id)
    if not member:
        return f"Error: Member with ID {member_id} not found."
    
    books = core.get_borrowed_books(member_id)
    if not books:
        return f"Member '{member.name}' (ID: {member_id}) has no borrowed books at the moment."
    
    books_list = [f"- ID {b.id}: {b.title} ({b.year})" for b in books]

    return f"Books borrowed by {member.name}:\n" + "\n".join(books_list)


@mcp.tool()
def get_book_borrower(book_id: int) -> str:
    """Check who is currently borrowing a specific book."""
    book = core.get_book(book_id)
    if not book:
        return f"Error: Book with ID {book_id} not found."
    
    borrower = core.get_book_owner(book_id)
    if not borrower:
        return f"The book '{book.title}' (ID: {book_id} is currently available in the library)."
    
    return (f"The book '{book.title}' (ID: {book_id}) is currently borrowed by: "
            f"{borrower.name} (Member ID: {borrower.id}, Email: {borrower.email}).")


@mcp.tool()
def borrow_book(member_id: int , book_id: int) -> str:
    """Assign a book to a member (Borrowing process). Requires both Member ID and Book ID."""
    result = core.borrow_book(member_id,book_id)
    if result == "success":
        return f"Success: Book {book_id} has been borrowed by Member {member_id}."
    
    elif result == "book_not_found":
        return f"Error: Book with ID {book_id} does not exist."
    
    elif result == "member_not_found":
        return f"Error: Member with ID {member_id} does not exist."
    
    elif result == "already_borrowed":
        return f"Error: Book {book_id} is already out on loan to someone else."
    
    elif result == "limit_reached":
        return f"Error: Member with ID {member_id} has reached the limit of 3 books" 
    
    else:
        return "Error: An unexpected issue occurred during the borrowing process."


@mcp.tool()
def return_book(member_id: int, book_id: int) -> str:
    """Handle the book return process. Ensures the book is being returned by the correct member."""
    result = core.return_book(member_id,book_id)
    if result == "success":
        return f"Success: Book ID {book_id} has been returned by Member ID {member_id}. It is now available!"
    
    elif result == "book_not_found":
        return f"Error: Book with ID {book_id} was not found in the system."
    
    elif result == "member_not_found":
        return f"Error: Member with ID {member_id} was not found."
    
    elif result == "not_borrowed_by_member":
        return f"Error: Member {member_id} cannot return Book {book_id} because they are not the current holder."
    
    else:
        return "Error: An unexpected issue occurred during the return process."
    


#RESOURCES
@mcp.resource("library://schema")
def get_schema() -> str:
    """Read the database schema and business rules."""
    path = "schema.txt" 
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    


@mcp.resource("info://app")
def get_app_info() -> str:
    """Returns general information about this MCP server / app."""
    return (
        "### LIBRARY SYSTEM METADATA ###\n"
        "Version: 2.1.0 (Stable)\n"
        "Environment: Development/Testing\n"
        "Data Storage: Local JSON/SQLite\n"
        "Entities Managed: Books, Library Members\n"
        "Business Rule: No entries allowed with publication year > 2026.\n"
        "Operational Status: All systems nominal."
    )



#PROMPTS

@mcp.prompt("inventory_analysis")
def inventory_analysis_prompt():
    """Instructions for the agent to analyze the professional library inventory."""
    return (
        "You are a Professional Library Manager. Your primary goal is to maintain a "
        "high-quality collection of Books and ensure all Members follow the rules.\n\n"
        
        "DIRECTIONS FOR ANALYSIS:\n"
        "1. DATA CONSTRAINTS: Check the 'library://schema' resource for publication year constraints.\n"
        "2. SYSTEM AUDIT:: Review 'info://app' for current system status and metadata.\n"
        "3. MEMBER COMPLIANCE: Use 'get_all_borrowings' to identify members with active loans. "
        "IMPORTANT: If a member is at the 3-book limit, list the specific Book IDs and Titles they hold.\n"
        "4. CROSS-REFERENCE: Flag any 'books from the future' (> 2026) or duplicate member emails.\n"
        "5. ORPHANED DATA: Identify books currently marked as borrowed but assigned to non-existent members.\n\n"
        
        "REPORTING REQUIREMENTS:\n"
        "- Provide a 'Collection Integrity' summary (Future books, data errors).\n"
        "- Provide a 'Borrowers Status' summary (Members at limit, overdue suggestions).\n"
        "- Always fetch real-time data using tools; do not rely on conversation history for inventory counts.\n\n"

       
        "Your analysis should be thorough and provide actionable insights to maintain the integrity of the library's collection."
    )




if __name__ == "__main__":
     mcp.run(transport="sse", host="127.0.0.1", port=8002)