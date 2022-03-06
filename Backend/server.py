from flask import Flask, request, jsonify
import os
import math

# Packages to interact with the PostgreSQL
from flask_sqlalchemy import SQLAlchemy

# Init app
app = Flask(__name__)

# Connect to database, check out https://www.youtube.com/watch?v=w25ea_I89iM for details
if os.environ['ENV'] == 'dev':
    app.debug = True    # Useful for development

    # TODO: Update with true debug database credentials
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{os.environ['postgres_pwd']}@localhost/WeekendsDoWhat"
else:
    pass    # TODO: Connect to production database
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

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

@app.route('/getitinerary', methods=['POST'])
def get_itinerary():
    x_coord = float(request.json['x_coord'])
    y_coord = float(request.json['y_coord'])

    return jsonify({
        'itinerary 1': {
            'activity 1': {
                'name': 'COLD STORAGE SINGAPORE (1983) PTE LTD'
            },
            'activity 2': {
                'name': f'{get_n_closest_parks(x_coord, y_coord, 1)[0]}'
            }
        }
    })

# Run server
if __name__ == '__main__':
    app.run()
