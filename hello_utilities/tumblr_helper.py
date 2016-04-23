import pytumblr

from hello_settings import SECRETS_DICT
from hello_utilities.log_helper import _log


client = pytumblr.TumblrRestClient(
  SECRETS_DICT['TUMBLR_API_KEY'],
  SECRETS_DICT['TUMBLR_API_SECRET'],
  SECRETS_DICT['TUMBLR_OAUTH_TOKEN'],
  SECRETS_DICT['TUMBLR_OAUTH_SECRET']
)


def post_photo_to_tumblr(photo_url, caption):
    tumblr = 'memecollections.tumblr.com'
    photo_url = photo_url.strip()
    created = client.create_photo(tumblr, caption=caption, state="published", source=photo_url)
    post_url = 'http://{tumblr}/image/{id}'.format(
        tumblr=tumblr,
        id=created['id']
    )
    _log('++ new tumblr post: {}'.format(post_url))


if __name__ == '__main__':
    photo = 'https://41.media.tumblr.com/033d1acfdc5e35c7c5b69591506903b6/tumblr_o5ycowfwXs1rdqms8o1_1280.jpg'
    caption = 'waves'
    post_photo_to_tumblr(photo_url=photo, caption=caption)
