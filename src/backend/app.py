from flask import Flask, render_template, request
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

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

@app.route('/')
def index():
    return render_template('index.html')