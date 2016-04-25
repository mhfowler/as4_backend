import pytumblr
import random
import os
import re

from hello_settings import SECRETS_DICT, TEMP_PATH
from hello_utilities.log_helper import _log
from hello_utilities.dropbox_helper import fetch_screenshot


client = pytumblr.TumblrRestClient(
  SECRETS_DICT['TUMBLR_API_KEY'],
  SECRETS_DICT['TUMBLR_API_SECRET'],
  SECRETS_DICT['TUMBLR_OAUTH_TOKEN'],
  SECRETS_DICT['TUMBLR_OAUTH_SECRET']
)


def post_photo_to_tumblr(photo_url, caption, tumblr='memecollections.tumblr.com'):
    photo_url = photo_url.strip()
    # if a dropbox image, fetch it to a temp file, and then post it
    if photo_url.startswith('https://www.dropbox.com/s/'):
        temp_path = fetch_screenshot(screenshot_url=photo_url)
        created = client.create_photo(tumblr, caption=caption, state="published", data=[temp_path])
        os.system('rm {}'.format(temp_path))
    # if a public image
    else:
        created = client.create_photo(tumblr, caption=caption, state="published", source=photo_url)
    # log the new post
    post_url = 'http://{tumblr}/image/{id}'.format(
        tumblr=tumblr,
        id=created['id']
    )
    _log('++ new tumblr post: {}'.format(post_url))


if __name__ == '__main__':
    # photo = 'https://41.media.tumblr.com/033d1acfdc5e35c7c5b69591506903b6/tumblr_o5ycowfwXs1rdqms8o1_1280.jpg'
    photo = 'https://www.dropbox.com/s/h0nty3y9633jzql/Screenshot%202016-04-24%2023.53.41.png?dl=0'
    caption = 'screenshot test2'
    post_photo_to_tumblr(photo_url=photo, caption=caption)
