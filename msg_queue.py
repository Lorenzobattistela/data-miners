import sqlite3
import csv
import logging


class Database:
    def __init__(self, db_file):
        self.connection = None
        self.db_file = db_file

    def connect(self):
        self.connection = sqlite3.connect(self.db_file)
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS message_queue
                          (
                            id integer primary key autoincrement,
                            message TEXT,
                            is_spam INTEGER
                            )''')
        self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()

    def drop_database(self):
        cursor = self.connection.cursor()
        cursor.execute('''DROP TABLE message_queue''')
        self.connection.commit()

    def insert_message(self, message, is_spam):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO message_queue(message, is_spam)
                          VALUES (?, ?)''', (message, is_spam))
        self.connection.commit()

    def update_message(self, message, is_spam):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE message_queue
                          SET is_spam = ?
                          WHERE message = ?''', (is_spam, message))
        self.connection.commit()

    def delete_message(self, message):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM message_queue
                          WHERE message = ?''', (message,))
        self.connection.commit()

    def delete_message_by_id(self, message_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM message_queue
                          WHERE id = ?''', (message_id,))
        self.connection.commit()

    def get_all_messages(self):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM message_queue''')
        rows = cursor.fetchall()
        return rows

    def get_spam_messages(self):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM message_queue
                          WHERE is_spam = 1''')
        rows = cursor.fetchall()
        return rows

    def write_messages_to_csv(self, filename: str = "new_spam.csv"):
        messages = self.get_all_messages()
        try:
            with open(filename, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(['message', 'is_spam'])
                for message in messages:
                    writer.writerow([message[0], message[1]])
        except IOError as e:
            logging.error(f"IOError: {e}")
