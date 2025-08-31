import click
from utils import create_dot_spark
from string import ascii_letters, digits

RESERVER_STRINGS = {"all", "list", "help"}

def clean_alphanum(value):
    cleaned = ''.join(c for c in value if c in ascii_letters + digits).lower()
    return cleaned

def validate_project_name(ctx, param, value):
    cleaned = clean_alphanum(value)
    if len(cleaned) < 3:
        raise click.BadParameter("Project name must be at least 3 alphanumeric characters.")
    if not cleaned:
        raise click.BadParameter("Project name cannot be empty after removing non-alphanumerics.")
    return cleaned

def validate_collection(ctx, param, value):
    cleaned = clean_alphanum(value)
    if cleaned in RESERVER_STRINGS:
        raise click.BadParameter(f"'{cleaned}' is a reserved word.")
    if len(cleaned) < 3:
        raise click.BadParameter("Collection name must be at least 3 alphanumeric characters.")
    return cleaned

@click.group()
def cli():
    pass

@click.command("init", help="creates a new spark context in the current directory")
@click.option('--project-name', prompt='Project name', callback=validate_project_name, help='Name of the project')
@click.option('--default-collection', default='general', prompt='Default collection', callback=validate_collection, help='Default collection for sparks')
def create_context(project_name, default_collection):
    try:
        create_dot_spark(project_name, default_collection)
        click.secho("✓ .spark file created successfully in current directory", fg="green")
    except Exception as e:
        click.secho(f"✗ {str(e)}", fg="red")
        raise click.Abort()

cli.add_command(create_context)

if __name__ == "__main__":
    cli()
