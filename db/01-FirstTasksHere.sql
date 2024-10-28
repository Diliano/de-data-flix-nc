\c nc_flix

-- Query the database to retrieve all of the movie titles that were released in the 21st century.

SELECT title
FROM movies
WHERE EXTRACT(YEAR FROM release_date) >= 2001;

-- Query the database to find the oldest customer.

SELECT customer_name, date_of_birth
FROM customers
WHERE date_of_birth = (SELECT MIN(date_of_birth) FROM customers);

-- Query the database to find the customers whose name begins with the letter D. Organise the results by age, youngest to oldest.

SELECT customer_name, date_of_birth
FROM customers
WHERE customer_name LIKE 'D%'
ORDER BY date_of_birth DESC;

-- Query the database to find the average rating of the movies released in the 1980s.

SELECT ROUND(AVG(rating), 2) AS avg_rating_for_1980s_release
FROM movies
WHERE EXTRACT(YEAR FROM release_date) BETWEEN 1980 AND 1989;

-- Query the database to list the locations of our customers, as well as the total and average number of loyalty points for all customers. 
-- You can assume that if the loyalty points row is empty, they are a new customer so they should have the value set to zero.

SELECT location, SUM(COALESCE(loyalty_points, 0)), ROUND(AVG(COALESCE(loyalty_points, 0)), 2)
FROM customers
GROUP BY location;

-- The rise in living costs is affecting rentals. Drop the cost of all rentals by 5% and display the updated table. 
-- As this is a monetary value, make sure it is rounded to 2 decimal places.

SELECT title, cost AS old_cost, ROUND((cost * 0.95), 2) AS updated_cost
FROM movies;