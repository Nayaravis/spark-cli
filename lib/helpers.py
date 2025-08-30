from db.models import Base, Context, Spark
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///db/spark_store.db")
Session = sessionmaker(bind=engine)
session = Session()

def create_context(working_dir, project_name):
    context = Context(
        working_directory=working_dir,
        project_name=project_name
    )

    session.add(context)
    session.commit()

def create_spark(content, context):
    spark = Spark(
        content=content,
        context_id=context.id
    )

    session.add(spark)
    session.commit()