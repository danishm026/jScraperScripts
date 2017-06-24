#!/usr/bin/python
from optparse import OptionParser

import os
import json

import subprocess


OUTPUT_DIRECTORY = "/home/danish/.scraper/output"
MODEL_PAGES = 'modelPages'
IMAGE_DATA_LIST = 'imageDataList'
IMAGE_URL = 'imageUrl'


def scrape_model_command(model_name):
    scrape_command = ['java']
    scrape_command.append('-cp')
    scrape_command.append('uber-jScraper-0.0.1-SNAPSHOT.jar')
    scrape_command.append('com.arc.jScraper.main.Main')
    scrape_command.append(model_name)
    subprocess.call(scrape_command)


def download_image(url, download_directory):
    download_command = ['wget']
    download_command.append('-U')
    download_command.append('')
    download_command.append('--continue')
    download_command.append('--directory-prefix')
    download_command.append(download_directory)
    download_command.append(url)
    subprocess.call(download_command)


def replace_space_with_underscore(string):
    return "_".join(string.strip().split())


def parse_command_line_arguments():
    parser = OptionParser()
    parser.add_option("-s", "--scrape", dest="scrape", action="store_true",
                      help="Specify whether to scrape model or not")
    parser.add_option("-d", "--download", dest="download", action="store_true",
                      help="Specify whether to download images  or not")
    parser.add_option("-n", "--name", dest="name", help="Name of model")
    options, args = parser.parse_args()
    if options.scrape is None and options.download is None:
        print "Either scrape or download flag must be present"
        exit(1)
    if options.name is None:
        print "Name must be present"
        exit(2)
    return options.scrape, options.download, options.name


def get_file_path(model_name):
    file_name = replace_space_with_underscore(model_name.title())
    return os.path.join(os.path.join(OUTPUT_DIRECTORY, file_name), file_name)


def get_file_content_as_json(file_path):
    with open(file_path) as file_handle:
        file_content = json.load(file_handle)
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
    scrape_model_command(model_name)


def download_images(model_name, image_urls):
    file_name = replace_space_with_underscore(model_name.title())
    download_directory = os.path.join(OUTPUT_DIRECTORY, file_name)
    for image_url in image_urls:
        if image_url is not None:
            download_image(image_url, download_directory)


if __name__ == '__main__':
    scrape, download, name = parse_command_line_arguments()
    if scrape:
        print "Scraping  %s", name
        scrape_model(name)
    file_path = get_file_path(name)
    model_json = get_file_content_as_json(file_path)
    if download:
        print "Download %s", name
        download_images(name, get_image_urls(model_json))

