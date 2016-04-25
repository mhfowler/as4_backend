import tempfile
import re
import os
import random

import dropbox

from hello_utilities.log_helper import _log
from hello_settings import SECRETS_DICT, TEMP_PATH


client = dropbox.client.DropboxClient(SECRETS_DICT['DROPBOX_ACCESS_TOKEN'])


def save_note_to_dropbox(title, text):
    if not title:
        title = str(random.randint(0, 10000000))
    temp_path = os.path.join(TEMP_PATH, title)
    with open(temp_path, 'w') as f:
        f.write(text)

    with open(temp_path, 'rb') as f:
        response = client.put_file(title + '.txt', f)

    os.system('rm {}'.format(temp_path))


def download_dropbox_file(dropbox_path, local_path):
    f, metadata = client.get_file_and_metadata(dropbox_path)
    with open(local_path, 'wb') as out_file:
        out_file.write(f.read())


def get_folder_contents(dropbox_path):
    folder_metadata = client.metadata(dropbox_path)
    print "metadata:", folder_metadata


def fetch_screenshot(screenshot_url):
    # TODO: replace with tempfile
    title = str(random.randint(0, 10000000))
    temp_path = os.path.join(TEMP_PATH, str(title))
    # download the dropbox file to temp_path using API
    screenshot_match = re.search('(Screenshot.*\.png)', screenshot_url)
    file_name = screenshot_match.group(1)
    dropbox_path = file_name.replace('%20', ' ')
    dropbox_path = '/Screenshots/' + dropbox_path
    download_dropbox_file(dropbox_path=dropbox_path, local_path=temp_path)
    return temp_path


if __name__ == '__main__':
    # save_note_to_dropbox(title='test', text='test note test note')
    temp_path = os.path.join(TEMP_PATH, 'dropboxtest.png')
    d_path = '/Screenshots/Screenshot 2016-04-24 23.53.41.png'
    # d_path = '/s/h0nty3y9633jzql/Screenshot%202016-04-24%2023.53.41.png'
    # d_path = '/desktop/art/carpet.jpg'
    download_dropbox_file(dropbox_path=d_path, local_path=temp_path)

    # get folder contents
    # d_path = '/Screenshots'
    # get_folder_contents(dropbox_path=d_path)
