from main import select_movies


class TestSelectMovies:
    def test_builds_list_of_movie_dictionaries_with_desired_types(self):
        movies = select_movies()["movies"]
        assert len(movies) == 25
        for movie in movies:
            assert isinstance(movie["movie_id"], int)
            assert isinstance(movie["title"], str)
            assert isinstance(movie["release_date"], str)
            assert isinstance(movie["rating"], int)
            assert isinstance(movie["classification"], str)

    def test_converts_datetime_object_to_date_string(self):
        movies = select_movies()["movies"]
        for movie in movies:
            if movie["title"] == "Ghostbusters II":
                ghostbusters_ii = movie
        assert ghostbusters_ii["release_date"] == "1989-12-01"

    # If the db holds a Null rating value, -1 is used as a placeholder to represent this
    def test_converts_null_rating_to_placeholder_value(self):
        movies = select_movies()["movies"]
        for movie in movies:
            if movie["title"] == "Ghostbusters II":
                ghostbusters_ii = movie
        assert ghostbusters_ii["rating"] == -1

    # If the db holds a Null classification value, a descriptive string replaces it
    def test_converts_null_classification_to_descriptive_string(self):
        movies = select_movies()["movies"]
        for movie in movies:
            if movie["title"] == "Pulp Fiction":
                pulp_fiction = movie
        assert pulp_fiction["classification"] == "No classification available"

    def test_default_movies_sorted_by_title(self):
        movies = select_movies()["movies"]
        titles = [movie["title"] for movie in movies]
        assert titles == sorted(titles)
