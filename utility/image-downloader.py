'''
Script to download the images of all "places" in the database

Documentation: https://pypi.org/project/bing-image-downloader/
'''
from bing_image_downloader import downloader as img_downloader
import os

img_downloader.download('Marina Bay Singapore', limit=1,  output_dir=f"{os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), 'data', 'images')}", adult_filter_off=True, verbose=True, force_replace=False)
