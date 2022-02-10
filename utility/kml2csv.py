"""
Converts a KML file to CSV
"""

from bs4 import BeautifulSoup
import os, sys
import pandas as pd

def main():
    """
    Open the KML. Read the KML. Open a CSV file. Process a coordinate string to be a CSV row.
    """
    assert len(sys.argv) == 2, "Please provide the path to the KML file to be converted to CSV"
    kml_file_path = sys.argv[1]
    if not os.path.exists(kml_file_path) or not os.path.isfile(kml_file_path) or not os.path.splitext(kml_file_path)[1] == '.kml':
        print(f"'{kml_file_path}' is not a valid KML file path")
        return

    file_basename, file_extension = os.path.splitext(kml_file_path)
    with open(kml_file_path, 'r') as f:
        soup = BeautifulSoup(f, 'xml')

        column_names = [i.text for i in soup.find_all('displayName')]

        data = []
        for entry in soup.find_all('SchemaData'):
            entry_dict = dict()

            for attr in entry.find_all('SimpleData'):
                entry_dict[attr['name']] = attr.text
            
            data.append(entry_dict)

        df = pd.DataFrame(data)
        df.to_csv(f'{file_basename}.csv')

if __name__ == "__main__":
    main()
