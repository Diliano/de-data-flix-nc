\c nc_flix

-- Query the database to find the number of films in stock for each genre.

SELECT genres.genre_name, COUNT(stock.movie_id) AS num_in_stock
FROM genres
LEFT JOIN movies_genres ON genres.genre_id = movies_genres.genre_id
LEFT JOIN movies ON movies_genres.movie_id = movies.movie_id
LEFT JOIN stock ON movies.movie_id = stock.movie_id
GROUP BY genres.genre_name;

-- Query the database to find the average rating for films in stock in Newcastle.

SELECT ROUND(AVG(rating), 2) AS avg_rating 
FROM movies
JOIN stock ON movies.movie_id = stock.movie_id
JOIN stores ON stock.store_id = stores.store_id
WHERE stores.city = 'Newcastle';

-- Query the database to retrieve all the films released in the 90s that have a rating greater than the total average.

SELECT title, rating
FROM movies
WHERE (EXTRACT(YEAR FROM release_date) BETWEEN 1990 AND 1999) AND rating > (SELECT (AVG(rating)) FROM movies);

-- Query the database to find the total number of copies that are in stock for the top-rated film from a pool of the five most recently released films.

WITH recent_five AS (
    SELECT movie_id, title, rating
    FROM movies
    WHERE rating IS NOT NULL
    ORDER BY release_date DESC 
    LIMIT 5
)
SELECT top_rated.movie_id, top_rated.title, COUNT(stock.movie_id) AS num_in_stock
FROM (
    SELECT movie_id, title, rating
    FROM recent_five
    WHERE rating = (SELECT MAX(rating) FROM recent_five)
) AS top_rated
LEFT JOIN stock ON top_rated.movie_id = stock.movie_id
GROUP BY top_rated.movie_id, top_rated.title;

-- Query the database to find a list of all the locations in which customers live that don't contain a store.

SELECT DISTINCT location AS locations_without_a_store
FROM customers 
WHERE location NOT IN (SELECT city FROM stores);

-- Query the database to find a list of all the locations we have influence over (locations of stores and/or customers). There should be no repeated data.

SELECT location AS all_locations
FROM customers 
UNION 
SELECT city 
FROM stores;

-- From a list of our stores which have customers living in the same location, calculate which store has the largest catalogue of stock. 
-- What is the most abundant genre in that store?

SELECT stores.store_id, stores.city, COUNT(stock.store_id) AS total_stock
FROM stores 
JOIN stock ON stores.store_id = stock.store_id 
WHERE stores.store_id IN (
    SELECT stores.store_id
    FROM stores
    WHERE stores.city IN (
        SELECT location 
        FROM customers 
        INTERSECT 
        SELECT city 
        FROM stores
    )
)
GROUP BY stores.store_id
ORDER BY total_stock DESC 
LIMIT 1;


SELECT genres.genre_name, COUNT(stock.movie_id) AS num_in_stock
FROM genres 
JOIN movies_genres ON genres.genre_id = movies_genres.genre_id  
JOIN movies ON movies_genres.movie_id = movies.movie_id 
JOIN stock ON movies.movie_id = stock.movie_id
WHERE stock.store_id = 2
GROUP BY genres.genre_name, stock.store_id
ORDER BY num_in_stock DESC
LIMIT 1;
