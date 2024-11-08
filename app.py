"""
# Author: David Luby
# Date Created: 2/15/2023
#
"""

# Package imports 
from flask import Flask, jsonify, session, request, redirect, url_for, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
import bcrypt

# Import scraper
import player_data

# Import CRUD object
from crud_obj import db_tool

# Import fitness DB
from fitness import fit_db

# Import User class
from user import User



# Initialize flask app
app = Flask(__name__)

# Backend Routes
@app.route('/')
def landing():
    return render_template('home.html')

@app.route('/resume.html')
def resume():
    return render_template('resume.html')

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
@app.route('/api/delete_deck', methods = ['DELETE'])
def delete_deck():
    deck = request.get_json()
    tool = db_tool()
    tool.delete_deck(deck)

    return ''


"""
# Fitness App Configuration
app.config['SECRET_KEY'] = 'the_secret_key'
app.config['JWT_SECRET_KEY'] = 'the_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']

# DB initialization
fit_db = fit_db()

#JWT Initialization
jwt = JWTManager(app)


@app.route('/get_name', methods=['GET'])
@jwt_required()
def get_name():
    # Extract user ID from JWT
    jwt_id = get_jwt_identity()
    user = User.verify_user(jwt_id)

    if user:
        return jsonify({'message': 'User found', 'name': user})
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    print('Received data:', username, password)


    user = User.verify_username(username)

    print(user)
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.user_id)
    else:
        return jsonify({'message': 'Login Failed'}), 401

"""


if __name__ == '__main__':
    app.run()