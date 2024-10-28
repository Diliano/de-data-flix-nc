\c nc_flix

-- Query the database to find the store with the highest total number of copies of sequels. 
-- Let's assume a film is a sequel if the title contains something like 'II' or 'VI'.
-- II, IV, IX

SELECT store_id, COUNT(movie_id) as stock_of_sequels
FROM stock 
WHERE movie_id IN (
    SELECT movie_id
    FROM movies
    WHERE title LIKE '%II%' OR title LIKE '%IV%' OR title LIKE '%IX%'
)
GROUP BY store_id
ORDER BY stock_of_sequels DESC
LIMIT 1;

-- This is likely not a good way to identify sequels going forward. 
-- Alter the movies table to track this information better and then update the previous query to make use of this new structure.

ALTER TABLE movies
ADD COLUMN is_sequel boolean;

UPDATE movies
SET is_sequel = TRUE
WHERE movie_id IN (
    SELECT movie_id
    FROM movies
    WHERE title LIKE '%II%' OR title LIKE '%IV%' OR title LIKE '%IX%'
);

SELECT stock.store_id, COUNT(stock.movie_id) AS stock_of_sequels
FROM stock 
JOIN movies ON stock.movie_id = movies.movie_id
WHERE movies.is_sequel = TRUE
GROUP BY stock.store_id
ORDER BY stock_of_sequels DESC 
LIMIT 1;
