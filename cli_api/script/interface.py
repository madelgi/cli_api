"""
Interface for models interacting with scripts.

"""
from typing import TypedDict


class ScriptInterface(TypedDict, total=False):
    name: str
    user: str
    content: str
    version: int
