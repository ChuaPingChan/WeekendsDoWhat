"""
Converts a KML file to CSV
"""

from bs4 import BeautifulSoup
import os, sys, re
import pandas as pd

def main():
    kml_file_paths = [
        f'{os.path.dirname(os.path.abspath(os.path.dirname(__file__)))}/data/eating-establishments/eating-establishments.kml',
        f'{os.path.dirname(os.path.abspath(os.path.dirname(__file__)))}/data/parks/parks-kml.kml'
    ]
    for kml_file_path in kml_file_paths:
        file_basename, file_extension = os.path.splitext(kml_file_path)
        with open(kml_file_path, 'r', encoding='utf-8') as f:
            print(f"Converting {kml_file_path} to CSV...")
            soup = BeautifulSoup(f, 'xml')

            data = []
            for entry in soup.find_all('SchemaData'):
                entry_dict = dict()
                for attr in entry.find_all('SimpleData'):
                    entry_dict[attr['name']] = replace_newline_chars(attr.text)
                data.append(entry_dict)

            df = pd.DataFrame(data)

            # Get latitude and longitude from KML
            latitudes = []
            longitudes = []
            for coords_str in soup.find_all('coordinates'):
                (long, lat, vert) = coords_str.text.split(',')
                latitudes.append(lat)
                longitudes.append(long)

            assert len(latitudes) == df.shape[0]
            assert len(longitudes) == df.shape[0]
            df['LATITUDE'] = latitudes
            df['LONGITUDE'] = longitudes

            # Delimit using '|' as some addresses contains commas
            df.to_csv(f'{file_basename}.csv', sep="|", index=False)

def replace_newline_chars(s):
    # Some description fields have newline chars
    # TODO: Check if newline chars is okay or not, they might still be successfully added to the DB
    s = re.sub(r'(\r|\n|\r\n)+(\w)', r', \2', s)
    s = s.strip()
    return s

if __name__ == "__main__":
    main()
