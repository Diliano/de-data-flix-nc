from connection import connect_to_db
from pg8000.native import identifier, literal


def select_movies(sort_by="title", order="ASC", min_rating=None, location=None):
    if sort_by not in {"title", "release_date", "rating", "cost"}:
        invalid_param_handler("sort_by", sort_by)

    if order not in {"ASC", "DESC"}:
        invalid_param_handler("order", order)

    if min_rating and min_rating not in range(0, 11):
        invalid_param_handler("min_rating", min_rating)

    if location and location not in {"Leeds", "Manchester", "Newcastle", "Birmingham"}:
        invalid_param_handler("location", location)

    db = connect_to_db()

    # If rating is NULL, replace with -1 as a placeholder
    # If classification is NULL, replace with a descriptive string
    select_query = f"""
        SELECT movie_id, title, release_date, COALESCE(rating, -1), cost, COALESCE(classification, 'No classification available')
        FROM movies
    """

    if min_rating:
        select_query += f""" WHERE rating >= {literal(min_rating)}"""

    if location:
        if min_rating:
            select_query += f""" AND movie_id IN (
                SELECT stock.movie_id
                FROM stock
                JOIN stores ON stock.store_id = stores.store_id 
                WHERE stores.city = {literal(location)}
            )"""
        else:
            select_query += f""" WHERE movie_id IN (
                SELECT stock.movie_id
                FROM stock
                JOIN stores ON stock.store_id = stores.store_id 
                WHERE stores.city = {literal(location)}
            )"""

    if sort_by == "rating":
        select_query += f""" ORDER BY COALESCE(rating, -1) {identifier(order)}"""
    else:
        select_query += f""" ORDER BY {identifier(sort_by)} {identifier(order)}"""

    movies = db.run(sql=select_query)
    db.close()

    # Convert datetime object to a date string
    formatted_movies = [
        {
            "movie_id": movie[0],
            "title": movie[1],
            "release_date": movie[2].strftime("%Y-%m-%d"),
            "rating": movie[3],
            "cost": movie[4],
            "classification": movie[5],
        }
        for movie in movies
    ]

    return {"movies": formatted_movies}


def invalid_param_handler(param, arg):
    raise ValueError(f"Invalid {param} argument provided: {arg}")
