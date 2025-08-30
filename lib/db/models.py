from sqlalchemy import func
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Context(Base):
    __tablename__ = "contexts"

    id = Column(Integer(), primary_key=True)
    working_directory = Column(Text(), nullable=False)
    project_name = Column(Text())
    created_at = Column(DateTime(), server_default=func.now())

class Spark(Base):
    __tablename__ = "sparks"

    id = Column(Integer(), primary_key=True)
    content = Column(Text(), nullable=False)
    created_at = Column(DateTime(), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(), onupdate=func.now())
    context_id = Column(Integer(), ForeignKey("contexts.id"))