import click

@click.group()
def cli():
    pass

@click.command("init", help="creates a new spark context in the current directory")
@click.option('--project-name', prompt='Project name', help='Name of the project')
@click.option('--default-collection', default='general', prompt='Default collection', help='Default collection for sparks')
def create_context(project_name, default_collection, force):
    try:

        click.secho("✓ .spark file created successfully in current directory", fg="green")
    except:
        click.Abort()

cli.add_command(create_context)

if __name__ == "__main__":
    cli()
