from flask import Flask, request, jsonify
import os
import math

# Packages to interact with the PostgreSQL
from flask_sqlalchemy import SQLAlchemy

# Init app
app = Flask(__name__)

# Connect to database, check out https://www.youtube.com/watch?v=w25ea_I89iM for details
if app.config['ENV'] == 'development':
    # TODO: Update with true debug database credentials
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{os.environ['postgres_pwd']}@localhost/WeekendsDoWhat"
else:
    if 'ENV' in os.environ and os.environ['ENV'] == 'heroku':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aoganqgblrifsa:9a12fa516c3d4002d773d7644617d4b6f92b7f4158c687ce3fe9778feffef5a7@ec2-52-207-74-100.compute-1.amazonaws.com:5432/d49oheo6egq1a2'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Just to avoid warnings
db = SQLAlchemy(app)

# TODO: Standardize location column names and set more appriate SQL types
class Park(db.Model):
    __tablename__ = 'parks'
    id = db.Column(db.Integer, primary_key=True)
    unnamed = db.Column(db.Text())
    landxaddresspoint = db.Column(db.Text())
    landyaddresspoint = db.Column(db.Text())
    name = db.Column(db.Text())
    description = db.Column(db.Text())
    inc_crc = db.Column(db.Text())
    fmel_upd_d = db.Column(db.Text())
    hyperlink = db.Column(db.Text())

def get_n_closest_parks(x_coord, y_coord, n=10):
    """
    Returns the n closest parks from the given coordinates
    """
    # Crude implementation of finding the parks with the shortest Euclidean distances, we can optimize this later if needed
    park_to_dist = dict()
    for park in Park.query.all():
        park_name = park.name
        park_x_coord = float(park.landxaddresspoint)
        park_y_coord = float(park.landyaddresspoint)

        distance = math.sqrt((x_coord - park_x_coord)**2 + (y_coord - park_y_coord)**2)
        park_to_dist[park_name] = distance

    return [k for k, v in sorted(park_to_dist.items(), key=lambda item: item[1])][:n]

#############
# REST APIs #
#############

@app.route('/')
def index():
    return jsonify({ 'msg': 'Hello World' })

@app.route('/getitinerary', methods=['GET'])
def get_itinerary():
    if 'location' not in request.args:
        return 'Invalid POST request format'

    response = jsonify({
        "itineraries": [
            {
                "activities": [
                {
                    "type": "food",
                    "name": "COLD STORAGE",
                    "address": "301 C, Block 3, TEMASEK BOULEVARD"
                },
                {
                    "type": "park",
                    "name": f'{get_n_closest_parks(31090, 40341, 1)[0]}',
                    "address": "399 Bukit Gombak West Ave 6"
                },
                {
                    "type": "food",
                    "name": "THE SOUP SPOON",
                    "address": "8 MARINA VIEW"
                }
                ]
            },
            {
                "activities": [
                {
                    "type": "food",
                    "name": "TAO SEAFOOD ASIA",
                    "address": "12 MARINA VIEW"
                },
                {
                    "type": "park",
                    "name": "MacRitchie Reservoir Park",
                    "address": "123 Lornie Road"
                },
                {
                    "type": "food",
                    "name": "THE SOUP SPOON",
                    "address": "8 MARINA VIEW"
                }
                ]
            }
            ]
        }
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Run server
if __name__ == '__main__':
    app.run()
