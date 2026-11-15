from flask import Flask, render_template, session, redirect, request
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

from pathlib import Path
from OMDB_API_KEY import API_KEY
import sqlite3


BASE_DIR = Path(__file__).resolve().parent.parent

db_conn = sqlite3.connect("database.db")
db_cursor = db_conn.cursor()

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "frontend" / "templates"),
    static_folder=str(BASE_DIR / "frontend" / "static")
)


@app.route('/movie', methods=['GET', 'POST'])
def movie():

    if request.method == 'POST':

        film = request.form.get('film')

        return render_template(
            'movie.html',
            film=film,
            poster=None,
            overview="Coming soon!",
            year="Coming soon",
            genre="Coming soon",
            runtime="Coming soon",
            submitted_prediction=None
        )

    return render_template(
        'movie.html',
        film="",
        poster=None,
        overview="",
        year="",
        genre="",
        runtime="",
        submitted_prediction=None
    )

@app.route('/predict', methods=['POST'])
def predict():

    film = request.form.get('film')
    prediction = request.form.get('prediction')

    try:
        prediction = float(prediction)

        if prediction < 0:
            raise ValueError

    except (ValueError, TypeError):
        return "Please enter a valid positive prediction.", 400

    return render_template(
        'movie.html',
        film=film,
        poster=None,
        overview="Coming soon!",
        year="Coming soon",
        genre="Coming soon",
        runtime="Coming soon",
        submitted_prediction=prediction
    )

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    pass



#hardcode for the timebeing lol
@app.route('/leaderboard')
def leaderboard():

    players = [
        {
            "rank": 1,
            "username": "FilmFan",
            "games": 12,
            "score": 950
        },
        {
            "rank": 2,
            "username": "cinemalovvvver",
            "games": 10,
            "score": 850
        },
        {
            "rank": 3,
            "username": "movieBro",
            "games": 8,
            "score": 700
        }
    ]

    return render_template(
        "leaderboard.html",
        players=players
    )