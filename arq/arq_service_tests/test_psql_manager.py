import unittest

from arq_service.database.psql_manager import PSQLManager


class TestPSQLManager(unittest.TestCase):
    def setUp(self):
        self.psql_manager = PSQLManager()
        self.query = 'SELECT * FROM "Testing"'

    def test_execute(self):
        expected = [(1, 'ConfigTest'), (2, 'DevelopmentTest')]
        result = self.psql_manager.execute(self.query)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
