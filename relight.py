from __future__ import print_function
import os
import sys
import click
import random
import sqlite3

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
NOTES_DIR  = os.path.join(SCRIPT_DIR, 'notes')

QUERY = (
    "SELECT "
    "Bookmark.BookmarkID, "
    "content.Title, "
    "content.Attribution, "
    "Bookmark.Text "
    "FROM Bookmark INNER JOIN content "
    "ON Bookmark.VolumeID = content.ContentID "
    "WHERE Bookmark.Text != 'None';"
)

def print_note():
    note_file = os.path.join(NOTES_DIR, random.choice(os.listdir(NOTES_DIR)))
    with open(note_file, 'r') as f:
        note = f.readlines()

    print(
        'Title : %sAuthor: %s%s' %
          (note[0], note[1], ("".join([str(x) for x in note[2:]]))))

def store_notes(path):
    if not os.path.exists(path):
        print("ERROR: Path does not exist.", file=sys.stderr)
        sys.exit(1)

    sql_connection = sqlite3.connect(path)
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute(QUERY)
    data = sql_cursor.fetchall()
    sql_cursor.close()
    sql_connection.close()

    for note in data:
        note_file = os.path.join(NOTES_DIR, note[0])
        f = open(note_file, 'w')
        f.write("\n".join([str(x) for x in note[1:]]))
        f.close()

@click.command()
@click.option("--store", "-s", default=None, nargs=1,
              help="Path to KoboReader.sqlite file")
def relight(store):
    """
    Store hightlights from Kobo SQLite, and print a random one.
    """
    if(store):
        store_notes(store)
    else:
        print_note()

if __name__ == "__main__":
    relight()
