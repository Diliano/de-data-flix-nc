from main import select_movies
from decimal import Decimal
import pytest
from connection import connect_to_db


class TestSelectMoviesDefault:
    def test_builds_list_of_movie_dictionaries_with_desired_types(self):
        movies = select_movies()["movies"]
        assert len(movies) == 25
        for movie in movies:
            assert isinstance(movie["movie_id"], int)
            assert isinstance(movie["title"], str)
            assert isinstance(movie["release_date"], str)
            assert isinstance(movie["rating"], int)
            assert isinstance(movie["cost"], Decimal)
            assert isinstance(movie["classification"], str)

    def test_converts_datetime_object_to_date_string(self):
        movies = select_movies()["movies"]
        for movie in movies:
            if movie["title"] == "Ghostbusters II":
                ghostbusters_ii = movie
        assert ghostbusters_ii["release_date"] == "1989-12-01"

    # If the db holds a NULL rating value, -1 is used as a placeholder to represent this
    def test_converts_null_rating_to_placeholder_value(self):
        movies = select_movies()["movies"]
        for movie in movies:
            if movie["title"] == "Ghostbusters II":
                ghostbusters_ii = movie
        assert ghostbusters_ii["rating"] == -1

    # If the db holds a NULL classification value, a descriptive string replaces it
    def test_converts_null_classification_to_descriptive_string(self):
        movies = select_movies()["movies"]
        for movie in movies:
            if movie["title"] == "Pulp Fiction":
                pulp_fiction = movie
        assert pulp_fiction["classification"] == "No classification available"

    def test_default_movies_sorted_by_title_ascending(self):
        movies = select_movies()["movies"]
        titles = [movie["title"] for movie in movies]
        assert titles == sorted(titles)


class TestSelectMoviesWithSpecifiedSortBy:
    def test_movies_sorted_by_specified_argument_ascending(self):
        movies = select_movies(sort_by="release_date")["movies"]
        release_dates = [movie["release_date"] for movie in movies]
        assert release_dates == sorted(release_dates)

        movies = select_movies(sort_by="rating")["movies"]
        ratings = [movie["rating"] for movie in movies]
        assert ratings == sorted(ratings)

        movies = select_movies(sort_by="cost")["movies"]
        costs = [movie["cost"] for movie in movies]
        assert costs == sorted(costs)

    def test_raises_value_exception_if_provided_invalid_sort_by_param(self):
        with pytest.raises(ValueError) as excinfo:
            select_movies(sort_by="randomcolumn")
        assert str(excinfo.value) == "Invalid sort_by argument provided: randomcolumn"


class TestSelectMoviesWithSpecifiedOrder:
    def test_movies_sorted_by_specified_order(self):
        movies = select_movies(sort_by="release_date", order="DESC")["movies"]
        release_dates = [movie["release_date"] for movie in movies]
        assert release_dates == sorted(release_dates, reverse=True)

        movies = select_movies(sort_by="cost", order="DESC")["movies"]
        costs = [movie["cost"] for movie in movies]
        assert costs == sorted(costs, reverse=True)

        movies = select_movies(sort_by="rating", order="ASC")["movies"]
        ratings = [movie["rating"] for movie in movies]
        assert ratings == sorted(ratings)

    def test_raises_value_exception_if_provided_invalid_order_param(self):
        with pytest.raises(ValueError) as excinfo:
            select_movies(order="randomorder")
        assert str(excinfo.value) == "Invalid order argument provided: randomorder"


class TestSelectMoviesWithSpecifiedMinRating:
    def test_movies_filtered_by_specified_min_rating(self):
        movies = select_movies(sort_by="rating", min_rating=5)["movies"]
        ratings = [movie["rating"] for movie in movies]
        assert all(rating >= 5 for rating in ratings)

        movies = select_movies(min_rating=8)["movies"]
        ratings = [movie["rating"] for movie in movies]
        assert all(rating >= 8 for rating in ratings)

    def test_raises_value_exception_if_provided_invalid_min_rating(self):
        with pytest.raises(ValueError) as excinfo:
            select_movies(sort_by="rating", min_rating=-10)
        assert str(excinfo.value) == "Invalid min_rating argument provided: -10"

        with pytest.raises(ValueError) as excinfo:
            select_movies(sort_by="rating", min_rating=20)
        assert str(excinfo.value) == "Invalid min_rating argument provided: 20"


class TestSelectMoviesAvailableBySpecifiedLocation:
    def test_filters_available_movies_by_specified_location(self):
        movies = select_movies(location="Newcastle")["movies"]
        movie_ids = [movie["movie_id"] for movie in movies]
        db = connect_to_db()
        results = db.run(
            f"""
            SELECT stock.movie_id
            FROM stock
            JOIN stores ON stock.store_id = stores.store_id 
            WHERE stores.city = 'Newcastle'
        """
        )
        db.close()
        db_ids = [result[0] for result in results]
        for id in movie_ids:
            assert id in db_ids

        movies = select_movies(location="Manchester")["movies"]
        movie_ids = [movie["movie_id"] for movie in movies]
        db = connect_to_db()
        results = db.run(
            f"""
            SELECT stock.movie_id
            FROM stock
            JOIN stores ON stock.store_id = stores.store_id 
            WHERE stores.city = 'Manchester'
        """
        )
        db.close()
        db_ids = [result[0] for result in results]
        for id in movie_ids:
            assert id in db_ids

    def test_raises_value_exception_if_provided_invalid_location(self):
        with pytest.raises(ValueError) as excinfo:
            select_movies(location="fakelocation")
        assert str(excinfo.value) == "Invalid location argument provided: fakelocation"
