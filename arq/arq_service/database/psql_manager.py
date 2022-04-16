from arq_service.database.postgresql_connector import PostgreSQLConnector


class PSQLManager:

    def __init__(self):
        self.connection, self.cur = PostgreSQLConnector.set_up_connection()

    def execute(self, query: str):
        if self.cur:
            self.cur.execute(query)
            return self.cur.fetchall()
