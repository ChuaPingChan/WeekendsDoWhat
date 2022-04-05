from flask import Flask, request, jsonify, send_file
import os, math
import datetime

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from flask_bcrypt import Bcrypt

from sqlalchemy import ForeignKey, desc
from sqlalchemy.exc import IntegrityError

# Packages to interact with the PostgreSQL
from flask_sqlalchemy import SQLAlchemy

# Documentation: https://pypi.org/project/bing-image-downloader/
from bing_image_downloader import downloader as img_downloader

from flask_cors import CORS

# TODO: These are just to mock reviews, can be removed later if needed
import random
import names

# Init app
app = Flask(__name__)
CORS(app)

# Connect to database, check out https://www.youtube.com/watch?v=w25ea_I89iM for details
if 'ENV' in os.environ and os.environ['ENV'] == 'heroku':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aoganqgblrifsa:9a12fa516c3d4002d773d7644617d4b6f92b7f4158c687ce3fe9778feffef5a7@ec2-52-207-74-100.compute-1.amazonaws.com:5432/d49oheo6egq1a2'
elif 'ENV' in os.environ and os.environ['ENV'] == 'aws':
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{os.environ['postgres_pwd']}@localhost/WeekendsDoWhat"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Just to avoid warnings
db = SQLAlchemy(app)

# For getting location information from user's input
import geopy
geopy.geocoders.options.default_timeout = 30
geolocator = geopy.geocoders.Nominatim(user_agent="my_request")

# For user handling and authentication
app.config["JWT_SECRET_KEY"] = "super-secret"  # TODO: Change this later
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=3600)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(seconds=3600)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Other global variables
DIR_IMAGE_DATA = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'images')
PLACE_TYPES_SUPPORTED = set(['food', 'park'])

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

