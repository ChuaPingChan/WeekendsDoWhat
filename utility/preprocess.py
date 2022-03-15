import pandas as pd
import os

def main():
    ##### Preprocess parks-kml.kml
    df = pd.read_csv(os.path.join(f"{os.path.dirname(os.path.abspath(os.path.dirname(__file__)))}/data/parks/parks-kml.csv"), sep="|")

    # Select only relevant columns
    df = df[[
        'INC_CRC',
        'NAME',
        'LATITUDE',
        'LONGITUDE',
        'DESCRIPTION',
        'HYPERLINK'
    ]]

    # Assert that 'INC_CRC' is unique because we will use it as the primary key later
    assert len(df['INC_CRC'].unique()) == df.shape[0]

    # Remove rows with null data of interests
    df = df[~df[['NAME', 'DESCRIPTION']].isnull().any(axis=1)]

    df.to_csv(f'{os.path.dirname(os.path.abspath(os.path.dirname(__file__)))}/data/parks/parks-kml-processed.csv', sep="|", index=False)

    ##### Preprocess eating-establishments.kml
    df = pd.read_csv(f'{os.path.dirname(os.path.abspath(os.path.dirname(__file__)))}/data/eating-establishments/eating-establishments.csv', sep="|")

    # Select only relevant columns
    df = df[[
        'INC_CRC',
        'BUSINESS_NAME',
        'LATITUDE',
        'LONGITUDE',
        'LIC_NAME',
        'STR_NAME',
        'UNIT_NO',
        'POSTCODE',
        'LEVEL_NO'
    ]]

    # Assert that 'INC_CRC' is unique because we will use it as the primary key later
    assert len(df['INC_CRC'].unique()) == df.shape[0]

    # Remove rows with null data of interests
    df = df[~df[['LIC_NAME', 'STR_NAME', 'POSTCODE']].isnull().any(axis=1)]

    # Perform some renaming for consistency
    df = df.rename(columns={'BUSINESS_NAME': 'NAME'})

    df.to_csv(f'{os.path.dirname(os.path.abspath(os.path.dirname(__file__)))}/data/eating-establishments/eating-establishments-processed.csv', sep="|", index=False)

if __name__ == "__main__":
    main()
