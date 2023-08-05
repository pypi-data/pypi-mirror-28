import os

import psycopg2
import click

import pmigrate

@click.group()
def main():
    pass

@main.command()
@click.option('--folder', default='migrations', prompt='Migrations folder')
@click.option('--digits', default=4)
def init(folder, digits):
    pmigrate.create_new_migration(
        'init',
        migrations_folder=folder,
        digits=digits,
        forward_tmpl=pmigrate.FIRST_FORWARD,
        backward_tmpl=pmigrate.FIRST_BACKWARD,
    )


@main.command()
@click.argument('name')
@click.option('--folder', default='migrations', prompt='Migrations folder')
@click.option('--digits', default=4)
def newmigration(name, folder, digits):
    pmigrate.create_new_migration(
        name,
        migrations_folder=folder,
        digits=digits,
    )

def get_db():
    dburl = os.getenv('DATABASE_URL')
    if not dburl:
        raise click.ClickException('No DATABASE_URL variable in environment')
    return pmigrate.get_migration_cursor(dburl)


@main.command()
@click.option('--to')
@click.option('--folder', default='migrations', prompt='Migrations folder')
@click.option('--digits', default=4)
def migrate(to, folder, digits):
    db = get_db()
    pmigrate.migrate(db, migrations_folder=folder, digits=digits, migrate_to=to)
    # init should ask you for your database url if DATABASE_URL is not set.


@main.command()
def show():
    # query the DB and report on which migrations have been run.
    pass

# migrate
# newmigration
# init
