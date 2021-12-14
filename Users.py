import sqlite3
import bcrypt

from main import *

class Users:
    def __init__(self):
        self.user_id = None
        self.first_name = None
        self.last_name = None
        self.phone = None
        self.street_address = None
        self.email = None
        self.__password = None
        self.city = None
        self.state = None
        self.date_created = None
        self.active = None


    def set_all(self, first_name, last_name, phone, street_address, email, password, city, state, date_created):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.street_address = street_address
        self.email = email
        self.__password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.city = city
        self.state = state
        self.date_created = date_created


    def change_password(self, new_password, cursor):
        if new_password:
            self.__password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

            update_password = '''
                UPDATE Users
                SET password = ?
                WHERE user_id = ?;
            '''

            cursor.execute(update_password, (self.__password, self.user_id))
            connection.commit()


    def get_password(self):
        return self.__password
    

    def change_email(self, new_email, cursor):
        self.email = new_email

        update_email = '''
            UPDATE Users
            SET email = ?
            WHERE user_id = ?;
        '''

        cursor.execute(update_email, (new_email, self.user_id))
        connection.commit()

    
    def check_password(self, email, new_password, cursor):
        row = cursor.execute("SELECT password FROM Users WHERE email = ?",(email,)).fetchone()
            
        hashed_password = row[0]

        valid_password = bcrypt.hashpw(new_password.encode('utf-8'), hashed_password)
        if valid_password == hashed_password:
            select_sql = '''
                SELECT email FROM Users WHERE password = ? AND email = ?;
            '''

            row = cursor.execute(select_sql, (valid_password, email)).fetchone()

            return (row != None)

    
    def save_user(self, cursor):
        insert_sql = '''
            INSERT INTO Users
                (first_name, last_name, phone, street_address, email, password, city, state, date_created)
            VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''

        cursor.execute(insert_sql, (self.first_name, self.last_name, self.phone, self.street_address, self.email, self.__password, self.city, self.state, self.date_created))
        cursor.connection.commit()

        new_user_id = cursor.execute('SELECT last_insert_rowid()').fetchone()
        self.user_id = new_user_id[0]


    def print_me(self):
        print(f'{self.user_id}: {self.last_name}, {self.first_name}')
        print(f'  Email: {self.email}')
        print(f'  Created: {self.date_created}')
        print(f'  Hashed PW: {self.__password}')


    def load(self, u_id, cursor):
        select_sql = '''
            SELECT user_id, first_name, last_name, phone, street_address, email, city, state, date_created, active
            FROM Users
            WHERE user_id = ?;
        '''

        row = cursor.execute(select_sql, (u_id, )).fetchone()

        if not row:
            return
        self.user_id = row[0]
        self.first_name = row[1]
        self.last_name = row[2]
        self.phone = row[3]
        self.street_address = row[4]
        self.email = row[5]
        self.city = row[6]
        self.state = row[7]
        self.date_created = row[8]


connection = sqlite3.connect('my_users.db')
cursor = connection.cursor()

andrew = Users()
andrew.set_all('Andrew', 'Fletcher', '8088088080', '808 st', 'af@test.com', '123', 'SLC', 'UT', '2020-11-20')
andrew.save_user(cursor)
andrew.print_me()

andrew.load(1, cursor)
andrew.change_password('321', cursor)
andrew.change_email('af@testing.com', cursor)

andrew.print_me()