from sqlalchemy import String, Column, Integer, Text

from cli_api.extensions import db


class Script(db.Model):

    __tablename__ = "script"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Integer, db.ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    version = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
