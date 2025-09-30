from models import db, User, Movie

class DataManager():
  # Define Crud operations as methods
  def create_user(self, name):
    new_user = User(name)
    db.session.add(new_user)
    db.session.commit()

    def get_users(self):
        return User.query.all()

    def get_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie):

        db.session.commit()

    def delete_movie(self, movie):
        db.session.delete(movie)
        db.session.commit()