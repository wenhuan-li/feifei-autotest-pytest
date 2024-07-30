import pyodbc


class SQLServerUtil:

    def __init__(self, server, database, username, password):
        self.conn = pyodbc.connect(
            f"DRIVER={'SQL Server'};SERVER={server};DATABASE={database};UID={username};PWD={password}")
        self.cursor = self.conn.cursor()

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()

    def get_row_dict(self, stmt):
        try:
            self.cursor.execute(stmt)
            row = self.cursor.fetchone()
            if row:
                rowdict = {}
                columns = [column[0].upper() for column in self.cursor.description]
                row = [column.strip() if isinstance(column, str) else column for column in row]
                for i, column in enumerate(columns):
                    rowdict[column] = row[i]
                return rowdict
            else:
                return None
        except Exception as e:
            raise LookupError(f"No data found! Error: {e}")
        # finally:
        #     self.close()

    def get_rows_dict(self, stmt):
        try:
            self.cursor.execute(stmt)
            rows = self.cursor.fetchall()
            rows_dict = []
            for row in rows:
                _dict = {}
                columns = [column[0].upper() for column in self.cursor.description]
                row = [column.strip() if isinstance(column, str) else column for column in row]
                for i, column in enumerate(columns):
                    _dict[column] = row[i]
                rows_dict.append(_dict)
            return rows_dict
        except Exception as e:
            raise LookupError(f"No data found! Error: {e}")
        # finally:
        #     self.close()
