"""
# All statistics taken from and property of Basketball-Reference.com
# Link: https://www.basketball-reference.com/
#
# Author: David Luby
# Date created: 2/10/2023
#
# This script is used for full CRUD operation between a Python-Flask
# API and AWS DB instance
"""

import pyodbc
from datetime import datetime
import json


# This function creates a new deck in the DB
def create_deck(deck):
    conn = connect()
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

    if id > 10:
        reset()
        initialize_tables()

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


# This function reads and returns all decks from the DB in JSON format
def read_deck():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM decks'
    )

    deck_keys = ['id', 'saved', 'bias']

    decks = []
    for row in cursor:
        deck = {}
        i = -1
        for data in row:
            i += 1
            deck[deck_keys[i]] = data
        decks.append(deck)

    card_keys = ['cardId', "deckId", "name", "pic", "age", "team", "pos", "min",
                "fg", "thr", "reb", "ast", "stl", "blk", "tov", "ppg"]
    
    entries = []
    i = -1
    for deck in decks:
        i += 1
        combine = [deck]
        cursor.execute(
            f'SELECT * FROM cards WHERE deckID = {deck["id"]}'
        )
        for row in cursor:
            dict = {}
            j = -1
            for keys in card_keys:
                j += 1
                dict[keys] = row[j]
            combine.append(dict)
        entries.append(combine)

    return json.dumps(entries)


# This function updates a deck in the DB
def update_deck(deck):
    conn = connect()
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


# This function deletes a deck from the DB
def delete_deck(deck):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        f'DELETE FROM decks WHERE id = {deck["id"]}'
    )

    cursor.commit()


# This function creates two tables in the DB for decks and cards
def initialize_tables():
    conn = connect()
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


# This function can be used to clear the DB
def reset():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('DROP TABLE cards')
    cursor.execute('DROP TABLE decks')
    #cursor.execute('DROP DATABASE decks')
    #cursor.execute('CREATE DATABASE decksDB')
    #cursor.execute("TRUNCATE TABLE players")
    #cursor.execute("TRUNCATE TABLE decks")

    conn.commit()

    return


# This function will write all tables to the console
def display_tables():
    conn = connect()
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


# This function establishes a connection to the MSSQL DB
def connect():
    conn = pyodbc.connect(
                            "Driver={ODBC Driver 17 for SQL Server};"
                            "Server=website-db.cmtiqqjm470n.us-east-1.rds.amazonaws.com,1433;"
                            "Database=decks_db;"
                            "Trusted_Connection=no;"
                            "UID=davidluby;"
                            "PWD=ASIOB785$^%"
                        )

    return conn


# Main method
def main():

    #initialize_tables()
    #reset()
    display_tables()
    #read_deck()


if __name__ == '__main__':
    main()