from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class Post(Base):
    __tablename__ = 'Posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='FALSE', nullable=False)
    # created_at = Column(Text, server_default=text("datetime('now')"), nullable=False)