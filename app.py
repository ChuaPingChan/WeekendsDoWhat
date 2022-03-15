from fileinput import close
import json
from flask import Flask, request, jsonify
import os
import math, random

# Packages to interact with the PostgreSQL
from flask_sqlalchemy import SQLAlchemy

# TODO: This is just to mock reviews, to be remove later
import names

# Init app
app = Flask(__name__)

# Connect to database, check out https://www.youtube.com/watch?v=w25ea_I89iM for details
if 'ENV' in os.environ and os.environ['ENV'] == 'heroku':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aoganqgblrifsa:9a12fa516c3d4002d773d7644617d4b6f92b7f4158c687ce3fe9778feffef5a7@ec2-52-207-74-100.compute-1.amazonaws.com:5432/d49oheo6egq1a2'
elif 'ENV' in os.environ and os.environ['ENV'] == 'aws':
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{os.environ['postgres_pwd']}@localhost/WeekendsDoWhat"

# For getting location information from user's input
import geopy
geopy.geocoders.options.default_timeout = 30
geolocator = geopy.geocoders.Nominatim(user_agent="my_request")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Just to avoid warnings
db = SQLAlchemy(app)

class Park(db.Model):
    __tablename__ = 'parks'
    inc_crc = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    description = db.Column(db.Text())
    hyperlink = db.Column(db.Text())

class EatingEstablishment(db.Model):
    __tablename__ = 'eating_establishments'
    inc_crc = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    lic_name = db.Column(db.String())
    str_name = db.Column(db.String())
    unit_no = db.Column(db.String())
    postcode = db.Column(db.Integer())
    level_no = db.Column(db.String())

def get_closest_eating_establishments(x_coord, y_coord, n=10):
    """
    Returns the n closest eating_establishments from the given coordinates
    """
    # Crude implementation of finding the eating establishments with the shortest Euclidean distances, we can optimize this later if needed
    dist_to_eating_establishment = dict()
    for eating_establishment in EatingEstablishment.query.all():
        eating_establishment_x_coord = float(eating_establishment.latitude)
        eating_establishment_y_coord = float(eating_establishment.longitude)

        distance = math.sqrt((x_coord - eating_establishment_x_coord)**2 + (y_coord - eating_establishment_y_coord)**2)
        dist_to_eating_establishment[distance] = eating_establishment

    return [dist_to_eating_establishment[k] for k in sorted(dist_to_eating_establishment)][:n]

def get_n_closest_parks(x_coord, y_coord, n=10):
    """
    Returns the n closest parks from the given coordinates
    """
    # Crude implementation of finding the parks with the shortest Euclidean distances, we can optimize this later if needed
    dist_to_park = dict()
    for park in Park.query.all():
        park_x_coord = float(park.latitude)
        park_y_coord = float(park.longitude)

        distance = math.sqrt((x_coord - park_x_coord)**2 + (y_coord - park_y_coord)**2)
        dist_to_park[distance] = park

    return [dist_to_park[k] for k in sorted(dist_to_park)][:n]


def construct_eating_establishment_address(id):
    ee_db_model = EatingEstablishment.query.filter_by(inc_crc=id).first()
    return f"{ee_db_model.unit_no} {ee_db_model.str_name}, {ee_db_model.postcode} Singapore"

def get_park_address(id):
    address = 'Unknown'
    park_db_model = Park.query.filter_by(inc_crc=id).first()
    geopy_location = geolocator.geocode(park_db_model.name, country_codes='SG')
    if geopy_location:
        address = geopy_location.address
    return address

def get_n_itineraries(x_coord, y_coord, n=4):
    # TODO: Polish itineraries JSON format
    itineraries = []

    # TODO: Revise recommendation algo
    # Get the n closest parks, and for each one generate a food->park->food itinerary
    closest_parks = get_n_closest_parks(x_coord, y_coord, n)
    for park in closest_parks:
        closest_eating_establishments = get_closest_eating_establishments(park.latitude, park.longitude, 2)

        itineraries.append({
            'activities': [
                {
                    'place_id': closest_eating_establishments[0].inc_crc,
                    'name': closest_eating_establishments[0].name,
                    'address': construct_eating_establishment_address(closest_eating_establishments[0].inc_crc),
                    'rating': round(random.randrange(30, 51) * 0.1, 1)
                },
                {
                    'place_id': park.inc_crc,
                    'name': park.name,
                    'address': get_park_address(park.inc_crc),
                    'rating': round(random.randrange(30, 51) * 0.1, 1)
                },
                {
                    'place_id': closest_eating_establishments[1].inc_crc,
                    'name': closest_eating_establishments[1].name,
                    'address': construct_eating_establishment_address(closest_eating_establishments[1].inc_crc),
                    'rating': round(random.randrange(30, 51) * 0.1, 1)
                }
            ]
        })
    
    return itineraries


