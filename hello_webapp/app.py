import os
import sys
import traceback
import re, json

from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, request

from hello_settings import PROJECT_PATH, get_db_url, DEBUG, NOTES_CHANNEL
from hello_utilities.log_helper import _log
from hello_utilities.dropbox_helper import save_note_to_dropbox
from hello_utilities.process_note import process_note
from hello_utilities.process_note import strip_data
from hello_webapp.helper_routes import get_hello_helpers_blueprint
from hello_models.database import db_session


# paths
FLASK_DIR = os.path.join(PROJECT_PATH, 'hello_webapp')
TEMPLATE_DIR = os.path.join(FLASK_DIR, 'templates')
STATIC_DIR = os.path.join(FLASK_DIR, 'static')


# create flask app
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=PROJECT_PATH)
app.debug = DEBUG


# integrate sql alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_url()
db = SQLAlchemy(app)


# register blueprints
hello_helpers = get_hello_helpers_blueprint(db=db, template_dir=TEMPLATE_DIR)
app.register_blueprint(hello_helpers)


@app.route("/")
def hello_page():
    return render_template("hello.html")


@app.route("/save_note/", methods=['POST'])
def save_note_endpoint():
    text = request.form['text']
    text += ' '
    note_text = strip_data(text)
    note_text_lines = note_text.split('\n')
    title = ''
    # quick loop to find first non blank line, and use that as title
    for line in note_text_lines:
        if line:
            title = line
            break
    # strip special char from title
    stripped_title = title.replace(' ', '_')
    stripped_title = re.sub(r'[\W]+', '', stripped_title)
    # save note to dropbox and log note to slack
    save_note_to_dropbox(title=stripped_title, text=text)
    _log('++ saved note: {}'.format(stripped_title))
    _log('++: {title}\n{text}'.format(title=title, text=text), channel_id=NOTES_CHANNEL)
    # process note and initiate functions based on hashtags
    process_note(text=text, title=title)
    return 'saved'


@app.route('/static/<path:path>')
def send_static(path):
    """
    for local static serving
    this route will never be reached on the server because nginx will bypass flask all together
    """
    return send_from_directory(STATIC_DIR, path)


@app.errorhandler(500)
def error_handler_500(e):
    """
    if a page throws an error, log the error to slack, and then re-raise the error
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    formatted_lines = traceback.format_exc()
    _log('@channel: 500 error: {}'.format(e.message))
    _log(formatted_lines)
    raise e


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run()
