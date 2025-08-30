from sqlalchemy import func
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

spark_collection = Table(
    "spark_collections",
    Base.metadata,
    Column("spark_id", Integer(), ForeignKey("sparks.id")),
    Column("collection_id", Integer(), ForeignKey("collections.id"))
)

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

    context = relationship("Context", backref=backref("spark"))
    collections = relationship("Collection", secondary=spark_collection, back_populates="sparks")

class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer(), primary_key=True)
    name = Column(Text(), nullable=False)
    description = Column(Text())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    sparks = relationship("Spark", secondary=spark_collection, back_populates="collections")