#############
# REST APIs #
#############

@app.route('/')
def index():
    return jsonify({ 'msg': 'This is the server of WeekendsDoWhat' })

@app.route('/all_districts')
def get_all_districts():
    # TODO: Consider returning the list in decreasing population density
    return jsonify({
        "districts": ['Amber Road', 'Ang Mo Kio', 'Anson', 'Balestier', 'Beach Road', 'Bedok', 'Bishan', 'Braddell', 'Bukit Panjang', 'Bukit Timah', 'Cairnhill', 'Cecil', 'Changi', 'Choa Chu Kang', 'Clementi New Town', 'Clementi Park', 'Dairy Farm', 'Eunos', 'Geylang', 'Golden Mile', 'Harbourfront', 'High Street', 'Hillview', 'Holland Road', 'Hong Leong Garden', 'Hougang', 'Joo Chiat', 'Jurong East', 'Jurong West', 'Katong', 'Kew Drive', 'Kranji', 'Lim Chu Kang', 'Little India', 'Loyang', 'Macpherson', 'Marina East', 'Marina South', 'Middle Road', 'Novena', 'Orchard', 'Pasir Panjang', 'Pasir Ris', "People's Park", 'Punggol', 'Queenstown', 'Raffles Place', 'River Valley', 'Seletar', 'Sembawang', 'Serangoon', 'Serangoon Garden', 'Springleaf', 'Tampines', 'Tanglin', 'Tanjong Pagar', 'Telok Blangah', 'Tengah', 'Thomson', 'Tiong Bahru', 'Toa Payoh', 'Ulu Pandan', 'Upper Bukit Timah', 'Upper East Coast', 'Upper Thomson', 'Watten Estate', 'Woodgrove', 'Yishun']
    })

@app.route('/place_info', methods=['GET'])
def place_info():
    if 'place_id' not in request.args or 'place_type' not in request.args:
        return ('', 400)

    id = request.args['place_id']
    place_type = request.args['place_type']

    if place_type == 'park':
        # TODO: Reconsider if this check is necessary or not
        place = Park.query.filter_by(inc_crc=id).first()
        if not place:
            return ('', 204)

        place_address = get_park_address(id)
    elif place_type == 'food':
        # TODO: Reconsider if this check is necessary or not
        place = EatingEstablishment.query.filter_by(inc_crc=id).first()
        if not place:
            return ('', 204)

        place_address = construct_eating_establishment_address(id)

    # Get reviews
    reviews = []

    # TODO: Remove fake reviews
    hardcoded_review = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    num_reviews = random.randrange(0, 7)
    for i in range(num_reviews):
        review = dict()
        review['username'] = names.get_full_name()
        review_length = random.randrange(25, 200)
        review['review'] = hardcoded_review[:review_length]

        # reviews.append(json.dumps(review))
        reviews.append(review)

    return {
        'name': place.name,
        'address': place_address,
        # TODO: Remove fake rating
        'rating': round(random.randrange(30, 51) * 0.1, 1),
        'reviews': reviews
    }

@app.route('/get_itineraries', methods=['GET'])
def get_itineraries():
    if 'location' not in request.args:
        return ('', 400)

    location = geolocator.geocode(request.args['location'], country_codes='SG')
    if not location:
        return ('Unable to identify location, please try a different input (e.g. street name)', 204)

    print(f"User's address:\n\t{location.address}")
    latitude, longitude = location.latitude, location.longitude

    response = jsonify({
        "itineraries": get_n_itineraries(latitude, longitude)
    }
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Run server
if __name__ == '__main__':
    app.run()
