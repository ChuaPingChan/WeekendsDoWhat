from flask import Flask, request, jsonify
import os

# Packages to interact with the PostgreSQL
from flask_sqlalchemy import SQLAlchemy

# Init app
app = Flask(__name__)

# Connect to database, check out https://www.youtube.com/watch?v=w25ea_I89iM for details
if app.debug:
    # TODO: Update with true debug database credentials
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/WeekendsDoWhat'
else:
    pass    # TODO: Connect to production database
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Just to avoid warnings
# db = SQLAlchemy(app)

@app.route('/')
def index():
    return jsonify({ 'msg': 'Hello World' })

@app.route('/getitinerary', methods=['POST'])
def get_itinerary():
    location = request.json['location']

    return jsonify({
        'itinerary 1': {
            'activity 1': {
                'name': 'COLD STORAGE SINGAPORE (1983) PTE LTD',
                'postcode': '38983'
            },
            'activity 2': {
                'name': 'Singpaore Botanic Gardens',
                'postcode': '259569'
            }
        }
    })

# Run server
if __name__ == '__main__':
    app.debug = True
    app.run()
