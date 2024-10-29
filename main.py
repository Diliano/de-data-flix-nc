from connection import connect_to_db


def select_movies():
    db = connect_to_db()

    select_query = """
        SELECT *
        FROM movies
        ORDER BY title;
    """

    movies = db.run(sql=select_query)
    db.close()

    # Convert datetime object to a date string
    # If rating is None, replace with -1 as a placeholder
    # If classification is None, replace with a descriptive string
    formatted_movies = [
        {
            "movie_id": movie[0],
            "title": movie[1],
            "release_date": movie[2].strftime("%Y-%m-%d"),
            "rating": -1 if movie[3] is None else movie[3],
            "cost": movie[4],
            "classification": (
                "No classification available" if movie[5] is None else movie[5]
            ),
        }
        for movie in movies
    ]

    return {"movies": formatted_movies}
