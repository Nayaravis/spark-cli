# utils.py
import yaml
from pathlib import Path
import os
from datetime import datetime

def create_dot_spark(project_name, default_collection):
    dot_context = {
        "project_name": project_name,
        "default_collection": default_collection
    }

    with open(".spark", "w") as spark_file:
        yaml.dump(dot_context, spark_file)

def read_dot_spark():
    if not Path(".spark").exists():
        raise FileNotFoundError("No .spark file found. Run 'spark init' first.")
    
    with open(".spark", "r") as spark_file:
        return yaml.safe_load(spark_file)

def get_current_context_id(session):
    dot_config = read_dot_spark()
    working_dir = os.getcwd()
    
    from helpers import get_context_by_working_dir
    context = get_context_by_working_dir(session, working_dir)
    
    if not context:
        from helpers import create_context
        context = create_context(session, working_dir, dot_config["project_name"])
    
    return context.id

def format_timestamp(timestamp):
    if not timestamp:
        return "N/A"
    return timestamp.strftime("%Y-%m-%d %H:%M")

def validate_spark_id(session, spark_id):
    from helpers import get_spark_by_id
    spark = get_spark_by_id(session, spark_id)
    if not spark:
        raise ValueError(f"Spark with ID {spark_id} not found")
    return spark