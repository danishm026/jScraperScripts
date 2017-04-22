#!/usr/bin/python3

import os
import json

OUTPUT_DIRECTORY = os.environ['SCRAPER_OUTPUT_DIRECTORY']
SCRAPE_COMMAND = 'java -Doutput.directory=' + OUTPUT_DIRECTORY + ' -cp uber-jScraper-0.0.1-SNAPSHOT.jar com.arc.jScraper.main.Main '
DOWNLOAD_COMMAND = 'wget -U="" --continue '
MODEL_PAGES = 'modelPages'
IMAGE_DATA_LIST = 'imageDataList'
IMAGE_URL = 'imageUrl'


def get_file_path(model_name):
    file_name = "_".join(model_name.strip().split())
    return os.path.join(os.path.join(OUTPUT_DIRECTORY, file_name), file_name)


def get_file_content_as_json(file_path):
    with open(file_path) as f:
        file_content = json.load(f)
    return file_content


def get_image_urls(model_data):
    image_urls = []
    model_pages = model_data[MODEL_PAGES]
    for model_page in model_pages:
        image_data_list = model_page[IMAGE_DATA_LIST]
        for image_data in image_data_list:
            image_urls.append(image_data[IMAGE_URL])
    return image_urls


def scrape_model(model_name):
    os.system(SCRAPE_COMMAND + '"' + model_name + '"')


def download_images(model_name, image_urls):
    current_directory = os.getcwd()
    file_name = "_".join(model_name.strip().split())
    os.chdir(os.path.join(OUTPUT_DIRECTORY, file_name))
    for image_url in image_urls:
        if image_url is not None:
            os.system(DOWNLOAD_COMMAND + '"' + image_url + '"')
    os.chdir(current_directory)


if __name__ == '__main__':
    name = str(input()).strip()
    scrape_model(name)
    file = get_file_path(name)
    model_json = get_file_content_as_json(file)
    download_images(name, get_image_urls(model_json))
