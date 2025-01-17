from typing import Optional


class Book:
    title: Optional[str]
    author: str

    def __init__(self, author: str, title: Optional[str] = None):
        self.author = author
        self.title = title
