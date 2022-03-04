import psycopg2
import csv

# Connect to database
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")
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

with open('data/eating-establishments/eating-establishments-processed.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cur.copy_from(f, 'eating_establishments', sep='|')

with open('data/parks/parks-kml-processed.csv', 'r') as f:
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