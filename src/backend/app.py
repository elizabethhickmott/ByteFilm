from flask import Flask, render_template, session, redirect, request
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path
from OMDB_API_KEY import API_KEY
import sqlite3
import requests
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

db_conn = sqlite3.connect("database.db")
db_cursor = db_conn.cursor()

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "frontend" / "templates"),
    static_folder=str(BASE_DIR / "frontend" / "static")
)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/movie', methods=['GET', 'POST'])
def movie():

    BASE_URL = "http://www.omdbapi.com/"
    POSTER_BASE_URL = "http://img.omdbapi.com/"

    if request.method == 'POST':

        film = request.form.get('film')
        api_request = requests.get(BASE_URL, params={"apikey": API_KEY, "t": film}, timeout=15)
        data = api_request.json()

        return render_template(
            'movie.html',
            film=film,
            poster=data.get("Poster"),
            overview=data.get("Plot"),
            year=data.get("Year"),
            genre=data.get("Genre"),
            runtime=data.get("Runtime"),
            submitted_prediction=None,
            ml_prediction = None,
            real_box_office = None
        )

    return render_template(
        'movie.html',
        film="",
        poster=None,
        overview="",
        year="",
        genre="",
        runtime="",
        submitted_prediction=None,
        ml_prediction = None,
        real_box_office = None
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

    BASE_URL = "http://www.omdbapi.com/"
    api_request = requests.get(BASE_URL, params={"apikey": API_KEY, "t": film}, timeout=15)
    data = api_request.json()

    model = joblib.load("../models/ml_model.pkl")

    movie_df = create_movie_df(data)

    ml_prediction = model.predict(movie_df)

    return render_template(
        'movie.html',
        film=film,
        poster=data.get("Poster"),
        overview=data.get("Plot"),
        year=data.get("Year"),
        genre=data.get("Genre"),
        runtime=data.get("Runtime"),
        submitted_prediction=prediction,
        ml_prediction = ml_prediction[0],
        real_box_office = data.get("BoxOffice")
    )

def create_movie_df(data):
    final_df = pd.DataFrame()
    final_df.at[0, "genre"] = data.get("Genre")
    final_df.at[0, "year"] = data.get("Year")
    final_df.at[0, "language"] = data.get("Language")
    final_df.at[0, "rated"] = data.get("Rated")
    final_df.at[0, "country"] = data.get("Country")
    runtime = data.get("Runtime")
    runtime_str = ""

    if runtime is not None:
        for char in runtime:
            if char.isdigit():
                runtime_str += char

    final_df.at[0, "runtime"] = pd.to_numeric(runtime_str, errors="coerce")
    final_df.at[0, "metacritic_rating"] = pd.to_numeric(data.get("Metascore"), errors="coerce")
    final_df.at[0, "imdb_rating"] = pd.to_numeric(data.get("imdbRating"), errors="coerce")

    ratings = data.get("Ratings", [])

    for rating in ratings:
        if rating.get("Source") == "Rotten Tomatoes":
            final_df.at[0, "rotten_tomatoes"] = pd.to_numeric(rating["Value"][:-1], errors="coerce")

    return final_df

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