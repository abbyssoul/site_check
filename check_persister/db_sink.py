import psycopg2


class DbSink:
    """A data sink that persists data in the database table
    """

    DEFAULT_TABLENAME = 'site_status'

    create_table_query = """
        CREATE TABLE IF NOT EXISTS {} (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP NOT NULL, 
        src TEXT NOT NULL,
        target TEXT NOT NULL,
        time TEXT NOT NULL,
        code INTEGER,
        has_match BOOLEAN NULL
        );
        """

    insert_query = """INSERT INTO {} (timestamp, src, target, time, code, has_match) VALUES (
        %(timestamp)s, 
        %(src)s, 
        %(target)s, 
        %(time)s, 
        %(code)s, 
        %(has_match)s
        );
        """

    def __init__(self, table_name=None, db_name=None, db_user=None, db_password=None, db_host=None, db_port=None, connection=None):
        self.connection = connection or psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            sslmode='require'
        )
        self.connection.autocommit = True

        self.table_name = table_name or self.DEFAULT_TABLENAME

        # Create a table in the DB IF one NOT EXISTS
        self._execute(self.create_table_query.format(self.table_name))

    def _execute(self, query, params=None) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)

    def post(self, msg) -> None:
        """Store give site check resuls in a database table

        Args:
            msg: Rest-resource status check result

        """

        # TODO: There is no data completness check done at this stage.
        # Production quality system must handle message versions changes.

        self._execute(self.insert_query.format(self.table_name), msg)
