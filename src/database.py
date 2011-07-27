'''
@author: dibyendu das

The database module for storing, accessing, 
deleting favourite words
'''

class DataBase:
    '''
    creates a database object & manages
    the operations on the same
    '''

    def __init__(self):
        'creates the words database'

        import sqlite3 as sqlite
        from path import HOME_PATH
        self.__connection = sqlite.connect(HOME_PATH + '/.plexicon/words.db')
        self.__connection.text_factory = str
        self.__cursor = self.__connection.cursor()

    def __create(self, table):
        'creates tables'

        query = "CREATE TABLE IF NOT EXISTS %s(word TEXT UNIQUE, \
english TEXT DEFAULT NULL, bengali TEXT DEFAULT NULL)" % (table)
        self.__cursor.execute(query)

    def __insert(self, table, values):
        'inserts words information into a table'

        query = "INSERT INTO %s(word) VALUES(?)" % (table)
        self.__cursor.execute(query, (values,))

    def __drop(self, table):
        'drops an empty table from the database'

        query = "DROP TABLE %s" % (table)
        self.__cursor.execute(query)

    def update(self, table, values):
        'updates a table (creates, inserts, deletes or drops on requirement)'

        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        self.__cursor.execute(query, (table,))
        row = self.__cursor.fetchone()
        if not row:
            self.__create(table)

        query = 'SELECT word FROM %s WHERE word=?' % (table)
        self.__cursor.execute(query, (values[0],))
        row = self.__cursor.fetchone()
        if not row:
            self.__insert(table, values[0])

        if values[2] == 'english':
            query = "UPDATE %s SET %s=? WHERE word=?" % (table, 'english')
        else:
            query = "UPDATE %s SET %s=? WHERE word=?" % (table, 'bengali')
        self.__cursor.execute(query, (values[1], values[0]))
        query = 'SELECT english, bengali FROM %s WHERE word=?' % table
        self.__cursor.execute(query, (values[0],))
        row = self.__cursor.fetchone()
        if not row[0] and not row[1]:
            query = 'DELETE FROM %s WHERE word=?' % table
            self.__cursor.execute(query, (values[0],))
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        self.__cursor.execute(query, (table,))
        row = self.__cursor.fetchone()
        if not row:
            self.__drop(table)
        self.__connection.commit()

    def row_count(self, table):
        'returns the number of rows from a table'

        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        self.__cursor.execute(query, (table,))
        row = self.__cursor.fetchone()
        if not row:
            return 0
        query = 'SELECT COUNT(*) FROM %s' % (table)
        self.__cursor.execute(query)
        return self.__cursor.fetchone()[0]

    def select(self, table):
        'select all words from a table'

        query = 'SELECT word FROM %s ORDER BY word' % (table)
        self.__cursor.execute(query)
        return self.__cursor.fetchall()

    def select_row(self, table, word):
        'select a row from a table'

        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        self.__cursor.execute(query, (table,))
        row = self.__cursor.fetchone()
        if row:
            query = 'SELECT * FROM %s WHERE word=?' % (table)
            self.__cursor.execute(query, (word,))
            return self.__cursor.fetchone()
        return row

    def close(self):
        'closes the existing session'

        self.__cursor.close()