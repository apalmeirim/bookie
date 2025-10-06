from dataclasses import dataclass
from typing import Optional

@dataclass
class Book:
    id: Optional[int]
    title: str
    author: Optional[str]
    year: Optional[int]
    genre: Optional[str]
    rating: Optional[int]
    notes: Optional[str]

