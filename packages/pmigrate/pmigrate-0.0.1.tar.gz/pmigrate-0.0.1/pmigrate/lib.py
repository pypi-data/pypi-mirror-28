import itertools
import logging
import os
import sys
from urllib.parse import urlsplit

import psycopg2

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

FIRST_FORWARD = """
BEGIN;
CREATE TABLE migration_history (
	name TEXT NOT NULL,
	time TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	who TEXT DEFAULT CURRENT_USER NOT NULL,
	PRIMARY KEY (name)
);

INSERT INTO migration_history(name) VALUES ('{name}');
COMMIT;"""

# TODO: first remove the initial migration row, then assert that the row count is 0, then and only
# then drop the migration history table.
FIRST_BACKWARD = """BEGIN;
DROP TABLE migration_history;
COMMIT;"""

FORWARD_TMPL = """BEGIN;
SELECT 1 / 0; -- Delete this line and replace with your own migration code.
INSERT INTO migration_history(name) VALUES ('{name}');
COMMIT;"""

BACKWARD_TMPL = """BEGIN;
SELECT 1 / 0; -- Delete this line and replace with your own migration code.
DELETE FROM migration_history WHERE name='{name}';
COMMIT;"""


def get_migration_number(migrations_folder, digits):
    try:
        migrations = sorted([
            m for m in os.listdir(migrations_folder)
            if os.path.isdir(os.path.join(migrations_folder, m))
            and m[:digits].isnumeric()
        ])
        return int(migrations[-1][:digits])
    except FileNotFoundError:
        return 0


def create_new_migration(name, migrations_folder, digits=4, forward_tmpl=FORWARD_TMPL,
                         backward_tmpl=BACKWARD_TMPL):
    next_number = get_migration_number(migrations_folder, digits) + 1
    migration_name = '{num}-{name}'.format(
        num=str(next_number).zfill(digits),
        name=name
    )
    path = os.path.join(migrations_folder, migration_name)
    os.makedirs(path)
    forward = os.path.join(path, 'forward.sql')
    backward = os.path.join(path, 'backward.sql')
    with open(forward, 'w') as f:
        f.write(forward_tmpl.format(name=migration_name))
    with open(backward, 'w') as f:
        f.write(backward_tmpl.format(name=migration_name))
    return forward, backward


def parse_pgurl(db_url):
    """
    Given a SQLAlchemy-compatible Postgres url, return a dict with
    keys for user, password, host, port, and database.
    """

    parsed = urlsplit(db_url)
    return {
        'user': parsed.username,
        'password': parsed.password,
        'database': parsed.path.lstrip('/'),
        'host': parsed.hostname,
        'port': parsed.port,
    }


def get_migration_cursor(dburl):
    conn = psycopg2.connect(**parse_pgurl(dburl))
    conn.autocommit = True
    return conn.cursor()

def migrate(db, migrations_folder, digits, migrate_to=None):
    migration_names = sorted([
        i for i in os.listdir(migrations_folder)
        if os.path.isdir(os.path.join(migrations_folder, i))
        and i[:digits].isnumeric()
    ])

    migrate_to = migrate_to or migration_names[-1]

    try:
        db.execute('SELECT name FROM migration_history ORDER BY name;')
        completed_migrations = [m[0] for m in db]
    except psycopg2.ProgrammingError:
        # The first migration creates the migration_history table.  So the query
        # on that table will fail if we have never run migrations.
        completed_migrations = []

    logging.info('Migrating to ' + migrate_to)
    #to_run = sorted(list(set(migration_names).difference(completed_migrations)))
    #logging.info('Migrations to run: ' + ', '.join(to_run))

    to_run = []
    if migrate_to not in migration_names:
        raise Exception('Could not find migration ' + migrate_to)
    elif migrate_to in completed_migrations:
        # Raise error if we're already past that migration, but let it slide
        # if it's the last one
        if migrate_to != completed_migrations[-1]:
            raise Exception("Cannot migrate to %s, because we're already at %s." % (
                           migrate_to, completed_migrations[-1]))
    else:
        for migration, completed_migration in itertools.zip_longest(migration_names, completed_migrations):
            if migration == completed_migration:
                # already run.  skip!
                continue
            elif completed_migration:
                # Somehow the completed migrations recorded in the DB don't match what we have in the
                # filesystem.  Error!
                raise Exception(
                    'Found completed migration {c} but expected {m}.  Aborting!'.format(
                        c=completed_migration,
                        m=migration
                    ))
            if completed_migration is None:
                # it's in the filesystem but not yet run.  Add it to the list
                to_run.append(migration)

            if migration == migrate_to:
                # stop when we get as far as we're supposed to be going.
                break


    if not len(to_run):
        logging.info('No migrations need running.')
        return
    logging.info('Migrations to run: ' + ', '.join(to_run))

    for m in to_run:
        logging.info('Running %s.' % m)
        script = os.path.join(migrations_folder, m, 'forward.sql')
        with open(script) as f:
            sql = f.read()
        try:
            db.execute(sql)
        except:
            logging.error('Error while running ' + script)
            raise
