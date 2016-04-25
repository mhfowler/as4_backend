import re

from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
import evernote.edam.userstore.constants as UserStoreConstants
from evernote.api.client import EvernoteClient

from hello_settings import SECRETS_DICT
from hello_utilities.log_helper import _log


client = EvernoteClient(token=SECRETS_DICT['EVERNOTE_TOKEN'], sandbox=False)


def save_evernote(note_title, note_text, notebook_name):
    _log('++ saving evernote: {}'.format(note_title), debug=True)
    # first get the notebook guid
    notebook_guid = get_or_create_notebook(name=notebook_name)
    # find links in the note, and replaces with a
    urlfinder = re.compile("(http\S+)")
    note_text = urlfinder.sub(r'<a href="\1">\1</a>', note_text)
    # wrap newlines in div
    note_text = '<div>{}</div>'.format(note_text)
    note_text = note_text.replace('\n', '<br></br>')
    # then create the note
    noteStore = client.get_note_store()
    note = Types.Note()
    note.title = note_title
    note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    note.content += '<en-note>{note_text}</en-note>'.format(note_text=note_text)
    note.notebookGuid = notebook_guid
    note = noteStore.createNote(note)
    _log('++ new evernote note: https://www.evernote.com/Home.action#n={}'.format(note.guid))
    return note.guid


def get_user():
    userStore = client.get_user_store()
    user = userStore.getUser()
    print user.username


def get_notebooks():
    noteStore = client.get_note_store()
    notebooks = noteStore.listNotebooks()
    for n in notebooks:
        print n.name


def get_or_create_notebook(name):
    noteStore = client.get_note_store()
    notebooks = noteStore.listNotebooks()
    for n in notebooks:
        if n.name == name:
            return n.guid
    # otherwise we must create new notebook
    notebook = Types.Notebook()
    notebook.name = name
    notebook = noteStore.createNotebook(notebook)
    return notebook.guid


if __name__ == '__main__':
    save_evernote(
        note_title='test token',
        note_text='new token: test evernote with image link: https://49.media.tumblr.com/faf7df3a35903046215ac67f5c0cde2b/tumblr_o64ev51pcp1rdqms8o1_500.gif  ',
        notebook_name='as4')
