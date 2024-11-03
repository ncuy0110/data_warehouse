import pandas as pd
from src import settings
from src.db import db

film_db = db["films"]

def import_film():
    try:
        if film_db.count_documents({}) != 0:
            film_db.drop()
    except:
        pass

    df = pd.read_excel(settings.input_path, sheet_name='film')

    # Extract unique films
    films = df[['show_id', 'title', 'director', 'cast', 'country', 'release_year', 'rating', 'duration', 'listed_in', 'description']].drop_duplicates()


    # Convert to dictionary
    films_dict = films.to_dict(orient='records')

    print(films_dict[:5])
    print(len(films_dict))

    for film in films_dict:
        try:
            film_db.insert_one(film)
        except:
            pass