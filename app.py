import os
import requests
from flask import flash, Flask, render_template, request, redirect, url_for
from data_management.data_manager import DataManager
from data_management.models import db, Movie
from dotenv import load_dotenv

load_dotenv()
API_key = os.getenv("API_KEY")
API_URL = "http://www.omdbapi.com"

app = Flask(__name__)

app.secret_key = "my_super_secret_key_123456789!"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager() # Create an object of your DataManager class


def get_data_from_api(search_term:str):
    """Get data from API."""
    try:
        response = requests.get(url=API_URL, params={"apikey": API_key, "t": search_term})
        return response.json()
    except Exception as e:
        return f"Couldn't access API! Error: {e}"


def prepare_data_for_db(movie_title:str):
    """Prepare data for DB."""
    #search_term = input("Enter search term: ")
    response = get_data_from_api(movie_title)
    if isinstance(response, dict) and "Title" in response:
        data_to_return = {"title": response["Title"],
                          "year": int(response["Year"]),
                          "poster_url": response["Poster"],
                          "director": response["Director"],}
        return data_to_return
    else:
        return response


@app.route('/')
def index():
    try:
        users = data_manager.get_users()
    except Exception as e:
        flash(f"Couldn't retrieve users! Error: {e}")
        users = []
    return render_template('index.html', users=users)

@app.route('/create_user', methods=['POST'])
def create_user():
    username = request.form.get('username')
    if username:
        data_manager.create_user(username)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_movies(user_id):
    try:
        movies = data_manager.get_movies(user_id)
        user = data_manager.get_user_by_id(user_id)
    except Exception as e:
        flash(f"Couldn't retrieve movies! Error: {e}")
        return redirect(url_for('index'))
    return render_template('movies.html', movies=movies, user=user)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    title = request.form.get('title')
    if not title:
        flash("Bitte einen Filmtitel eingeben!")
        return redirect(url_for('list_movies', user_id=user_id))
    try:
        movie_to_add = prepare_data_for_db(title)
        if not isinstance(movie_to_add, dict) or not movie_to_add.get('title'):
            flash("Kein gültiger Filmtitel gefunden!")
            return redirect(url_for('list_movies', user_id=user_id))
        # flash(f"Adding movie: {movie_to_add['title']} directed by {movie_to_add['director']} from {movie_to_add['year']}")

        new_movie = Movie(name=movie_to_add['title'],
                        director=movie_to_add['director'],
                        year=int(movie_to_add['year']),
                        poster_url=movie_to_add['poster_url'])
        new_movie.user_id = user_id
        data_manager.add_movie(new_movie)
    except Exception as e:
        flash(f"Couldn't add movie! Error: {e}")
        return redirect(url_for('list_movies', user_id=user_id))

    return redirect(url_for('list_movies', user_id=user_id))



@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        flash("Movie not found!")
        return redirect(url_for('list_movies', user_id=user_id))
    new_title = request.form.get('title')
    if not new_title:
        flash("Bitte einen Filmtitel eingeben!")
        return redirect(url_for('list_movies', user_id=user_id))
    try:
        movie_to_update = prepare_data_for_db(new_title)
        if not isinstance(movie_to_update, dict) or not movie_to_update.get('title'):
            flash("Kein gültiger Filmtitel gefunden!")
            return redirect(url_for('list_movies', user_id=user_id))
        movie.name = movie_to_update['title']
        movie.director = movie_to_update['director']
        movie.year = int(movie_to_update['year'])
        movie.poster_url = movie_to_update['poster_url']
        data_manager.update_movie(movie)
    except Exception as e:
        flash(f"Couldn't update movie! Error: {e}")
        return redirect(url_for('list_movies', user_id=user_id))
    return redirect(url_for('list_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    movie = Movie.query.get(movie_id)
    if movie:
        data_manager.delete_movie(movie)
    else:
        flash("Movie not found!")
        return redirect(url_for('list_movies', user_id=user_id))
    return redirect(url_for('list_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
  with app.app_context():
    db.create_all()

  app.run(host='0.0.0.0', port=5001, debug=True)