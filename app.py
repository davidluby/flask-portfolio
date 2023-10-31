"""
# Author: David Luby
# Date Created: 2/15/2023
#
"""

# Package imports 
from flask import Flask, request

# Import scraper
import player_data

# Import CRUD object
from crud_obj import db_tool

app = Flask(__name__)


# SEARCH FOR CARD
@app.route('/api/get_data', methods = ['POST'])
def get_card():
    name = request.get_json()
    data = player_data.main(name)

    return data

# CREATE NEW DECK
@app.route('/api/create_deck', methods = ['POST'])
def create_deck():
    deck = request.get_json()
    tool = db_tool()
    tool.create_deck(deck)
    
    return ''

# READ STORED DECKS
@app.route('/api/show_deck', methods = ['GET'])
def show_deck():
    tool = db_tool()
    decks = tool.read_deck()

    return decks

# UPDATE DECK IN DB
@app.route('/api/update_deck', methods = ['PUT'])
def update_deck():
    deck = request.get_json()
    tool = db_tool()
    tool.update_deck(deck)
    
    return ''

# DELETE DECK
@ app.route('/api/delete_deck', methods = ['DELETE'])
def delete_deck():
    deck = request.get_json()
    tool = db_tool()
    tool.delete_deck(deck)

    return ''


if __name__ == '__main__':
    app.run()