from typing import Final

items: Final = ("a", "b")

def f(s: str) -> bool:
    return s in items
