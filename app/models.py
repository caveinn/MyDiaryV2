'''creating and managing database tables'''
import psycopg2

class db_table(object):
    '''class to initialise tables in db'''
    def __init__(self, db_name):
        self.db_name = db_name

    def create_tables(self):
        connection = psycopg2.connect(self.db_name)
        cursor = connection.cursor()
        #create users table
        cursor.execute("CREATE TABLE users (id serial PRIMARY KEY, " \
            "username varchar not null unique,password varchar not null )"
                      )
        #create entries db
        cursor.execute("CREATE TABLE entries (id serial PRIMARY KEY, title varchar not null unique"\
            ",content varchar not null, user_id integer references users(id))")
        connection.commit()
        connection.close()

    def drop_all(self):
        connection = psycopg2.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_schema,table_name")
        rows = cursor.fetchall()
        for row in rows:
            cursor.execute("drop table "+row[1] + " cascade") 
        cursor.close()
        connection.commit()
        connection.close()


class user(object):
    '''class store users in db and perform various functions'''
    def __init__(self, db_name):
        '''inititalize empty user object'''
        self.data = None
        self.username = None
        self.password = None
        self.db_name = db_name

    def create(self, name, password):
        self.username = name
        self.password = password
        self.save()

    def save(self):
        '''save user after creation or modification'''
        connection = psycopg2.connect(self.db_name)
        cursor = connection.cursor()
        #save information to db
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                       (self.username, self.password, )
                      )
        connection.commit()
        connection.close()

    def get_all(self):
        '''function to return all users'''
        connection = psycopg2.connect(self.db_name)
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
        connection = psycopg2.connect(self.db_name)
        cursor = connection.cursor()
        #save information to db
        cursor.execute("INSERT INTO entries (title, content, user_id ) VALUES (%s, %s, %s)",
                       (self.title, self.content, self.user_id, )
                      )
        connection.commit()
        connection.close()
    
    def update(self,id, title, content):
        connection = psycopg2.connect(self.db_name)
        cursor = connection.cursor()
        #save information to db
        cursor.execute("UPDATE entries SET content = %s , title = %s WHERE id = %s",
                       (content, title, id, )
                      )
        connection.commit()
        connection.close()
        


    def get_all(self):
        '''function to return all users'''
        connection = psycopg2.connect(self.db_name)
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
