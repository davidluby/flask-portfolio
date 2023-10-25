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
from crud_obj import Deck, Card, db_tool

app = Flask(__name__)


@app.route('/api/get_data', methods = ['POST'])
def get_data():
    name = request.get_json()
    data = player_data.main(name)

    return {'player_data':data}


@app.route('/api/show_deck', methods = ['GET'])
def show_deck():
    tool = db_tool()
    decks = tool.read_deck()

    return decks


@app.route('/api/intake_deck', methods = ['POST'])
def intake_deck():
    deck = request.get_json()
    tool = db_tool()

    if (deck['id'] == 'null'):
        tool.create_deck(deck)
    else:
        tool.update_deck(deck)
    
    return ''


@ app.route('/api/delete_deck', methods = ['POST'])
def delete_deck():
    deck = request.get_json()
    tool = db_tool()
    tool.delete_deck(deck)

    return ''


if __name__ == '__main__':
    app.run()