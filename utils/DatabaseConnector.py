import mysql.connector


class DatabaseConnector:
    def __init__(self, host, user, passw):
        self.database_host = host
        self.database_username = user
        self.database_password = passw
        self.connection = None
        self.laststatement = None

    def connect(self):
        try:
            cnx = mysql.connector.connect(user=self.database_username, password=self.database_password,
                                          host=self.database_host,
                                          database='Cinema', autocommit=True)
            self.connection = cnx
        except:
            return False

    def close(self):
        self.connection.close()

    def getstatement(self):
        return self.laststatement

    def getuser(self):
        if self.connection is not None:
            return self.connection.user
        else:
            return 'No active connection'

    def query(self, query):
        if self.connection is not None:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.laststatement = cursor.statement
            if cursor.with_rows:
                return cursor.fetchall()
            cursor.close()
        else:
            return False
