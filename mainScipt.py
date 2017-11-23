
import sqlite3 as MySql
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import exc
import sys

# Create Engine
#engine = create_engine('sqlite:///AndyDB.sqlite', echo=False)
engine = create_engine('sqlite:///'+sys.argv[1], echo=False)

# Create Session to handle DB
Session = sessionmaker()
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Session.configure(bind=engine)
session = Session()

# Initialize Table Structure
from Models import Bot, Suggestion, Intro, Source, Intent, Setting, Base, BotIntro, BotSuggestion
Base.metadata.create_all(engine)

# These are setting defaults [(key,date_type, value),(key,date_type,value)]
settingDefaults = [ ('SEMANTICS_conversation_bot_invalid_compound_message',         'text',     "Oops! Looks like I didn't find anything"),
                    ('CONFIG_conversation_bot_intent_fallback_suggestion_count',    'text',     '3'),
                    ('CONFIG_conversation_bot_intent_fallback',                     'text',     'Default Fallback Intent'),
                    ('CONFIG_conversation_bot_intent_suggestion',                   'text',     'Suggestion'),
                    ('CONFIG_conversation_bot_compound_intent_map',                 'text',     '{  "FEED_session": "session", \
                                                                                                    "FEED_speaker": "speaker", \
                                                                                                    "FEED_artist": "artist", \
                                                                                                    "FEED_exhibitors": "exhibitors", \
                                                                                                    "FEED_location": "location", \
                                                                                                    "FEED_entity": "entity" }'),
                    ('CONFIG_conversation_bot_data_key_map_eventbase',              'text',     '{  "session": "FEED_session", \
                                                                                                    "speaker": "FEED_speaker", \
                                                                                                    "artist": "FEED_artist", \
                                                                                                    "exhibitors": "FEED_exhibitors", \
                                                                                                    "location": "FEED_location", \
                                                                                                    "entity": "FEED_entity" }')]
# These are the bot table defaults
tBotDefault = [('Bot Name', 'bot_avatar_ebhi')]
tSourceDefault = [('eventbase')]
tIntentDefault = [('DL_Favorites', '/favorites'),
                  ('DL_ScheduleView', '/schedule'),
                  ('DL_ProfileView', '/my_profile')]
tIntroDefault = [("Hello I'm a personal assistant."),
                 ("Here are some sample questions you can ask me:")]
tSuggestionDefault = [("What's on my schedule?"),
                      ("Are there any roundtable sessions?"),
                      ("Where are the breakout sessions?")]

SORT_FACTOR = 10

# # STEP 3: Go through the Settings_KV Table First
# If it exist and has a value, ask if user wants to overwrite
# If it exist but is NULL or "", update
# If it does not exist, add.
# TODO: Handle If more than 1 row returned?
for setting in settingDefaults:
    try:
        # Search for one instance
        row = session.query(Setting).filter(Setting.key == setting[0], Setting.value != None).one()

        # If the value is empty, it should be considered as NoResults
        if not row.value:
            raise exc.NoResultFound()
        # else ask user if they want to overwrite
        else:
            print(setting[0] + ' was found with the following value: \n"' + row.value + '"')
            choice = input("Do you want to overwrite with default? [Yes/No]")
            if choice.lower() in {'yes', 'ye', 'y'}:
            # Overwrite it
                record = session.query(Setting).filter(Setting.key == setting[0]).one()
                print('Adding: ' + setting[0] + '\n Reason: Manual overwrite')
                record.value = setting[2]
                record.data_type = setting[1]
    # If more than 1... raise TODO not sure what to do here yet
    except exc.MultipleResultsFound:
        print("ERROR: More than 1 " + setting[0] + " was found!")
    except exc.NoResultFound:
        try:
            # Filter for just the key to encompass the "NULL" values
            record = session.query(Setting).filter(Setting.key == setting[0]).one()

            # If the key exists, but no value assigned, UPDATE
            print('Adding: ' + setting[0] + '\n Reason: No value found')
            record.value = setting[2]
            record.data_type = setting[1]
        # otherwise exception thrown if not found, ie. will just ADD
        except exc.NoResultFound:
            print('Adding: ' + setting[0] + '\n Reason: No key found')
            keyToAdd = Setting(key=setting[0], value=setting[2], data_type=setting[1])
            session.add(keyToAdd)
    # Push and Clear
    session.commit()
    session.flush()



