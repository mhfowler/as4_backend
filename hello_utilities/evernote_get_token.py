"""
Run this script, and follow the console prompts to get an evernote token.
"""
from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
import evernote.edam.userstore.constants as UserStoreConstants
from evernote.api.client import EvernoteClient

from hello_settings import SECRETS_DICT


def get_auth_token():
    ##
    # Helper function to turn query string parameters into a
    # Python dictionary
    ##
    def parse_query_string(authorize_url):
        uargs = authorize_url.split('?')
        vals = {}
        if len(uargs) == 1:
            raise Exception('Invalid Authorization URL')
        for pair in uargs[1].split('&'):
            key, value = pair.split('=', 1)
            vals[key] = value
        return vals

    ##
    # Create an instance of EvernoteClient using your API
    # key (consumer key and consumer secret)
    ##
    client = EvernoteClient(
                consumer_key = SECRETS_DICT['EVERNOTE_CONSUMER_KEY'],
                consumer_secret = SECRETS_DICT['EVERNOTE_CONSUMER_SECRET'],
                sandbox = False
            )

    ##
    # Provide the URL where the Evernote Cloud API should
    # redirect the user after the request token has been
    # generated. In this example, localhost is used; note
    # that in this example, we're copying the URLs manually
    # and that, in production, this URL will need to
    # automatically parse the response and send the user
    # to the next step in the flow.
    ##
    request_token = client.get_request_token('http://localhost')

    ##
    # Prompt the user to open the request URL in their browser
    ##
    print "Visit this URL in your browser and login"
    print
    print '\t'+client.get_authorize_url(request_token)
    print
    print '-------'

    ##
    # Have the user paste the resulting URL so we can pull it
    # apart
    ##
    print "Paste the URL after login here:"
    authurl = raw_input()

    ##
    # Parse the URL to get the OAuth verifier
    ##
    vals = parse_query_string(authurl)

    ##
    # Use the OAuth verifier and the values from request_token
    # to built the request for our authentication token, then
    # ask for it.
    ##
    auth_token = client.get_access_token(
                request_token['oauth_token'],
                request_token['oauth_token_secret'],
                vals['oauth_verifier']
            )
    print auth_token

if __name__ == '__main__':
    get_auth_token()
