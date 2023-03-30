"""
# Author: David Luby
# Date Created: 2/15/2023
#
"""

# Package imports
from flask import Flask, request
from flask_restful import reqparse, Api, Resource

# Script imports
import player_data
import db_CRUD as crud

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task')

@app.route('/plain_test')
def plain_test():
    return 'Welcome to my API'

class rest_test(Resource):
    def get(self):
        return 'restful test endpoint'
api.add_resource(rest_test, '/rest_test')


# This endpoint is used to return player data when making decks
class get_player_data(Resource):
    def post(self):
        name = request.get_json()

        data = player_data.main(name)

        return {'player_data':data}
    
api.add_resource(get_player_data, '/api/get_data')


# This endpoint is used to create and update decks
class intake_deck(Resource):
    def post(self):
        deck = request.get_json()
        
        if (deck[0]['id'] == 'null'):
            crud.create_deck(deck)
        else:
            crud.update_deck(deck)

api.add_resource(intake_deck, '/api/intake_deck')


# This endpoint is used to display all of the saved decks
class show_decks(Resource):
    def get(self):
        decks = crud.read_deck()

        return decks
    
api.add_resource(show_decks, '/api/show_deck')


# This endoint is used to delete a saved deck
class delete_deck(Resource):
    def post(self):
        deck = request.get_json()
        crud.delete_deck(deck)

api.add_resource(delete_deck, '/api/delete_deck')


if __name__ == '__main__':
    app.run()