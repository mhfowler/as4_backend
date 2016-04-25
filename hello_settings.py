import os, json


# project path
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
print 'PROJECT_PATH: {}'.format(PROJECT_PATH)


# secrets dict
SECRETS_PATH = os.path.join(PROJECT_PATH, 'devops/secret_files/secret.json')
SECRETS_DICT = json.loads(open(SECRETS_PATH, "r").read())


# environment dict (different from machine to machine)
ENVIRON_PATH = os.path.join(PROJECT_PATH, 'environment.json')
ENVIRON_DICT = json.loads(open(ENVIRON_PATH, "r").read())

# which environment are we in
ENVIRON = os.environ.get('HELLO_ENVIRON') or ENVIRON_DICT['ENVIRON']
LOCAL = False
DEV = False
PROD = False
if ENVIRON == 'LOCAL':
    LOCAL = True
elif ENVIRON == 'PROD':
    PROD = True
DEBUG = LOCAL

# TEMP
TEMP_PATH = os.path.join(PROJECT_PATH, 'temp')
if not os.path.exists(TEMP_PATH):
    os.makedirs(TEMP_PATH)


# settings
NOTES_CHANNEL = 'C135CHY1H'
NOTES_DROPBOX_FOLDER = '/as4_notes'
VERBOSE_LOG = True

# temporary settings below


# configure database url dynamically
def get_db_url():
    return SECRETS_DICT['TEST_DB_CONNECTION']
