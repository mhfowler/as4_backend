import tempfile
import os

import dropbox

from hello_utilities.log_helper import _log
from hello_settings import SECRETS_DICT, TEMP_PATH


client = dropbox.client.DropboxClient(SECRETS_DICT['DROPBOX_ACCESS_TOKEN'])


def save_note_to_dropbox(title, text):
    temp_path = os.path.join(TEMP_PATH, title)
    with open(temp_path, 'w') as f:
        f.write(text)

    with open(temp_path, 'rb') as f:
        response = client.put_file(title + '.txt', f)

    os.system('rm {}'.format(temp_path))


if __name__ == '__main__':
    save_note_to_dropbox(title='test', text='test note test note')
