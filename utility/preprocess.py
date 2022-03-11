import pandas as pd
import os

def main():
    ##### Preprocess parks-kml.kml
    df = pd.read_csv(os.path.join(f"{os.path.dirname(os.path.abspath(os.path.dirname(__file__)))}/data/parks/parks-kml.csv"), sep="|")

    # Remove rows with null data of interests
    df = df[~df[['LANDXADDRESSPOINT', 'LANDYADDRESSPOINT', 'NAME', 'DESCRIPTION']].isnull().any(axis=1)]

    df.to_csv(f'{os.path.dirname(os.path.abspath(os.path.dirname(__file__)))}/data/parks/parks-kml-processed.csv', sep="|")

    ##### Preprocess parks-kml.kml
    df = pd.read_csv(f'{os.path.dirname(os.path.abspath(os.path.dirname(__file__)))}/data/eating-establishments/eating-establishments.csv', sep="|")

    # Remove rows with null data of interests
    df = df[~df[['LIC_NAME', 'STR_NAME', 'POSTCODE', 'LIC_NO']].isnull().any(axis=1)]

    df.to_csv(f'{os.path.dirname(os.path.abspath(os.path.dirname(__file__)))}/data/eating-establishments/eating-establishments-processed.csv', sep="|")

if __name__ == "__main__":
    main()
