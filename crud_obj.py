import pyodbc
from datetime import datetime
import json


class Deck:
    def __init__(self, id, saved, bias):
        self.id = id
        self.saved = saved
        self.bias = bias

class Card(Deck):
    def __init__(self, cardId, deckId, stats):
        self.cardId = cardId
        self.deckId = deckId
        self.stats = stats

class db_tool():

    def connect(self):
        db_conn = pyodbc.connect(
                            "Driver={ODBC Driver 17 for SQL Server};"
                            "Server=website-db.cmtiqqjm470n.us-east-1.rds.amazonaws.com,1433;"
                            "Database=decks_db;"
                            "Trusted_Connection=no;"
                            "UID=davidluby;"
                            "PWD=ASIOB785$^%"
                        )
        return db_conn
    
# This method creates a new deck in the DB
    def create_deck(self, deck):
        conn = self.connect()
        cursor = conn.cursor()


        dateFormat = '%d-%m-%y %H:%M'
        dateTimeNow = datetime.now().strftime(dateFormat)

        cursor.execute(
            'INSERT INTO decks VALUES (?, ?)',
            (dateTimeNow, 'boston'))
        conn.commit()

        id = cursor.execute("""
            SELECT * FROM decks
            WHERE ID = (
                SELECT MAX(id) FROM decks
            )
            """ 
        ).fetchval()


        if id > 20:
            self.reset()
            self.initialize_tables()
            self.create_deck(deck)
        else:
            for card in deck[1::]:
                card['deckId'] = id
                    
                cursor.execute(
                    'INSERT INTO cards VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (card['deckId'], card['name'], card['pic'], card['age'], card['team'],
                    card['pos'], card['min'], card['fg'], card['thr'], card['reb'],
                    card['ast'], card['stl'], card['blk'], card['tov'], card['ppg'])
                    )
                    

        conn.commit()

        return

# This method reads and returns all decks from the DB in JSON format
    def read_deck(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM decks'
        )

        deck_keys = ['id', 'saved', 'bias', 'cards']
        card_keys = ['cardId', "deckId", "name", "pic", "age", "team", "pos", "min",
                    "fg", "thr", "reb", "ast", "stl", "blk", "tov", "ppg"]

        decks = []
        for row in cursor:
            deck = {}
            i = -1
            for key in deck_keys:
                i += 1
                if i < 3:
                    deck[key] = row[i]
                else:
                    deck[key] = []
            decks.append(deck)


        for deck in decks:
            cursor.execute(
                f'SELECT * FROM cards WHERE deckId = {deck["id"]}'
            )
            for row in cursor:
                cards = {}
                i = -1
                for key in card_keys:
                    i += 1
                    cards[key] = row[i]
                deck['cards'].append(cards)

        temp = decks
        decks = {}
        decks['decks'] = temp

        return decks

# This method updates a deck in the DB
    def update_deck(self, deck):
        conn = self.connect()
        cursor = conn.cursor()

        dateFormat = '%d-%m-%y %H:%M'
        dateTimeNow = datetime.now().strftime(dateFormat)

        id = deck[0]['id']

        deck_keys = ['saved', 'bias']

        cursor.execute(
            f'UPDATE decks SET saved = ?, bias = ? WHERE id = ?;',
            (dateTimeNow, 'Boston', id)
        )
        conn.commit()

        card_keys = ['name', 'pic', 'age', 'team', 'pos', 'min',
                    'fg', 'thr', 'reb', 'ast', 'stl', 'blk', 'tov', 'ppg']

        cursor.execute(
            f'SELECT * FROM cards WHERE deckId = {id}'
        )

        indices = []
        for card in cursor:
            indices.append(card[0])

        i = -1
        for card in deck[1::]:
            i += 1
            for key in card_keys:
                cursor.execute(
                    f'UPDATE cards SET {key} = ? WHERE cardId = ?;',
                    (card[key], indices[i])
                )
        conn.commit()
        
        return

# This method deletes a deck from the DB
    def delete_deck(self, deck):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            f'DELETE FROM decks WHERE id = {deck["id"]}'
        )

        cursor.commit()

# This method creates two tables in the DB for decks and cards
    def initialize_tables(self):
        conn = self.connect()
        cursor = conn.cursor()

        decks =  """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='decks' AND xtype='U') 
                CREATE TABLE decks (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    saved VARCHAR(30),
                    bias VARCHAR(30));
                """
        
        cards = """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='cards' AND xtype='U')
                CREATE TABLE cards (
                    cardId INT PRIMARY KEY IDENTITY(1,1),
                    deckId INT FOREIGN KEY(deckId) REFERENCES decks(id) ON DELETE CASCADE,
                    name VARCHAR(50),
                    pic VARCHAR(100),
                    age SMALLINT,
                    team VARCHAR(5),
                    pos VARCHAR(5),
                    min FLOAT, 
                    fg FLOAT,
                    thr FLOAT,
                    reb FLOAT,
                    ast FLOAT, 
                    stl FLOAT,
                    blk FLOAT,
                    tov FLOAT,
                    ppg FLOAT);
                """

        cursor = conn.cursor()
        cursor.execute(decks)
        cursor.execute(cards)
        conn.commit()

        return

# This method can be used to clear the DB
    def display_tables(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
        'SELECT * FROM INFORMATION_SCHEMA.TABLES;'
        )
        

        print("\n----- Tables -----")
        tables = []
        i = -1
        for table in cursor:
            i += 1
            tables.append(table)
            print("\n----- Table "+ str(i) +" -----")
            print(tables[i])

        print("\n--- Table Data ---")
        i = -1
        for table in tables:
            i += 1
            print("\n----- Table "+ str(i) +" -----")
            cursor.execute(f'SELECT * FROM {table[2]}')
            for row in cursor:
                print(f'{row}')
            print()

        return

# This method will write all tables to the console
    def reset(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('DROP TABLE cards')
        cursor.execute('DROP TABLE decks')
        #cursor.execute('DROP DATABASE decks')
        #cursor.execute('CREATE DATABASE decksDB')
        #cursor.execute("TRUNCATE TABLE players")
        #cursor.execute("TRUNCATE TABLE decks")

        conn.commit()

        return
