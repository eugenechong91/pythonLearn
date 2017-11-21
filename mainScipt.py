import sqlite3 as MySql

connection = MySql.connect('AndyDB.sqlite')

c = connection.cursor()

c.execute('''CREATE TABLE myTable
                (col1 text, col2 text, col3 text)''')
c.execute('''INSERT INTO myTable VALUES ('col1val', 'col2val', 'col3val')''')

connection.commit()

connection.close()
