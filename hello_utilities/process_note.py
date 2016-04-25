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


def save_simplenote_helper(text, hashtags):
    # remove hashtags from note and put them at the bottom
    lines = text.split('\n')
    lines = [strip_line(line) for line in lines]
    note_lines = filter(lambda line: not (line.startswith('source: ') or line.startswith('img: ')), lines)
    source_lines = filter(lambda line: line.startswith('source: '), lines)
    img_lines = filter(lambda line: line.startswith('img: '), lines)
    simplenote_text = '\n'.join(note_lines)
    # remove any initial blank lines
    while simplenote_text and simplenote_text[0] == '\n':
        simplenote_text = simplenote_text[1:]
    # if simplenote_text does not add with newlines then add 2
    if simplenote_text[-1] != '\n':
        simplenote_text += '\n'
    if simplenote_text[-2] != '\n':
        simplenote_text += '\n'
    # append img and source lines to note
    if img_lines:
        simplenote_text += '\n'.join(img_lines) + '\n\n'
    if source_lines:
        simplenote_text += '\n'.join(source_lines)
    # add metadata to the bottom
    hashtag_line = ' '.join([('#' + tag) for tag in hashtags])
    simplenote_text += '\n' + hashtag_line
    hashtags.append('as4notes')
    save_simplenote(note_text=simplenote_text, tags=hashtags)


def process_note(text, title):
    # get commands
    commands = get_commands(text)
    _log('++ found commands: {}'.format(str(commands)), debug=True)
    # trigger actions based on certain commands
    if 'meme' in commands:
        tumblr_post_img(text)
    # get hashtags
    hashtags = list(get_hashtags(text))
    _log('++ found hashtags: {}'.format(str(hashtags)), debug=True)
    # use a hashtag as an evernote notebook name
    if not hashtags:
        notebook_name = 'as4'
    else:
        notebook_name = hashtags[0]
    # save a simplenote
    save_simplenote_helper(text=text, hashtags=hashtags)
    # save an evernote
    save_evernote(note_title=title, note_text=text, notebook_name=notebook_name)


if __name__ == '__main__':

    note_text = 'source: https://www.tumblr.com/dashboard\n\n' \
                'img: https://40.media.tumblr.com/tumblr_luyygcHHPZ1qh2axio1_1280.jpg\n\n' \
                'stop the war\n\n'

    process_note(text=note_text,
                 title='test as4')