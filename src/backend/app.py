from flask import Flask, render_template, session, redirect, request, flash
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path
from OMDB_API_KEY import API_KEY
import sqlite3
import requests
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

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
            ml_prediction=None,
            real_box_office=None
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
        ml_prediction=None,
        real_box_office=None
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
        ml_prediction=ml_prediction[0],
        real_box_office=data.get("BoxOffice")
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
    if "user_id" not in session:
        flash("You have to be logged in to view this page.", "error")
        return redirect("/login")

    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    db_conn = sqlite3.connect("database.db")
    db_cursor = db_conn.cursor()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmed_password = request.form.get('confirm_password')

        if password != confirmed_password:
            flash('Passwords do not match.', "error")
            redirect("/login")

        if not username or not password:
            flash('Please fill out all fields.', "error")
            redirect("/login")

        password = generate_password_hash(password)

        try:
            db_cursor.execute("INSERT INTO users (user_name, password) VALUES (?, ?)", (username, password))
            db_conn.commit()
            flash("Your account has been created, please log in")
            return redirect("/login")
        except ValueError:
            flash(f"The username: {username} is already taken", "error")
            return redirect("/login")

    return render_template("login.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    db_conn = sqlite3.connect("database.db")
    db_conn.row_factory = sqlite3.Row
    db_cursor = db_conn.cursor()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        #   Query the SQL database to look for a match for the username
        row = db_cursor.execute("SELECT * FROM users WHERE user_name = ?", (username,)).fetchone()

        #   Check that the username and password match an account in the database
        if row is None or not check_password_hash(row["password"], password):
            flash("Invalid username and/or password", "error")
            return redirect("/")

        #   Input the user_id in the session
        session["user_id"] = row["id"]

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


@app.route('/leaderboard')
def leaderboard():
    db_conn = sqlite3.connect("database.db")
    db_cursor = db_conn.cursor()

    db_cursor.execute("SELECT user_name, high_score FROM users ORDER BY high_score DESC")
    db_data = db_cursor.fetchall()
    players = []

    rank = 0
    for row in db_data:
        players.append({"rank": rank, "user_name": row[0], "score": row[1]})
        rank += 1

    return render_template(
        "leaderboard.html",
        players=players
    )
