import simplenote

from hello_settings import SECRETS_DICT
from hello_utilities.log_helper import _log


snote = simplenote.Simplenote(SECRETS_DICT['SIMPLENOTE_USER'], SECRETS_DICT['SIMPLENOTE_PASSWORD'])


def get_notes():
    returned = snote.get_note_list(since='2016-04-25')
    notes = returned[0]
    notes.sort(key=lambda note: note['modifydate'], reverse=True)
    note_keys = [note['key'] for note in notes]
    return note_keys[0]


def get_note(note_id):
    note = snote.get_note(note_id)[0]
    note_text = note['content']
    return note


def save_simplenote(note_text, tags=None):
    if not tags: tags = []
    new_note = snote.add_note({
        'content': note_text.encode('ascii', 'ignore'),
        'tags': tags
    })[0]
    _log('++ new simplenote: {}'.format(new_note['key']))
    return new_note


if __name__ == '__main__':
    note_key = get_notes()

    # note_key = '4d98379280bf4674a725fca3f6f4a90c'
    # note_key = u'909d12e10b2311e68c279d3c7ea1cbf8'
    # note_key = '713199b6a55f4c0a9d352adddc09782a'
    note = get_note(note_id=note_key)
    print note['content']
    # new_note = save_simplenote(note_text='testing taggin a note and taggin',
    #                            tags=['banana', 'test'])