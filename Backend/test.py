from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os, math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{os.environ['postgres_pwd']}@localhost/WeekendsDoWhat"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Just to avoid warnings
db = SQLAlchemy(app)


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

print(get_n_closest_parks(31090, 40341, 1))
