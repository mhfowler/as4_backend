import re

from hello_utilities.tumblr_helper import post_photo_to_tumblr
from hello_utilities.log_helper import _log
from hello_utilities.evernote_helper import save_evernote


def get_hashtags(text):
    hashtags = {tag.strip("#") for tag in text.split() if tag.startswith("#")}
    return hashtags


def strip_data(text):
    lines = text.split('\n')
    note_lines = filter(lambda line: not (line.startswith('url: ') or line.startswith('img: ')), lines)
    stripped = '\n'.join(note_lines)
    return stripped


def tumblr_post_img(text):
    img_match = re.search('img:(.*)\n', text)
    if img_match:
        _log('++ saving image to tumblr', debug=True)
        url = img_match.group(1)
        note_text = strip_data(text)
        post_photo_to_tumblr(photo_url=url, caption=note_text)


def process_note(text, title):
    hashtags = get_hashtags(text)
    _log('++ found hashtags: {}'.format(str(hashtags)), debug=True)
    if 'meme' in hashtags:
        tumblr_post_img(text)
    # save to evernote
    save_evernote(note_title=title, note_text=text, notebook_name='as4')


if __name__ == '__main__':
    process_note('img: https://41.media.tumblr.com/a02410dc6a319722b3c77207e7a3b039/tumblr_o5uc36xK271qcphy8o1_1280.jpg\n'
                 '\nhello test\n ', title='test as4')