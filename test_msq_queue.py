
from msg_queue import Database
import os

FILENAME = "test.sqlite"

def test_db_creation():
    db = Database(FILENAME)
    assert db.db_file == FILENAME

    db.connect()
    assert db.connection != None
    db.drop_database()
    db.close()

def test_message_inserting():
    db = Database(FILENAME)
    db.connect()
    db.insert_message(message="test", is_spam=0)
    messages = db.get_all_messages()
    is_in = 'test' in messages[0]
    assert  is_in == True, "Message should have been stored."
    db.drop_database()
    db.close()

def test_message_updating():
    db = Database(FILENAME)
    db.connect()
    db.insert_message(message="test", is_spam=0)
    db.update_message(message="test", is_spam=1)
    msgs = db.get_all_messages()
    assert msgs[0][2] == 1, "message is_spam should be 1"
    db.drop_database()
    db.close()

def test_message_deleting_by_msg():
    db = Database(FILENAME)
    db.connect()
    db.insert_message(message="test", is_spam=0)
    db.delete_message(message="test")
    msgs = db.get_all_messages()
    assert len(msgs) == 0, "Should delete the only message."
    db.drop_database()
    db.close()

def test_message_deleting_by_id():
    db = Database(FILENAME)
    db.connect()
    db.insert_message(message="test", is_spam=0)
    db.delete_message_by_id(message_id=1)
    msgs = db.get_all_messages()
    assert len(msgs) == 0, "Should delete the only message."
    db.drop_database()
    db.close()

def test_message_getter():
    db = Database(FILENAME)
    db.connect()
    db.insert_message(message="test", is_spam=0)
    msgs = db.get_all_messages()
    assert msgs[0] == (1, "test", 0), "Message should be equal to the inserted."
    db.drop_database()
    db.close()

def test_spam_getter():
    db = Database(FILENAME)
    db.connect()
    db.insert_message(message="test", is_spam=0)
    db.insert_message(message="teast", is_spam=1)
    spam = db.get_spam_messages()
    assert len(spam) == 1, "Should have only one spam message."
    assert spam[0] == (2, "teast", 1), "Spam message should be equal to the inserted."
    db.drop_database()
    db.close()

def test_csv_writing():
    db = Database(FILENAME)
    db.connect()
    db.insert_message(message="alo", is_spam=0)
    db.write_messages_to_csv(filename="test.csv")
    assert os.path.isfile("test.csv"), "Should have written a csv file."
    os.remove("test.csv")
    db.drop_database()
    db.close()

