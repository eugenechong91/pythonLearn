from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# Main Obj Declaration
class Bot(Base):
    __tablename__ = 'bot'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    avatar = Column(String)

    sources = relationship("BotSource", back_populates="bot")
    intents = relationship("BotIntent", back_populates="bot")
    intros = relationship("BotIntro", back_populates="bot")
    suggestions = relationship("BotSuggestion", back_populates="bot")

    def __repr__(self):
        return"<Bot(id='%s', name='%s', avatar='%s')>" & (self.id, self.name, self.avatar)

    def __init__(self, id, name, avatar):
        self.id = id
        self.name = name
        self.avatar = avatar

class Source(Base):
    __tablename__ = 'bot_source'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    bots = relationship("BotSource", back_populates="source")

    def __repr__(self):
        return"<Bot(id='%s', name='%s')>" & (self.id, self.name)

class Intent(Base):
    __tablename__ = 'bot_intent_action'

    id = Column(Integer, primary_key=True)
    intent = Column(String, nullable=False)
    uri = Column(String, nullable=False)

    bots = relationship("BotIntent", back_populates="intent")

    def __repr__(self):
        return"<Bot(id='%s', intent='%s', uri='%s')>" & (self.id, self.intent, self.uri)

class Intro(Base):
    __tablename__ = 'bot_introduction_message'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)

    bots = relationship("BotIntro", back_populates="intro")

    def __repr__(self):
        return"<Bot(id='%s', text='%s')>" & (self.id, self.text)


class Suggestion(Base):
    __tablename__ = 'bot_suggestion_message'

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)

    bots = relationship("BotSuggestion", back_populates="suggestion")

    def __repr__(self):
        return"<Bot(id='%s', message='%s')>" & (self.id, self.message)


# Everything is a many to many relationship....
class BotSource(Base):
    __tablename__ = 'bot_bot_source'

    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, ForeignKey('bot.id'), primary_key=True)
    bot_source_id = Column(Integer, ForeignKey('bot_source.id'), primary_key=True)

    bot = relationship("Bot", back_populates="sources")
    source = relationship("Source", back_populates="bots")

class BotIntent(Base):
    __tablename__ = 'bot_bot_intent_action'

    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, ForeignKey('bot.id'), primary_key=True)
    bot_intent_id = Column(Integer, ForeignKey('bot_intent_action.id'), primary_key=True)

    bot = relationship("Bot", back_populates="intents")
    intent = relationship("Intent", back_populates="bots")

class BotIntro(Base):
    __tablename__ = 'bot_bot_introduction_message'

    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, ForeignKey('bot.id'), primary_key=True)
    bot_introduction_message_id = Column(Integer, ForeignKey('bot_introduction_message.id'), primary_key=True)
    sort_order = Column(Integer, nullable=False)

    bot = relationship("Bot", back_populates="intros")
    intro = relationship("Intro", back_populates="bots")

class BotSuggestion(Base):
    __tablename__ = 'bot_bot_suggestion_message'

    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, ForeignKey('bot.id'), primary_key=True)
    bot_intent_id = Column(Integer, ForeignKey('bot_suggestion_message.id'), primary_key=True)
    sort_order = Column(Integer, nullable=False)

    bot = relationship("Bot", back_populates="suggestions")
    suggestion = relationship("Suggestion", back_populates="bots")

