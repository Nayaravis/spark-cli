# cli.py
import click
from utils import create_dot_spark, read_dot_spark, get_current_context_id, format_timestamp, validate_spark_id
from helpers import (
    create_context, get_context_by_id, update_context, delete_context,
    create_spark, get_spark_by_id, update_spark, delete_spark,
    create_collection, get_collection_by_id, update_collection, delete_collection,
    get_all_contexts, get_sparks_by_context, get_sparks_by_collection,
    get_sparks_from_today, search_sparks, get_all_collections,
    get_collection_by_name, add_spark_to_collection, remove_spark_from_collection
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from string import ascii_letters, digits
import os

engine = create_engine("sqlite:///lib/db/spark_store.db")
Session = sessionmaker(bind=engine)

RESERVED_STRINGS = {"all", "list", "help"}

def clean_alphanum(value):
    cleaned = ''.join(c for c in value if c in ascii_letters + digits + " -_").lower()
    return cleaned

def validate_project_name(ctx, param, value):
    cleaned = clean_alphanum(value)
    if len(cleaned) < 3:
        raise click.BadParameter("Project name must be at least 3 alphanumeric characters.")
    if not cleaned:
        raise click.BadParameter("Project name cannot be empty after removing non-alphanumerics.")
    return cleaned

def validate_collection_name(ctx, param, value):
    cleaned = clean_alphanum(value)
    if cleaned in RESERVED_STRINGS:
        raise click.BadParameter(f"'{cleaned}' is a reserved word.")
    if len(cleaned) < 3:
        raise click.BadParameter("Collection name must be at least 3 alphanumeric characters.")
    return cleaned

def get_session():
    return Session()

@click.group()
def cli():
    """Spark - Capture and organize your coding ideas"""
    pass

@click.command("init", help="creates a new spark context in the current directory")
@click.option('--project-name', prompt='Project name', callback=validate_project_name, help='Name of the project')
@click.option('--default-collection', default='general', prompt='Default collection', callback=validate_collection_name, help='Default collection for sparks')
def create_context_cmd(project_name, default_collection):
    try:
        create_dot_spark(project_name, default_collection)
        click.secho("✓ .spark file created successfully in current directory", fg="green")
    except Exception as e:
        click.secho(f"✗ {str(e)}", fg="red")
        raise click.Abort()

@click.command("add", help="add a new spark")
@click.argument('content')
@click.option('--collection', '-c', help='Collection name')
def add_spark(content, collection):
    try:
        session = get_session()
        dot_config = read_dot_spark()
        context_id = get_current_context_id(session)
        
        # Create spark
        spark = create_spark(session, content, get_context_by_id(session, context_id))
        
        # Add to collection if specified
        if collection:
            collection_obj = get_collection_by_name(session, collection)
            if not collection_obj:
                collection_obj = create_collection(session, collection)
            add_spark_to_collection(session, spark.id, collection_obj.id)
        else:
            # Add to default collection
            default_collection_obj = get_collection_by_name(session, dot_config["default_collection"])
            if not default_collection_obj:
                default_collection_obj = create_collection(session, dot_config["default_collection"])
            add_spark_to_collection(session, spark.id, default_collection_obj.id)
        
        click.secho(f"✓ Spark #{spark.id} added successfully", fg="green")
    except Exception as e:
        click.secho(f"✗ {str(e)}", fg="red")

@click.command("list", help="list sparks")
@click.option('--collection', '-c', help='Filter by collection name')
@click.option('--today', '-t', is_flag=True, help='Show only today\'s sparks')
@click.option('--context', '-ctx', help='Show sparks from specific context path')
def list_sparks(collection, today, context):
    try:
        session = get_session()
        
        if context:
            context_obj = get_context_by_working_dir(session, context)
            if not context_obj:
                click.secho(f"✗ No context found for path: {context}", fg="red")
                return
            sparks = get_sparks_by_context(session, context_obj.id)
        else:
            context_id = get_current_context_id(session)
            if today:
                sparks = get_sparks_from_today(session, context_id)
            elif collection:
                collection_obj = get_collection_by_name(session, collection)
                if not collection_obj:
                    click.secho(f"✗ Collection '{collection}' not found", fg="red")
                    return
                sparks = get_sparks_by_collection(session, collection_obj.id)
            else:
                sparks = get_sparks_by_context(session, context_id)
        
        if not sparks:
            click.secho("No sparks found", fg="yellow")
            return
            
        for spark in sparks:
            click.echo(f"{spark.id}: {spark.content} [{format_timestamp(spark.created_at)}]")
            
    except Exception as e:
        click.secho(f"✗ {str(e)}", fg="red")

@click.command("collections", help="manage collections")
@click.argument('action', required=False)
@click.argument('name', required=False)
@click.argument('spark_id', required=False, type=int)
def collections_cmd(action, name, spark_id):
    try:
        session = get_session()
        
        if not action:
            # List all collections
            collections = get_all_collections(session)
            if not collections:
                click.secho("No collections found", fg="yellow")
                return
                
            for collection in collections:
                click.echo(f"{collection.name} ({len(collection.sparks)} sparks)")
            return
            
        if action == "create" and name:
            collection = create_collection(session, name)
            click.secho(f"✓ Collection '{name}' created", fg="green")
        elif action == "add" and name and spark_id:
            collection_obj = get_collection_by_name(session, name)
            if not collection_obj:
                collection_obj = create_collection(session, name)
            add_spark_to_collection(session, spark_id, collection_obj.id)
            click.secho(f"✓ Spark #{spark_id} added to '{name}'", fg="green")
        else:
            click.secho("Invalid command. Use: collections [create|add] [name] [spark_id]", fg="red")
            
    except Exception as e:
        click.secho(f"✗ {str(e)}", fg="red")

@click.command("search", help="search sparks")
@click.argument('query')
def search_sparks_cmd(query):
    try:
        session = get_session()
        context_id = get_current_context_id(session)
        sparks = search_sparks(session, context_id, query)
        
        if not sparks:
            click.secho(f"No sparks found for '{query}'", fg="yellow")
            return
            
        for spark in sparks:
            click.echo(f"{spark.id}: {spark.content}")
            
    except Exception as e:
        click.secho(f"✗ {str(e)}", fg="red")

@click.command("show", help="show spark details")
@click.argument('spark_id', type=int)
def show_spark(spark_id):
    try:
        session = get_session()
        spark = validate_spark_id(session, spark_id)
        
        click.echo(f"ID: {spark.id}")
        click.echo(f"Content: {spark.content}")
        click.echo(f"Created: {format_timestamp(spark.created_at)}")
        click.echo(f"Updated: {format_timestamp(spark.updated_at)}")
        if spark.collections:
            collections = ", ".join([c.name for c in spark.collections])
            click.echo(f"Collections: {collections}")
            
    except Exception as e:
        click.secho(f"✗ {str(e)}", fg="red")

@click.command("edit", help="edit a spark")
@click.argument('spark_id', type=int)
@click.argument('content')
def edit_spark(spark_id, content):
    try:
        session = get_session()
        spark = validate_spark_id(session, spark_id)
        update_spark(session, spark_id, content=content)
        click.secho(f"✓ Spark #{spark_id} updated", fg="green")
    except Exception as e:
        click.secho(f"✗ {str(e)}", fg="red")

@click.command("delete", help="delete a spark")
@click.argument('spark_id', type=int)
def delete_spark_cmd(spark_id):
    try:
        session = get_session()
        spark = validate_spark_id(session, spark_id)
        delete_spark(session, spark_id)
        click.secho(f"✓ Spark #{spark_id} deleted", fg="green")
    except Exception as e:
        click.secho(f"✗ {str(e)}", fg="red")

# Add all commands to CLI
cli.add_command(create_context_cmd)
cli.add_command(add_spark)
cli.add_command(list_sparks)
cli.add_command(collections_cmd)
cli.add_command(search_sparks_cmd)
cli.add_command(show_spark)
cli.add_command(edit_spark)
cli.add_command(delete_spark_cmd)

if __name__ == "__main__":
    cli()