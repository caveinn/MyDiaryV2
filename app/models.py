'''creating and managing database tables'''
import psycopg2
import os

class Db(object):
    '''class to initialise tables in db'''
    def __init__(self, app):
        self.db_name = app.config.get("DB_NAME")
        self.db_host = app.config.get("DB_HOST")
        self.db_password = app.config.get("DB_PASSWORD")
        self.db_user = app.config.get("DB_USER")
        self.conn = None
        if os.getenv("APP_SETTINGS") == "testing" or os.getenv("APP_SETTINGS") == "development":
            self.conn = psycopg2.connect(database=self.db_name)
        else:
            self.conn = psycopg2.connect(
                database=self.db_name,
                password=self.db_password,
                user=self.db_user,
                host=self.db_host
                )
        self.cursor = self.conn.cursor()


    def create_tables(self):
        try:
            #create users table
            self.cursor.execute(
                "CREATE TABLE users (id serial PRIMARY KEY, " \
                "username varchar not null unique,password varchar not null )"
                )
            #create entries db
            self.cursor.execute(
                "CREATE TABLE entries (id serial PRIMARY KEY, title varchar not null unique"\
                ",content varchar not null, user_id integer references users(id))"
                )
        except psycopg2.Error as db_error:
            return db_error.pgerror
        self.conn.commit()
    def get_all_users(self):
        '''function to return all users'''
        #save information to db
        self.cursor.execute("SELECT * FROM users")
        user_data = self.cursor.fetchall()
        user_list = []
        for single_user in user_data:
            user_list.append(
                User(id=single_user[0], username=single_user[1], email=single_user[2],
                password=single_user[3], app=self.app)
                )
        return user_list

    def drop_all(self):
        self.cursor.execute(
            "SELECT table_schema, table_name FROM information_schema.tables WHERE"\
             "table_schema = 'public' ORDER BY table_schema,table_name"
        )
        rows = self.cursor.fetchall()
        for row in rows:
            self.cursor.execute("drop table "+row[1] + " cascade")
        self.conn.commit()


class User(Db):
    '''class store users in db and perform various functions'''
    def __init__(self, app, username, email, password, user_id=None):
        '''inititalize a user object'''
        super(User, self).__init__(app)
        self.username = username
        self.password = password
        self.email = email
        self.user_id = user_id
        user_list = self.get_all_users()
        for user in user_list:
            if user.username == username or user.email == email:
                return {"mesage": "cannot store duplicate email or username"}
        #save information to db
        self.cursor.execute(
            "INSERT INTO users (username, email password) VALUES (%s, %s, %s)",
            (self.username, self.password, )
            )
        self.conn.commit()

    def save(self):
        '''save user after creation or modification'''
        connection = psycopg2.connect(
            database  = "d9uk0uj735e4rp",
            password = '4fc5272295b21a8157ca9c88c95ebcf100f57112247356756dc725974b810a22',
            user  = 'pfpewbzvzcrsnk',
            host  = "ec2-54-204-23-228.compute-1.amazonaws.com",
            )
        
        connection.close()

    def get_all(self):
        '''function to return all users'''
        connection = psycopg2.connect(
            database  = "d9uk0uj735e4rp",
            password = '4fc5272295b21a8157ca9c88c95ebcf100f57112247356756dc725974b810a22',
            user  = 'pfpewbzvzcrsnk',
            host  = "ec2-54-204-23-228.compute-1.amazonaws.com",
            )
        cursor = connection.cursor()
        #save information to db
        cursor.execute("SELECT * FROM users")
        table_data = cursor.fetchall()
        temp = []
        token = None
        for single_user in table_data:
            temp.append({"id":single_user[0], "username":single_user[1], "password":single_user[2]})
        self.data = temp
        connection.commit()
        connection.close()
        return self.data

class entry(object):
    def __init__(self,db_name):
        self.data = None
        self.title = None
        self.content = None
        self.user_id = None
        self.db_name =db_name

    def create(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.save()

    def save(self):
        connection = psycopg2.connect(
            database  = "d9uk0uj735e4rp",
            password = '4fc5272295b21a8157ca9c88c95ebcf100f57112247356756dc725974b810a22',
            user  = 'pfpewbzvzcrsnk',
            host  = "ec2-54-204-23-228.compute-1.amazonaws.com",
            )
        cursor = connection.cursor()
        #save information to db
        cursor.execute("INSERT INTO entries (title, content, user_id ) VALUES (%s, %s, %s)",
                       (self.title, self.content, self.user_id, )
                      )
        connection.commit()
        connection.close()
    
    def update(self,id, title, content):
        connection = psycopg2.connect(
            database  = "d9uk0uj735e4rp",
            password = '4fc5272295b21a8157ca9c88c95ebcf100f57112247356756dc725974b810a22',
            user  = 'pfpewbzvzcrsnk',
            host  = "ec2-54-204-23-228.compute-1.amazonaws.com",
            )
        cursor = connection.cursor()
        #save information to db
        cursor.execute("UPDATE entries SET content = %s , title = %s WHERE id = %s",
                       (content, title, id, )
                      )
        connection.commit()
        connection.close()
        


    def get_all(self):
        '''function to return all users'''
        connection = psycopg2.connect(
            database  = "d9uk0uj735e4rp",
            password = '4fc5272295b21a8157ca9c88c95ebcf100f57112247356756dc725974b810a22',
            user  = 'pfpewbzvzcrsnk',
            host  = "ec2-54-204-23-228.compute-1.amazonaws.com",
            )
        cursor = connection.cursor()
        #save information to db
        cursor.execute("SELECT * FROM entries")
        table_data = cursor.fetchall()
        temp = []
        token = None
        for single_entry in table_data:
            temp.append({"id":single_entry[0], "title":single_entry[1], "content":single_entry[2],
                "user_id":single_entry[3]})
        self.data = temp
        connection.commit()
        connection.close()
        return self.data
