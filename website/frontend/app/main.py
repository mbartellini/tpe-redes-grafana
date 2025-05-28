from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/media/<int:media_id>')
def show_media(media_id):
    return f'Media {media_id}'