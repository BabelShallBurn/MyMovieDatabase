import os
from flask import Flask, render_template, request, redirect, url_for
from data_management.data_manager import DataManager
from data_management.models import db, Movie
from dotenv import load_dotenv

load_dotenv()
API_key = os.getenv("API_KEY")
API_URL = "http://www.omdbapi.com"

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager() # Create an object of your DataManager class

@app.route('/')
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users)

@app.route('/users', methods=['POST'])
def list_users():
    users = data_manager.get_users()
    return str(users)  # Temporarily returning users as a string

@app.route('/create_user', methods=['POST'])
def create_user():
    username = request.form.get('username')
    if username:
        data_manager.create_user(username)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_movies(user_id):
    movies = data_manager.get_movies(user_id)
    user = data_manager.get_user_by_id(user_id)
    return render_template('movies.html', movies=movies, user=user)


""" @app.route('/users/<int:user_id>/movies', methods=['POST'])


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])


@app.route('/users/<int:user_id>/movies', methods=['POST']) """


if __name__ == '__main__':
  with app.app_context():
    db.create_all()

  app.run(host='0.0.0.0', port=5001, debug=True)