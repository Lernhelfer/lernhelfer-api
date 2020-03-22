from typing import List
import psycopg2


class DatabaseConnector:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.connection = psycopg2.connect(user=self.user,
                                           password=self.password,
                                           host=self.host,
                                           port=self.port,
                                           dbname=self.database)

    def check_connection(self):
        if self.connection.closed == 1:
            self.connection = psycopg2.connect(user=self.user,
                                               password=self.password,
                                               host=self.host,
                                               port=self.port,
                                               dbname=self.database)

    def receive_from_database(self, query: str) -> List:
        self.check_connection()
        try:
            cur = self.connection.cursor()
            cur.execute(query)
            records = cur.fetchall()
            return records

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            return []

        finally:
            if (self.connection):
                cur.close()
                self.connection.close()
                print("PostgreSQL connection is closed")

    def write_to_database(self, query):
        self.check_connection()
        try:
            cur = self.connection.cursor()
            cur.execute(query)
            self.connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

        finally:
            if (self.connection):
                cur.close()
                self.connection.close()
                print("PostgreSQL connection is closed")
