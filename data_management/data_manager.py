from data_management.models import db, User, Movie
from typing import List, Optional

class DataManager:
    def create_user(self, name: str) -> bool:
        try:
            new_user = User(name)
            db.session.add(new_user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Fehler beim Erstellen des Benutzers: {str(e)}")
            return False

    def get_users(self) -> List[User]:
        return User.query.all()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return User.query.get(user_id)

    def get_movies(self, user_id: int) -> List[Movie]:
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie: Movie) -> bool:
        try:
            db.session.add(movie)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Fehler beim Hinzufügen des Films: {str(e)}")
            return False

    def update_movie(self, movie: Movie) -> None:
        db.session.commit()

    def delete_movie(self, movie: Movie) -> None:
        db.session.delete(movie)
        db.session.commit()