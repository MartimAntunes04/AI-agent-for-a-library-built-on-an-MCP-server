from sqlmodel import Relationship, SQLModel, Field
from typing import List, Optional

class Book(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    author: str
    year: Optional[int] = None
    owner_id: Optional[int] = Field(default=None, foreign_key="member.id")
    owner: List["Member"] = Relationship(back_populates="borrowed_books")


class Member(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    borrowed_books: List["Book"] = Relationship(back_populates="owner")