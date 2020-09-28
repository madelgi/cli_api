from sqlalchemy import String, Column, Integer, Text

from cli_api.extensions import db



class Script(db.Model):

    __tablename__ = 'script'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Integer)
    name = Column(String)
    version = Column(Integer)
    content = Column(Text)
