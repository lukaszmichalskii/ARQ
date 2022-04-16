import os

import psycopg2


class PostgreSQLConnector:

    @staticmethod
    def set_up_connection():
        connection = None
        cur = None
        try:
            connection = psycopg2.connect(
                database=os.getenv('POSTGRES_DB'), user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'), host=os.getenv("HOST"))
            cur = connection.cursor()
            if connection is None or cur is None:
                raise Exception
        except Exception as e:
            print('Database establish connection process failed:\n{}'.format(e))

        return connection, cur
