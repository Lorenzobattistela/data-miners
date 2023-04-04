
import csv
import logging
from collections import namedtuple
from typing import List, NamedTuple


class ContactMessage:
    def __init__(self, name: str, email: str, message: str) -> None:
        self.name = name
        self.email = email
        self.message = message

    def clean(self):
        self.message = self.message.replace("|", "/")
        self.name = self.name.replace("|", "/")
        self.email = self.email.replace("|", "/")

    def save_to_csv(self, filename: str = "contact_messages.csv") -> bool:
        try:
            self.clean()
            new_row = [self.name, self.email, self.message]
            with open(filename, 'a', newline='') as f:
                writer = csv.writer(f, delimiter="|")
                writer.writerow(new_row)
            return True
        except Exception as e:
            logging.error(f"Error while saving contact message to csv: {e}")
            return False


def load_messages(filename: str = "contact_messages.csv") -> List[NamedTuple]:
    Row = namedtuple('Row', "name email message")
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter="|")
            for row in reader:
                rows.append(Row(row[0], row[1], row[2]))
        rows.pop(0)
        return rows
    except Exception as e:
        logging.error(f"Error while loading contact messages from csv: {e}")
        return []
