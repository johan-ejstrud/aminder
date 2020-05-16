from __future__ import print_function
import os
import sys
import sqlite3

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

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

def main():
    path = sys.argv[1]

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
        note_file = os.path.join(SCRIPT_DIR, 'notes', note[0])
        f = open(note_file, 'w')
        f.write("\n".join([str(x) for x in note[1:]]))
        f.close()

if __name__ == "__main__":
    main()
