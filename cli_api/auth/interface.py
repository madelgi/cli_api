"""
Interface for models interacting with scripts.

"""
from typing import TypedDict


class UserInterface(TypedDict, total=False):
    email: str
    password: str
    admin: bool
