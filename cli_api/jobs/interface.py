"""
Interface for models interacting with scripts.

"""
from typing import TypedDict


class JobInterface(TypedDict, total=False):
    id: str
    name: str
    user_id: int
    description: str
