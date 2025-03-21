import pyodbc
from datetime import datetime


class fit_db():
    def init_db(self, exists):

        conn = pyodbc.connect(
                        "Driver={ODBC Driver 17 for SQL Server};"
                        "Server=database-1.cqxosuqkkyqm.us-east-1.rds.amazonaws.com,1433;"
                        "Database=master;"
                        "Trusted_Connection=no;"
                        "UID=admin;"
                        "PWD=OIBSDOisab234."
                    )
        
        if exists == False:
            conn.autocommit = True
            conn.execute('CREATE DATABASE fitness')


        if exists == True:
            conn.autocommit = True
            conn.execute('DROP DATABASE fitness')



    def connect(self):

        conn = pyodbc.connect(
                        "Driver={ODBC Driver 17 for SQL Server};"
                        "Server=flask-api-db.c2cs59ejtfti.us-east-1.rds.amazonaws.com,1433;"
                        "Database=fitness;"
                        "Trusted_Connection=no;"
                        "UID=davidluby;"
                        "PWD=ASIOB785$^%"
                    )
        return conn



    def init_tables(self):
        users = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE  name='users' AND xtype='U')
        CREATE TABLE users(
        user_id INT IDENTITY(1, 1) PRIMARY KEY,
        first_name VARCHAR(20),
        last_name VARCHAR(20),
        username VARCHAR(20),
        password VARCHAR(20),
        email VARCHAR(30),
        birthday VARCHAR(20)
        );
        """

        figures = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='figures' AND xtype='U')
        CREATE TABLE figures(
        figure_id INT PRIMARY KEY IDENTITY(1, 1),
        user_id INT FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        background VARCHAR(20),
        title_on VARCHAR(5),
        y_on VARCHAR(5),
        yy_on VARCHAR(5),
        x_on VARCHAR(5),
        title VARCHAR(100),
        label VARCHAR(50),
        x_min FLOAT,
        x_max FLOAT
        );
        """
        
        datasets = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='datasets' AND xtype='U')
        CREATE TABLE datasets(
        dataset_id INT PRIMARY KEY IDENTITY(1, 1),
        figure_id INT FOREIGN KEY(figure_id) REFERENCES figures(figure_id) ON DELETE CASCADE,
        show_data VARCHAR(5),
        show_ticks VARCHAR(5),
        show_label VARCHAR(5),
        show_tick_labels VARCHAR(5),
        show_ls VARCHAR(5),
        dashed VARCHAR(5),
        label VARCHAR(50),
        data_color VARCHAR(20),
        ls_color VARCHAR(20),
        y_min FLOAT,
        y_max FLOAT
        );
        """

        data = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='figure_data' AND xtype='U')
        CREATE TABLE figure_data(
        data_id INT PRIMARY KEY IDENTITY(1, 1),
        dataset_id INT FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id) ON DELETE CASCADE,
        date VARCHAR(30),
        value FLOAT,
        );
        """

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(users)
        cursor.execute(figures)
        cursor.execute(datasets)
        cursor.execute(data)
        conn.commit()



    def verify_user(self, jwt_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            f'SELECT FROM users WHERE user_id = {jwt_id}'
        )

        return cursor.fetchall()
            


    def verify_username(self, username):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            f'SELECT * FROM users WHERE username = {username}'
        )

        return cursor.fetchall()



    def get_data(self, id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            f'SELECT * FROM users WHERE user_id = {id}'
        )
        return cursor
    





if __name__ == '__main__':
    db = fit_db()
    #db.init_db(False)

    db.init_tables()


