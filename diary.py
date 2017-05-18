#!/usr/bin/env python3
import sys
from collections import OrderedDict
import datetime
from peewee import *
import os

db = SqliteDatabase('diary.db')

class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    """Create the database and the table if they don't exist"""
    # Connect to database
    db.connect()
    # Create tables
    db.create_tables([Entry], safe=True)


def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            menu[choice]()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def add_entry():
    """Add an entry."""
    print("Enter your entry. Press Ctrl+D when finished.")
    data = sys.stdin.read().strip()

    if data:
        if input("Save entry? [Y/n] ").lower() != 'n':
            Entry.create(content=data)
            print("Saved successfully!")

def search_entries():
    """Search entries for a string."""
    view_entries(input("Search query: "))

def delete_entry(entry):
    """Delete an entry."""
    if input("Are you sure? [yN] ").lower() == 'y':
        entry.delete_instance()

def view_entries(search_query=None):
    """View previous entries"""
    entries = Entry.select().order_by(Entry.timestamp.desc())

    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        print(timestamp)
        print('='*len(timestamp)) # Shortcut to underline something!
        print(entry.content)
        print('\n\n'+'='*len(timestamp))
        print('n) next entry')
        print('d) delete entry')
        print('q) return to main menu')

        next_action = input("Action: [Ndq] ").lower().strip()
        if next_action == 'q':
            break

        elif next_action == 'd':
            delete_entry(entry)
def delete_entry(entry):
    """Delete an entry"""
    pass

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries)
])

if __name__ == '__main__':
    initialize()
    menu_loop()

