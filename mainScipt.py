import sqlite3 as MySql
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


Session = sessionmaker()

# connection = MySql.connect('AndyDB.sqlite')
# c = connection.cursor()

# Create Engine
engine = create_engine('sqlite:///AndyDB.sqlite', echo=True)

# Create handles to DB via Sessions
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Session.configure(bind=engine)
session = Session()

# Initialize Table Structure
from Models import Bot, Suggestion, Intro, Source, Intent, Base
# metadata = Base.metadata.declarative_base(bind=engine)
Base.metadata.create_all(engine)

print(Base.metadata.tables.keys())
print(Base.metadata.reflect(engine))
print('1231231231231231')


# Creating First Instance of Bot ie...a row
myBot = Bot(name='TestName', avatar= 'TestAvi', id=2)
session.add(myBot)
session.commit()



# c.execute('''CREATE TABLE myTable
#                 (col1 text, col2 text, col3 text)''')
# c.execute('''INSERT INTO myTable VALUES ('col1val', 'col2val', 'col3val')''')
#
# connection.commit()
#
# connection.close()
