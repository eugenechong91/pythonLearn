from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger

Base = declarative_base()


# Main Obj Declaration
class Bot(Base):
    __tablename__ = 'bot'

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String, nullable=False)
    avatar = Column(String)

    sources = relationship("Source", secondary='bot_bot_source', back_populates="bots")
    intents = relationship("Intent", secondary='bot_bot_intent_action', back_populates="bots")
    #intros = relationship("Intro", secondary='bot_bot_introduction_message', back_populates="bots")

    suggestions = relationship("BotSuggestion", backref="bots")
    intros = relationship("BotIntro", backref="bots")

    def __repr__(self):
        return"<Bot(id='%s', name='%s', avatar='%s')>" % (self.id, self.name, self.avatar)
    def __init__(self, name, avatar):
        self.name = name
        self.avatar = avatar

class Source(Base):
    __tablename__ = 'bot_source'

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String, nullable=False)

    bots = relationship("Bot", secondary='bot_bot_source', back_populates="sources")

    def __repr__(self):
        return"<Bot(id='%s', name='%s')>" % (self.id, self.name)
    def __init__(self, name):
        self.name = name

class Intent(Base):
    __tablename__ = 'bot_intent_action'

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    intent = Column(String, nullable=False)
    uri = Column(String, nullable=False)

    bots = relationship("Bot", secondary='bot_bot_intent_action', back_populates="intents")

    def __repr__(self):
        return"<Bot(id='%s', intent='%s', uri='%s')>" % (self.id, self.intent, self.uri)
    def __init__(self, intent, uri):
        self.intent = intent
        self.uri = uri

class Intro(Base):
    __tablename__ = 'bot_introduction_message'

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)

    #bots = relationship("Bot", secondary='bot_bot_introduction_message', back_populates="intros")

    def __repr__(self):
        return"<Bot(id='%s', text='%s')>" % (self.id, self.text)
    def __init__(self, text):
        self.text = text


class Suggestion(Base):
    __tablename__ = 'bot_suggestion_message'

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    message = Column(String, nullable=False)

    #bots = relationship("Bot", secondary='bot_bot_suggestion_message', back_populates="suggestions")

    def __repr__(self):
        return"<Bot(id='%s', message='%s')>" % (self.id, self.message)
    def __init__(self, message):
        self.message = message


class Setting(Base):
    __tablename__ = 'settings_kv'

    key = Column(String, primary_key=True, nullable=False)
    value = Column(String)
    data_type = Column(String)

    def __repr__(self):
        return "<Setting(key='%s', value='%s', data_type='%s')>" % (self.key, self.value, self.data_type)

# Everything is a many to many relationship....
class BotSource(Base):
    __tablename__ = 'bot_bot_source'

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    bot_id = Column(Integer, ForeignKey('bot.id'))
    bot_source_id = Column(Integer, ForeignKey('bot_source.id'))

    # bot = relationship("Bot", back_populates="sources")
    # source = relationship("Source", back_populates="bots")

class BotIntent(Base):
    __tablename__ = 'bot_bot_intent_action'

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    bot_id = Column(Integer, ForeignKey('bot.id'))
    bot_intent_id = Column(Integer, ForeignKey('bot_intent_action.id'))

    # bot = relationship("Bot", back_populates="intents")
    # intent = relationship("Intent", back_populates="bots")

# Associate OBJ since extra field
class BotIntro(Base):
    __tablename__ = 'bot_bot_introduction_message'

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    bot_id = Column(Integer, ForeignKey('bot.id'))
    bot_introduction_message_id = Column(Integer, ForeignKey('bot_introduction_message.id'))
    sort_order = Column(Integer, nullable=False, autoincrement=True)

    # bot = relationship("Bot", backref="intros")
    intro = relationship("Intro", backref="bot")

# botIntroLinker = Table('bot_bot_introduction_message', Base.metadata,
#                        Column('bot_id', Integer, ForeignKey('bot.id'), primary_key=True),
#                        Column('bot_introduction_message_id', Integer, ForeignKey('bot_introduction_message.id'), primary_key=True),
#                        Column('id', BigInteger().with_variant(Integer, "sqlite"), nullable=True),
#
#                        Column('sort_order', Integer, nullable=True ))

# Associate OBJ since extra field
class BotSuggestion(Base):
    __tablename__ = 'bot_bot_suggestion_message'

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    bot_id = Column(Integer, ForeignKey('bot.id'))
    bot_intent_id = Column(Integer, ForeignKey('bot_suggestion_message.id'))
    sort_order = Column(Integer, nullable=False, autoincrement=True)

    # bot = relationship("Bot", back_populates="suggestions")
    suggestion = relationship("Suggestion", backref="bot")

