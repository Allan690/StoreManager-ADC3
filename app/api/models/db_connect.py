import os
import psycopg2
from instance.config import Config


class DatabaseConnection:
    """Creates a database connection"""
    def __init__(self):
        self.db_host = Config.DB_HOST
        self.db_name = Config.DB_NAME
        self.db_user = Config.DB_USER
        self.db_password = Config.DB_PASSWORD
        self.conn = None

    def connection(self):
        try:
            if os.getenv("APP_SETTINGS") == "testing":
                self.conn = psycopg2.connect(database="testing_db",
                                             password=self.db_password,
                                             user=self.db_user,
                                             host=self.db_host
                                             )
            if os.getenv("APP_SETTINGS") == "development":
                self.conn = psycopg2.connect(
                    database=self.db_name,
                    password=self.db_password,
                    user=self.db_user,
                    host=self.db_host
                )

        except Exception as e:
            print(e)
        return self.conn

    def create_db_tables(self):
        commands = [
            """
            CREATE TABLE IF NOT EXISTS users (userId) serial PRIMARY KEY,            
            email varchar(50) not null,
            password varchar(250) not null,
            role varchar(10) not null)
            """,
            """ 
        CREATE TABLE IF NOT EXISTS products (
            userId INTEGER,
            productId SERIAL PRIMARY KEY,
            prodName VARCHAR(150) NOT NULL,
            Description VARCHAR(150),
            Quantity INTEGER,
            Price INTEGER,
            FOREIGN KEY(userId)
            REFERENCES users(userId)
                      )
        """,

            """
                CREATE TABLE IF NOT EXISTS sales (saleId serial PRIMARY KEY,
                userID int REFERENCES users(user) not null,
                productID int REFERENCES products(productId) not null)
            """
        ]
        try:
            cur = self.connection().cursor()
            for command in commands:
                cur.execute(command)
        except Exception as e:
            print(e)
        self.conn.commit()
        self.conn.close()

    def destroy_db_tables(self):
        cur = self.connection().cursor()

        drop_commands = [
            "DROP TABLE IF EXISTS users CASCADE",
            "DROP TABLE IF EXISTS products CASCADE",
            "DROP TABLE IF EXISTS sales CASCADE"
        ]
        for command in drop_commands:
            cur.execute(command)
        self.conn.commit()
        self.conn.close()
