'''creating and managing database tables'''
import psycopg2

class db_table:
    '''class to initialise tables in db'''
    def __init__(self):
        connection = psycopg2.connect("dbname=test_db")
        cursor = connection.cursor()
        #create users table
        cursor.execute("CREATE TABLE users (id serial PRIMARY KEY, " \
            "username varchar not null unique,password varchar not null )"
                      )
        #create entries db
        cursor.execute("CREATE TABLE entries (id serial PRIMARY KEY, title varchar not null unique"\
            ",content varchar not null )")
        connection.commit()
        connection.close()

class user:
    '''class store users in db and perform various functions'''
    def __init__(self):
        '''inititalize empty user object'''
        self.data = None
        self.username = None
        self.password = None

    def create(self, name, password):
        self.username = name
        self.password = password
        self.save()

    def save(self):
        '''save user after creation or modification'''
        connection = psycopg2.connect("dbname=test_db")
        cursor = connection.cursor()
        #save information to db
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                       (self.username, self.password, )
                      )
        connection.commit()
        connection.close()

    def get_all(self):
        '''function to return all users'''
        connection = psycopg2.connect("dbname=test_db")
        cursor = connection.cursor()
        #save information to db
        cursor.execute("SELECT * FROM Users")
        self.data = cursor.fetchall()
        connection.commit()
        connection.close()
        return self.data
