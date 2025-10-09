# MyMovieDatabase

A Flask web application for managing personal movie collections. Users can create and maintain their own movie collections using data from the OMDb API. This project is for educational purposes.

## Features

- Create and manage users
- Add movies to personal collection
- Automatic movie data retrieval via OMDb API
- Edit and delete movies
- Movie poster display for visual overview
- Error handling and user feedback

## Installation

1. Repository klonen:
```bash
git clone https://github.com/BabelShallBurn/MyMovieDatabase.git
cd MyMovieDatabase
```

2. Virtuelle Umgebung erstellen und aktivieren:
```bash
python -m venv .venv
source .venv/bin/activate  # Unter Windows: .venv\Scripts\activate
```

3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
cp .env.example .env
```
Then in `.env`:
- Set `API_KEY` with your OMDb API key
- Set `APP_KEY` for Flask secret key

## Usage

1. Start the server:
```bash
python app.py
```

2. Open in browser:
```
http://localhost:5000
```

## Project Structure

```
MyMovieDatabase/
├── app.py                 # Flask main application
├── data/                  # Database files
├── data_management/      
│   ├── data_manager.py   # Database operations
│   └── models.py         # SQLAlchemy models
├── static/               # Static files (CSS, JS)
└── templates/            # HTML templates
```

## Technologies

- Python 3.x
- Flask (Web Framework)
- SQLAlchemy (ORM)
- OMDb API (Movie Data)
- SQLite (Database)