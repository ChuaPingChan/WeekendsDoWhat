import psycopg2
import csv
import os

# Connect to database
conn = None
if 'ENV' in os.environ and os.environ['ENV'] == 'heroku':
    conn = psycopg2.connect(r"host=ec2-52-207-74-100.compute-1.amazonaws.com port=5432 dbname=d49oheo6egq1a2 user=aoganqgblrifsa password=9a12fa516c3d4002d773d7644617d4b6f92b7f4158c687ce3fe9778feffef5a7")
elif 'ENV' in os.environ and os.environ['ENV'] == 'aws':
    conn = psycopg2.connect(r"")
else:
    conn = psycopg2.connect(f"host=localhost port=5432 dbname=WeekendsDoWhat user=postgres password={os.environ['postgres_pwd']}")
# Creating a cursor object using the cursor()
cur = conn.cursor()

# Drop tables
cur.execute("""
    DROP TABLE IF EXISTS eating_establishments;
""")

cur.execute("""
    DROP TABLE IF EXISTS parks;
""")

cur.execute("""
    DROP TABLE IF EXISTS reviews;
""")

cur.execute("""
    DROP TABLE IF EXISTS users;
""")

# Create tables 
cur.execute("""
    CREATE TABLE IF NOT EXISTS eating_establishments(
        inc_crc VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255),
        latitude double precision,
        longitude double precision,
        lic_name VARCHAR(255),
        str_name VARCHAR(255),
        unit_no VARCHAR(255),
        postcode integer,
        level_no VARCHAR(255)
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS parks(
        inc_crc VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255),
        latitude double precision,
        longitude double precision,
        description text,
        hyperlink text
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        email VARCHAR(255) PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(80) NOT NULL,
        premium BOOLEAN NOT NULL
    )
""")

# TODO: Rethink the design to enforce FK constraints of place IDs
cur.execute("""
    CREATE TABLE IF NOT EXISTS reviews(
        email VARCHAR(255),
        username VARCHAR(255) NOT NULL,
        place_id VARCHAR(255),
        datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        rating INTEGER,
        review text,
        FOREIGN KEY (email) REFERENCES users(email),
        PRIMARY KEY (email, place_id)
    )
""")

if 'ENV' in os.environ and os.environ['ENV'] == 'heroku':
    with open(f'{os.path.dirname(os.path.abspath(os.path.dirname(__file__)))}/data/eating-establishments/eating-establishments-processed-heroku.csv', 'r') as f:
        # Notice that we don't need the `csv` module.
        next(f) # Skip the header row.
        cur.copy_from(f, 'eating_establishments', sep='|')

    with open(f'{os.path.dirname(os.path.abspath(os.path.dirname(__file__)))}/data/parks/parks-kml-processed-heroku.csv', 'r') as f:
        # Notice that we don't need the `csv` module.
        next(f) # Skip the header row.
        cur.copy_from(f, 'parks', sep='|')
else:
    with open(f'{os.path.dirname(os.path.abspath(os.path.dirname(__file__)))}/data/eating-establishments/eating-establishments-processed.csv', 'r') as f:
        # Notice that we don't need the `csv` module.
        next(f) # Skip the header row.
        cur.copy_from(f, 'eating_establishments', sep='|')

    with open(f'{os.path.dirname(os.path.abspath(os.path.dirname(__file__)))}/data/parks/parks-kml-processed.csv', 'r') as f:
        # Notice that we don't need the `csv` module.
        next(f) # Skip the header row.
        cur.copy_from(f, 'parks', sep='|')

cur.execute("""
    SELECT COUNT(*) FROM eating_establishments
""")
total_count_eating = cur.fetchall()

cur.execute("""
    SELECT COUNT(*) FROM parks
""")
total_parks = cur.fetchall()

# Commit your changes in the database
conn.commit()

# Closing the connection
conn.close()

print("Eating establishments:", total_count_eating[0][0])
print("Parks:", total_parks[0][0])
