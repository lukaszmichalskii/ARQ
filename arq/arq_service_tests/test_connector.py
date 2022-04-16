import unittest

from arq_service.database.postgresql_connector import PostgreSQLConnector


class TestConnector(unittest.TestCase):
    def test_set_up_connection(self):
        conn, cur = PostgreSQLConnector.set_up_connection()
        if conn is None or cur is None:
            self.fail()


if __name__ == '__main__':
    unittest.main()