# Step 5: Populate "bot" Tables
# If Nothing, just add all the defaults above
if (session.query(Bot).count() == 0):
    for eachBot in tBotDefault:
        botToAdd = Bot(name=eachBot[0], avatar=eachBot[1])
        botToAdd.sources.append(Source(name=tSourceDefault[tBotDefault.index(eachBot)]))

        for eachIntent in tIntentDefault:
            botToAdd.intents.append(Intent(intent=eachIntent[0],uri=eachIntent[1]))

        for eachIntro in tIntroDefault:
            inter = BotIntro(sort_order=((1+tIntroDefault.index(eachIntro))*SORT_FACTOR))
            inter.intro = Intro(text=eachIntro)
            botToAdd.intros.append(inter)

        for eachSuggestion in tSuggestionDefault:
            inter = BotSuggestion(sort_order=((1+tSuggestionDefault.index(eachSuggestion))*SORT_FACTOR))
            inter.suggestion = Suggestion(message=eachSuggestion)
            botToAdd.suggestions.append(inter)

        session.add(botToAdd)
        session.commit()
        session.flush()
else:
    choice = input("You already have a bot added. Would you like to add another? [Yes/No]")
    if choice.lower() in {'yes', 'ye', 'y'}:
        nameInput = input("Enter the name of the bot:") or tBotDefault[0][0]
        avatarInput = input("Enter the avatar of the bot:") or tBotDefault[0][1]
        botToAdd = Bot(name=nameInput, avatar=avatarInput)

        sourceInput = input("What is the source of the bot?") or tSourceDefault[0]
        botToAdd.sources.append(Source(name=sourceInput))

        # Intent Input, if no, askes if default is desired
        intentChoice = input("Do you want to add your own Intents? [Yes/No]")
        if intentChoice.lower() in {'yes', 'ye', 'y'}:
            continueIntent = True
            while continueIntent:
                intentInput = input("Enter your intent: ex. DL_Favorites") or tIntentDefault[0][0]
                uriInput = input("Enter the uri for this " + intentInput + " intent: ex. /favorites") or tIntentDefault[0][1]
                botToAdd.intents.append(Intent(intent=intentInput, uri=uriInput))
                continueChoice = input("Do you want to add another intent?")
                if continueChoice.lower() in {'no', 'n', ''}:
                    continueIntent = False
        else:
            intentChoice = input("Do you want to use default Intents? [Yes/No]")
            if intentChoice.lower() in {'yes', 'ye', 'y'}:
                for eachIntent in tIntentDefault:
                    botToAdd.intents.append(Intent(intent=eachIntent[0], uri=eachIntent[1]))

        # Intro Input, if no, askes if default is desired
        introChoice = input("Do you want to add your own Introduction Messages? [Yes/No]")
        if introChoice.lower() in {'yes', 'ye', 'y'}:
            continueIntro = True
            index = 0
            while continueIntro:
                index += 1
                introInput = input("In order, enter your Introduction Message: ex. 'Hello I'm a personal assistant.'") or tIntroDefault[0]
                inter = BotIntro(sort_order=(index*SORT_FACTOR))
                inter.intro = Intro(text=introInput)
                botToAdd.intros.append(inter)
                continueChoice = input("Do you want to add another Introduction Message?")
                if continueChoice.lower() in {'no', 'n', ''}:
                    continueIntro = False
        else:
            introChoice = input("Do you want to use default Introduction Messages? [Yes/No]")
            if introChoice.lower() in {'yes', 'ye', 'y'}:
                for eachIntro in tIntroDefault:
                    inter = BotIntro(sort_order=((1 + tIntroDefault.index(eachIntro)) * SORT_FACTOR))
                    inter.intro = Intro(text=eachIntro)
                    botToAdd.intros.append(inter)

        # Suggestion Input, if no, askes if default is desired
        suggestChoice = input("Do you want to add your own Suggestion Messages? [Yes/No]")
        if suggestChoice.lower() in {'yes', 'ye', 'y'}:
            continueSuggest = True
            index = 0
            while continueSuggest:
                index += 1
                introInput = input("In order, enter your Suggestion Message: ex. 'What's on my schedule?'") or tSuggestionDefault[0]
                inter = BotSuggestion(sort_order=(index * SORT_FACTOR))
                inter.suggestion = Suggestion(message=introInput)
                botToAdd.suggestions.append(inter)
                continueChoice = input("Do you want to add another Suggestion Message?")
                if continueChoice.lower() in {'no', 'n', ''}:
                    continueSuggest = False
        else:
            suggestChoice = input("Do you want to use default Suggestion Messages? [Yes/No]")
            if suggestChoice.lower() in {'yes', 'ye', 'y'}:
                for eachSuggestion in tSuggestionDefault:
                    inter = BotSuggestion(sort_order=((1 + tSuggestionDefault.index(eachSuggestion)) * SORT_FACTOR))
                    inter.suggestion = Suggestion(message=eachSuggestion)
                    botToAdd.suggestions.append(inter)

        # After Input Phase is done, add
        session.add(botToAdd)
        session.commit()
        session.flush()
