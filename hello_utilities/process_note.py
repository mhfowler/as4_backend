import re

from hello_utilities.tumblr_helper import post_photo_to_tumblr
from hello_utilities.log_helper import _log
from hello_utilities.evernote_helper import save_evernote
from hello_utilities.simplenote_helper import save_simplenote


def get_hashtags(text):
    hashtags = {tag.strip("#").encode('ascii', 'ignore') for tag in text.split() if tag.startswith("#")}
    return hashtags


def get_commands(text):
    hashtags = {tag.strip("\\").encode('ascii', 'ignore') for tag in text.split() if tag.startswith("\\")}
    return hashtags


def strip_data(text):
    lines = text.split('\n')
    note_lines = filter(lambda line: not (line.startswith('source: ') or line.startswith('img: ')), lines)
    note_lines = [strip_line(line) for line in note_lines]
    stripped = '\n'.join(note_lines)
    return stripped


def strip_line(line):
    words = line.split(' ')
    words = filter(lambda word: not word.startswith('#') and not word.startswith('\\'), words)
    stripped = ' '.join(words)
    return stripped


def tumblr_post_img(text):
    img_match = re.search('img:(.*)\n', text)
    if img_match:
        _log('++ saving image to tumblr', debug=True)
        url = img_match.group(1)
        note_text = strip_data(text)
        post_photo_to_tumblr(photo_url=url, caption=note_text)


def process_note(text, title):
    commands = get_commands(text)
    _log('++ found commands: {}'.format(str(commands)), debug=True)
    if 'meme' in commands:
        tumblr_post_img(text)
    # save to evernote
    hashtags = list(get_hashtags(text))
    _log('++ found hashtags: {}'.format(str(hashtags)), debug=True)
    if not hashtags:
        notebook_name = 'as4'
    else:
        notebook_name = hashtags[0]
    # save a simplenote
    # remove hashtags from note and put them at the bottom
    lines = text.split('\n')
    lines = [strip_line(line) for line in lines]
    simplenote_text = '\n'.join(lines)
    # add metadata to the bottom
    hashtag_line = ' '.join([('#' + tag) for tag in hashtags])
    simplenote_text += '\n' + hashtag_line
    hashtags.append('as4notes')
    save_simplenote(note_text=simplenote_text, tags=hashtags)
    # save an evernote
    save_evernote(note_title=title, note_text=text, notebook_name=notebook_name)


if __name__ == '__main__':

    note_text = 'source: https://www.tumblr.com/dashboard\n\n' \
                'img: https://40.media.tumblr.com/tumblr_luyygcHHPZ1qh2axio1_1280.jpg\n\n' \
                'stop the war \meme '

    process_note(text=note_text,
                 title='test as4')