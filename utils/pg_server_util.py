import psycopg2


class PgServerUtil:

    def __init__(self, host, port, database, username, password):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(host=self.host, port=self.port, dbname=self.database, user=self.username, password=self.password)
            print("Connect to PostgresSQL success")
            return self
        except psycopg2.Error as e:
            print(f"Connect to PostgresSQL Error: {e}")
            return None

    def execute(self, stmt):
        if not self.connection:
            self.connect()
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute(stmt)
            columns = [column[0] for column in self.cursor.description]
            results = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            return results
        except pyodbc.Error as e:
            print(f"PgServerUtil.fetch_all Error: {e}")
            return []
        finally:
            self.cursor.close()
        return self