class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(), primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    premium = db.Column(db.Boolean, nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        self.premium = False

class Review(db.Model):
    __tablename__ = 'reviews'
    email = db.Column(db.String(), ForeignKey('users.email'), primary_key=True)
    username = db.Column(db.String(), nullable=False)
    place_id = db.Column(db.String(), primary_key=True)
    datetime = db.Column(db.DateTime(), default=datetime.datetime.now)
    rating = db.Column(db.Integer(), nullable=False)
    review = db.Column(db.Text())

    def __init__(self, email, username, place_id, rating, review):
        self.email = email
        self.username = username
        self.place_id = place_id
        self.rating = rating
        self.review = review

def place_type_valid(place_type):
    if place_type in PLACE_TYPES_SUPPORTED:
        return True
    return False

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
    # TODO: Improve recommendation later if needed
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

def get_n_itineraries(x_coord, y_coord, n=4, show_ratings=False):
    # TODO: Polish itineraries JSON format
    itineraries = []

    # TODO: Revise recommendation algo
    # Get the n closest parks, and for each one generate a food->park->food itinerary
    closest_parks = get_n_closest_parks(x_coord, y_coord, n)
    for park in closest_parks:
        closest_eating_establishments = get_closest_eating_establishments(park.latitude, park.longitude, 2)

        # TODO: Show ratings only for premium users
        itineraries.append({
            'activities': [
                {
                    'place_id': closest_eating_establishments[0].inc_crc,
                    'place_type': 'food',
                    'name': closest_eating_establishments[0].name,
                    'address': construct_eating_establishment_address(closest_eating_establishments[0].inc_crc),
                    # TODO: Return rating only if user is a premium user
                    # TODO: Add rating column to places DB and update them for each review
                    'rating': round(random.randrange(30, 51) * 0.1, 1)
                },
                {
                    'place_id': park.inc_crc,
                    'place_type': 'park',
                    'name': park.name,
                    'address': get_park_address(park.inc_crc),
                    'rating': round(random.randrange(30, 51) * 0.1, 1)
                },
                {
                    'place_id': closest_eating_establishments[1].inc_crc,
                    'place_type': 'food',
                    'name': closest_eating_establishments[1].name,
                    'address': construct_eating_establishment_address(closest_eating_establishments[1].inc_crc),
                    'rating': round(random.randrange(30, 51) * 0.1, 1)
                }
            ]
        })
    
    return itineraries

def user_is_premium(user_email):
    query_res = User.query.filter_by(email=user_email).first()
    if query_res:
        return query_res.premium
    return False

#############
# REST APIs #
#############

@app.route('/')
def index():
    return jsonify({ 'msg': 'This is the server of WeekendsDoWhat' })

@app.route("/get_user_info", methods=["GET"])
@jwt_required()
def get_user_info():
    user_email = get_jwt_identity()

    user_matched = User.query.filter_by(email=user_email).first()
    if not user_matched:
        return ('User is not logged in', 401)

    return {
        'email': user_matched.email,
        'username': user_matched.username,
        'is_premium': user_matched.premium
    }

# TODO: Use SSL to secure data in POST request
# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def create_token():
    if 'email' not in request.json or 'password' not in request.json:
        return ('Invalid request', 400)

    email_input = request.json.get('email', None)
    password_input = request.json.get('password', None)

    # TODO: Authentication
    query_res = User.query.filter_by(email=email_input).first()
    if not query_res or not bcrypt.check_password_hash(query_res.password, password_input):
        return ('Bad email or password', 401)

    access_token = create_access_token(identity=query_res.email)
    return {
        "access_token": access_token,
        "is_premium": query_res.premium
    }

# TODO: Use SSL to secure data in POST request
@app.route('/signup', methods=['POST'])
def signup():
    if set(['email', 'username', 'password']) - set(request.json):
        return ('Invalid request', 400)

    email = request.json['email']
    username = request.json['username']
    password = request.json['password']

    user = User(email, username, password)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        return (f'Email address already exists', 409)
    except Exception as e:
        print(type(e))
        return (f'Sign up failed', 400)

    access_token = create_access_token(identity=email)
    return ({
        'access_token': access_token,
        'is_premium': False
    }, 200)

@app.route('/set_premium_user', methods=["GET"])
@jwt_required()
def set_premium_user():
    user_email = get_jwt_identity()

    num_rows_matched = User.query.filter_by(email=user_email).update({"premium": True})
    if not num_rows_matched == 1:
        return ('', 500)

    db.session.commit()
    return ('', 200)

@app.route('/all_districts')
def get_all_districts():
    # TODO: Consider returning the list in decreasing population density
    return jsonify({
        "districts": ['Amber Road', 'Ang Mo Kio', 'Anson', 'Balestier', 'Beach Road', 'Bedok', 'Bishan', 'Braddell', 'Bukit Panjang', 'Bukit Timah', 'Cairnhill', 'Cecil', 'Changi', 'Choa Chu Kang', 'Clementi New Town', 'Clementi Park', 'Dairy Farm', 'Eunos', 'Geylang', 'Golden Mile', 'Harbourfront', 'High Street', 'Hillview', 'Holland Road', 'Hong Leong Garden', 'Hougang', 'Joo Chiat', 'Jurong East', 'Jurong West', 'Katong', 'Kew Drive', 'Kranji', 'Lim Chu Kang', 'Little India', 'Loyang', 'Macpherson', 'Marina East', 'Marina South', 'Middle Road', 'Novena', 'Orchard', 'Pasir Panjang', 'Pasir Ris', "People's Park", 'Punggol', 'Queenstown', 'Raffles Place', 'River Valley', 'Seletar', 'Sembawang', 'Serangoon', 'Serangoon Garden', 'Springleaf', 'Tampines', 'Tanglin', 'Tanjong Pagar', 'Telok Blangah', 'Tengah', 'Thomson', 'Tiong Bahru', 'Toa Payoh', 'Ulu Pandan', 'Upper Bukit Timah', 'Upper East Coast', 'Upper Thomson', 'Watten Estate', 'Woodgrove', 'Yishun']
    })

@app.route('/place_image', methods=['GET'])
def place_image():
    if 'place_id' not in request.args:
        return ('Invalid request format', 400)

    id = request.args['place_id']
    place = Park.query.filter_by(inc_crc=id).first()
    if not place:
        return ('Place not found', 204)

    place_image_path = os.path.join(DIR_IMAGE_DATA, f"{place.name} Singapore", "Image_1.jpg")

    try:
        if not os.path.isfile(place_image_path):
            img_downloader.download(f"{place.name} Singapore", limit=1,  output_dir=f"{DIR_IMAGE_DATA}", adult_filter_off=True, verbose=True, force_replace=False, timeout=5)
    except:
        return ('Place not found', 204)

    if not os.path.isfile(place_image_path):
        return ('Place not found', 204)

    return send_file(place_image_path)

@app.route('/place_info', methods=['GET'])
@jwt_required(optional=True)
def place_info():
    if 'place_id' not in request.args or 'place_type' not in request.args or not place_type_valid(request.args['place_type']):
        return ('Invalid request format', 400)

    place = None
    id = request.args['place_id']
    place_type = request.args['place_type']

    if place_type == 'park':
        # TODO: Reconsider if this check is necessary or not
        place = Park.query.filter_by(inc_crc=id).first()
        if not place:
            return ('Place not found', 204)

        place_address = get_park_address(id)
    elif place_type == 'food':
        # TODO: Reconsider if this check is necessary or not
        place = EatingEstablishment.query.filter_by(inc_crc=id).first()
        if not place:
            return ('Place not found', 204)

        place_address = construct_eating_establishment_address(id)

    ##### Get reviews and ratings

    # Default shown to free users
    reviews = []
    overall_rating = round(random.randrange(30, 51) * 0.1, 1)       # TODO: Use real overall ratings
    total_num_reviews = 0

    # Get reviews only for premium users
    user_email = get_jwt_identity()
    if user_email and user_is_premium(user_email):
        # Need to reset it to 0 to calculate the true overall rating
        overall_rating = 0

        reviews_query_res = Review.query.filter_by(place_id=id).order_by(desc(Review.datetime))
        for review in reviews_query_res:
            reviews.append({
                'username': review.username,
                'rating': review.rating,
                'review': review.review
            })

            # Update overall stats
            total_num_reviews += 1
            overall_rating = (overall_rating * (total_num_reviews - 1) + review.rating) / total_num_reviews

        # Mock some reviews
        # TODO: Remove fake reviews
        hardcoded_review = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
        num_reviews = random.randrange(1, 3)
        for i in range(num_reviews):
            review = dict()
            review['username'] = names.get_full_name()
            review_length = random.randrange(25, 200)
            review['review'] = hardcoded_review[:review_length]
            rand_rating = round(random.randrange(30, 51) * 0.1, 1)
            review['rating'] = rand_rating

            # Update overall stats
            total_num_reviews += 1
            overall_rating = (overall_rating * (total_num_reviews - 1) + review['rating']) / total_num_reviews

            reviews.append(review)

    return {
        'name': place.name,
        'address': place_address,
        'rating': overall_rating,
        'reviews': reviews
    }

@app.route('/get_itineraries', methods=['GET'])
@jwt_required(optional=True)
def get_itineraries():
    if 'location' not in request.args or 'num_itineraries' not in request.args:
        return ('Invalid request format', 400)

    try:
        num_itineraries = int(request.args['num_itineraries'])
    except:
        return ('num_itineraries is not set properly in GET request', 400)

    location = geolocator.geocode(request.args['location'], country_codes='SG')
    if not location:
        return ('Unable to identify location, please try a different input (e.g. street name)', 204)

    print(f"User's address:\n\t{location.address}")
    latitude, longitude = location.latitude, location.longitude

    response = jsonify({
        "itineraries": get_n_itineraries(latitude, longitude, n=num_itineraries, show_ratings=user_is_premium(get_jwt_identity()))
    }
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# TODO: Use SSL to secure data in POST request
@app.route('/add_review', methods=["POST"])
@jwt_required()
def add_review():
    review_length_limit = 1000

    if set(['rating', 'review', 'place_id']) - set(request.json):
        return ('Invalid request format', 400)

    user_email = get_jwt_identity()
    if not user_email:
        return ('Only premium users can add reviews', 403)
    user_query_res = User.query.filter_by(email=user_email).first()
    if not user_query_res:
        return ('Only premium users can add reviews', 403)
    username = user_query_res.username
    if not user_is_premium(user_email):
        return ('Only premium users can add reviews', 403)

    place_id = request.json['place_id']
    rating = int(request.json['rating'])
    if rating < 1 or rating > 5:
        return ('Invalid rating', 400)
    review = request.json['review']
    if len(review) > review_length_limit:
        return (f'Review exceeded {review_length_limit} characters', 400)

    # Validate place_id
    # TODO: Ideally, this should be a constraint in the DB layer
    if not Park.query.filter_by(inc_crc=place_id) and not EatingEstablishment.query.filter_by(inc_crc=place_id):
        return ('Invalid place', 400)

    # Update user's review if present
    query_result = Review.query.filter_by(email=user_email, place_id=place_id).first()
    if query_result:
        query_result.rating = rating
        query_result.review = review
        # PostgreSQL doesn't support ON UPDATE during create table
        query_result.datetime = datetime.datetime.now()
        db.session.commit()
        return ('Review updated successfully', 200)

    try:
        db.session.add(Review(user_email, username, place_id, rating, review))
        db.session.commit()
    except Exception as e:
        return (f'Failed to add review', 400)

    return ('Review submitted successfully', 200)

# Run server
if __name__ == '__main__':
    app.run()
