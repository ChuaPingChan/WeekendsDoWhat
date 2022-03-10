import psycopg2
import csv
import os

# Connect to database
conn = None
if 'ENV' in os.environ and os.environ['ENV'] == 'heroku':
    conn = psycopg2.connect(r"host=ec2-52-207-74-100.compute-1.amazonaws.com port=5432 dbname=d49oheo6egq1a2 user=aoganqgblrifsa password=9a12fa516c3d4002d773d7644617d4b6f92b7f4158c687ce3fe9778feffef5a7")
else:
    conn = psycopg2.connect(f"host=localhost port=5432 dbname=WeekendsDoWhat user=postgres password={os.environ['postgres_pwd']}")
# Creating a cursor object using the cursor()
cur = conn.cursor()

# Create tables 
cur.execute("""
    CREATE TABLE IF NOT EXISTS eating_establishments(
    id integer PRIMARY KEY,
    unnamed text,
    lic_name text,
    blk_house text,
    str_name text,
    unit_no text,
    postcode text,
    lic_no text,
    business_name text,
    level_no text,
    lic_iss_date text,
    lic_exp_date text,
    inc_crc text,
    fmel_upd_d text
)
""")

cur.execute("""
    DELETE FROM eating_establishments
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS parks(
    id integer PRIMARY KEY,
    unnamed text,
    landxaddresspoint text,
    landyaddresspoint text,
    name text,
    description text,
    inc_crc text,
    fmel_upd_d text,
    hyperlink text
)
""")

cur.execute("""
    DELETE FROM parks
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
