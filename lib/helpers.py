from db.models import Base, Context, Spark, Collection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# engine = create_engine("sqlite:///db/spark_store.db")
# Session = sessionmaker(bind=engine)
# session = Session()

# Context CRUD
def create_context(session, working_dir, project_name):
    try:
        context = Context(
            working_directory=working_dir,
            project_name=project_name
        )
        session.add(context)
        session.commit()
        return context
    except Exception as e:
        session.rollback()
        raise e

def get_context_by_id(session, context_id):
    try:
        return session.query(Context).where(Context.id == context_id).first()
    except Exception as e:
        raise e

def update_context(session, context_id, **kwargs):
    try:
        context = get_context_by_id(session, context_id)
        if context:
            for key, value in kwargs.items():
                if hasattr(context, key) and key != "id":
                    setattr(context, key, value)
            session.commit()
            return context
        else:
            return None
    except Exception as e:
        session.rollback()
        raise e

def delete_context(session, context_id):
    try:
        context = get_context_by_id(session, context_id)
        if context:
            session.delete(context)
            session.commit()
        else:
            raise ValueError(f"Context with id {context_id} does not exist.")
    except Exception as e:
        session.rollback()
        raise e

# Spark CRUD
def create_spark(session, content, context):
    try:
        spark = Spark(
            content=content,
            context_id=context.id
        )
        session.add(spark)
        session.commit()
        return spark
    except Exception as e:
        session.rollback()
        raise e

def get_spark_by_id(session, spark_id):
    try:
        return session.query(Spark).where(Spark.id == spark_id).first()
    except Exception as e:
        raise e

def update_spark(session, spark_id, **kwargs):
    try:
        spark = get_spark_by_id(session, spark_id)
        if spark:
            for key, value in kwargs.items():
                if hasattr(spark, key) and key != "id":
                    setattr(spark, key, value)
            session.commit()
            return spark
        else:
            return None
    except Exception as e:
        session.rollback()
        raise e

def delete_spark(session, spark_id):
    try:
        spark = get_spark_by_id(session, spark_id)
        if spark:
            session.delete(spark)
            session.commit()
        else:
            raise ValueError(f"Spark with id {spark_id} does not exist.")
    except Exception as e:
        session.rollback()
        raise e

# Collection CRUD
def create_collection(session, name, description=None):
    try:
        collection = Collection(
            name=name,
            description=description
        )
        session.add(collection)
        session.commit()
        return collection
    except Exception as e:
        session.rollback()
        raise e

def get_collection_by_id(session, collection_id):
    try:
        return session.query(Collection).where(Collection.id == collection_id).first()
    except Exception as e:
        raise e

def update_collection(session, collection_id, **kwargs):
    try:
        collection = get_collection_by_id(session, collection_id)
        if collection:
            for key, value in kwargs.items():
                if hasattr(collection, key) and key != "id":
                    setattr(collection, key, value)
            session.commit()
            return collection
        else:
            return None
    except Exception as e:
        session.rollback()
        raise e

def delete_collection(session, collection_id):
    try:
        collection = get_collection_by_id(session, collection_id)
        if collection:
            session.delete(collection)
            session.commit()
        else:
            raise ValueError(f"Collection with id {collection_id} does not exist.")
    except Exception as e:
        session.rollback()
        raise e

# helpers.py (add these functions)
def get_context_by_working_dir(session, working_dir):
    try:
        return session.query(Context).where(Context.working_directory == working_dir).first()
    except Exception as e:
        raise e

def get_all_contexts(session):
    try:
        return session.query(Context).all()
    except Exception as e:
        raise e

def get_sparks_by_context(session, context_id):
    try:
        return session.query(Spark).where(Spark.context_id == context_id).all()
    except Exception as e:
        raise e

def get_sparks_by_collection(session, collection_id):
    try:
        collection = get_collection_by_id(session, collection_id)
        if collection:
            return collection.sparks
        return []
    except Exception as e:
        raise e

def get_sparks_from_today(session, context_id):
    try:
        from datetime import datetime, date
        today = date.today()
        return session.query(Spark).where(
            Spark.context_id == context_id,
            func.date(Spark.created_at) == today
        ).all()
    except Exception as e:
        raise e

def search_sparks(session, context_id, search_term):
    try:
        return session.query(Spark).where(
            Spark.context_id == context_id,
            Spark.content.ilike(f"%{search_term}%")
        ).all()
    except Exception as e:
        raise e

def get_all_collections(session):
    try:
        return session.query(Collection).all()
    except Exception as e:
        raise e

def get_collection_by_name(session, name):
    try:
        return session.query(Collection).where(Collection.name == name).first()
    except Exception as e:
        raise e

def add_spark_to_collection(session, spark_id, collection_id):
    try:
        spark = get_spark_by_id(session, spark_id)
        collection = get_collection_by_id(session, collection_id)
        
        if spark and collection:
            if collection not in spark.collections:
                spark.collections.append(collection)
                session.commit()
            return spark
        return None
    except Exception as e:
        session.rollback()
        raise e

def remove_spark_from_collection(session, spark_id, collection_id):
    try:
        spark = get_spark_by_id(session, spark_id)
        collection = get_collection_by_id(session, collection_id)
        
        if spark and collection:
            if collection in spark.collections:
                spark.collections.remove(collection)
                session.commit()
            return spark
        return None
    except Exception as e:
        session.rollback()
        raise e