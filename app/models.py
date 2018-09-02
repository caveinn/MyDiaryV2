'''creating and managing database tables'''
import os
from datetime import datetime
import psycopg2
from flask import jsonify
class Db(object):
    '''class to initialise tables in db'''
    def __init__(self):
        self.db_name = os.getenv("DB_NAME")
        self.db_host = os.getenv("DB_HOST")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_user = os.getenv("DB_USER")
        self.conn = None

    def get_connnection(self):
        if os.getenv("APP_SETTINGS") == "testing" or os.getenv("APP_SETTINGS") == "development":
            self.conn = psycopg2.connect(database="test_db")
        else:
            self.conn = psycopg2.connect(
                database=self.db_name,
                password=self.db_password,
                user=self.db_user,
                host=self.db_host
                )
        return self.conn


    def create_tables(self):
        try:
            #create users table
            cursor = self.get_connnection().cursor()
            cursor.execute(
                "CREATE TABLE users (id serial PRIMARY KEY, " \
                "username varchar(30) not null unique, email varchar not null unique, password varchar not null )"
                )
            #create entries db
            cursor.execute(
                "CREATE TABLE entries (id serial PRIMARY KEY, title varchar(100) not null,"\
                "content varchar(400) not null, date_created varchar not null, "\
                "user_id integer references users(id))"
                )
        except psycopg2.Error as db_error:
            pass
        self.conn.commit()
        self.conn.close()

    def get_all_users(self):
        '''function to return all users'''
        #save information to db
        cursor = self.get_connnection().cursor()
        cursor.execute("SELECT * FROM users")
        user_data = cursor.fetchall()
        users_list = []
        user_dict = {}
        for single_user in user_data:
            user_dict["id"]=single_user[0]
            user_dict["username"]=single_user[1] 
            user_dict["email"]=single_user[2]
            user_dict["password"]=single_user[3]
            users_list.append(user_dict)

        self.conn.close()
        return users_list

    def update(self, entry_id, title, content, user_id):
        #update entry in db
        cursor = self.get_connnection().cursor()
        cursor.execute("SELECT * FROM entries WHERE title = %s and user_id = %s",(title, user_id,))
        row = cursor.fetchall()
        if row:
            return jsonify({"message":"the title is already in use"}), 400
        cursor.execute(
            "UPDATE entries SET content = %s , title = %s WHERE id = %s",
            (content, title, entry_id, )
            )
        self.conn.commit()
        cursor.execute("SELECT * FROM entries WHERE id = %s",(entry_id,))
        row = cursor.fetchone()
        entry_dict = {}
        entry_dict["id"] = row[0]
        entry_dict["title"] = row[1]
        entry_dict["content"] = row[2]
        entry_dict["date_created"] = row[3]
        entry_dict["user_id"] = row[4]
        return jsonify(entry_dict), 200
    
    def delete(self, entry_id):
        #delete entry
        cursor = self.get_connnection().cursor()
        cursor.execute(
            "DELETE FROM entries WHERE id = %s",
            (entry_id, )
            )
        self.conn.commit()

    def get_all_entries(self):
        cursor = self.get_connnection().cursor()
        cursor.execute("SELECT * FROM entries")
        entry_data = cursor.fetchall()
        entry_list = []
        
        for single_entry in entry_data:
            entry_dict = {}
            entry_dict["id"] = single_entry[0]
            entry_dict["title"] = single_entry[1]
            entry_dict["content"] = single_entry[2]
            entry_dict["date_created"] = single_entry[3]
            entry_dict["user_id"] = single_entry[4]
            entry_list.append(entry_dict)
        self.conn.close()
        return entry_list

    def drop_all(self):
        cursor=self.get_connnection().cursor()
        cursor.execute(
            "SELECT table_schema,table_name FROM information_schema.tables "\
            " WHERE table_schema = 'public' ORDER BY table_schema,table_name"
        )
        rows = cursor.fetchall()
        for row in rows:
            cursor.execute("drop table "+row[1] + " cascade")
        self.conn.commit()
        self.conn.close()


class User(Db):
    '''class store users in db and perform various functions'''
    def __init__(self, username, email, password):
        '''inititalize a user object'''
        super(User, self).__init__()
        self.username = username
        self.password = password
        self.email = email
        self.id = None
        user_list = self.get_all_users()
        save = True
        for user in user_list:
            if user["username"] == username or user["email"] == email:
                 save = False
       #save information to db
        cursor = self.get_connnection().cursor()
        if save:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (self.username, self.email, self.password, )
                )
        cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
        row = cursor.fetchone()
        self.id = row[0]
        self.conn.commit()
        self.conn.close()

    def get_data(self):
        user_data = {
            "id":self.id,
            "username":self.username,
            "email": self.email
        }

        return user_data



class Entry(Db):
    def __init__(self, title, content, user_id = None  ):
        super(Entry, self).__init__()
        self.title = title
        self.content = content
        self.user_id = user_id
        self.id = None
        self.date_created = datetime.now().strftime("%c")
        entry_list = self.get_all_entries()
        save = True
        for entry in entry_list:
            if entry["title"] == title:
                save = False
       #save information to db
        cursor = self.get_connnection().cursor()
        if save:
            cursor.execute(
                "INSERT INTO entries (title, content, date_created ,user_id) VALUES (%s, %s, %s, %s)",
                (self.title, self.content, self.date_created, self.user_id,)
                )
        cursor.execute("SELECT id FROM entries WHERE title = %s and user_id = %s ", (self.title,self.user_id,))
        row = cursor.fetchone()
        self.id = row[0]
        self.conn.commit()
        self.conn.close()

    def get_data(self):
        entry_data = {
            "id":self.id,
            "title":self.title,
            "content": self.content,
            "date-created":self.date_created,
            "author_id": self.user_id
        }

        return entry_data
    