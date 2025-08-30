from sqlalchemy import func
from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Context(Base):
    __tablename__ = "contexts"

    id = Column(Integer(), primary_key=True)
    working_directory = Column(Text(), nullable=False)
    project_name = Column(Text())
    created_at = Column(DateTime(), server_default=func.now())
