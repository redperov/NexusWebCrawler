from bs4 import BeautifulSoup
import requests
import urllib.request
from urllib.parse import urlparse
import os
import time
from shutil import rmtree

destination_folder = ""


def get_links(url):
    """
    Get all the links from the given url.
    :param url: website url
    :return: list of links
    """
    request = requests.get(url)
    contents = request.content

    soup = BeautifulSoup(contents, features="html.parser")
    links = []

    for link in soup.findAll('a'):
        try:
            links.append(link['href'])
        except KeyError:
            pass
    return links


def download_links(links):
    """
    Downloads all the given links to a folder.
    :param links: list of links
    """
    for link in links:

        # Extract the file name from the url
        parsed_url = urlparse(link)
        file_name = os.path.basename(parsed_url.path)

        # Download the file and save at the destination folder
        if file_name:
            urllib.request.urlretrieve(link, destination_folder + file_name)
            time.sleep(1)


def clean_directory(directory_path):
    """
    Cleans the directory's content
    :param directory_path: path of directory to clean
    """
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


if __name__ == "__main__":
    url = ""
    clean_directory(destination_folder)
    links = get_links(url)
    download_links(links)
