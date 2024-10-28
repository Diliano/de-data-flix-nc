\c nc_flix

-- Design a way of storing information on rentals. A rental should track the following information:
-- rental_id, stock_id, rental_start, rental_end, customer_id   
-- Add some rental rows we can query later.

CREATE TABLE rentals (
    rental_id SERIAL PRIMARY KEY,
    stock_id INT REFERENCES stock(stock_id),
    rental_start DATE,
    rental_end DATE,
    customer_id INT REFERENCES customers(customer_id)
);

INSERT INTO rentals (
    stock_id, rental_start, rental_end, customer_id
) 
VALUES 
    (1, '2024-10-01', '2024-10-05', 1),
    (2, '2024-09-08', '2024-09-15', 2),
    (3, '2024-10-25', '2024-10-26', 3),
    (4, '2024-10-01', '2024-10-09', 4);

-- Finally, we have a customer in one of our stores! They wish to rent a film but have some requirements:
-- The film must be age-appropriate (classification of U).
-- The film must be available in Birmingham.
-- The film must not have been rented more than 5 times already.
-- Instead of creating a list of only the films that match this criteria, create an output that marks yes or no in a column that represents the requirement.

SELECT movies.title, CASE WHEN COUNT(rentals.stock_id) <= 5 THEN 'yes' ELSE 'no' END AS meets_requirement
FROM movies 
JOIN stock ON movies.movie_id = stock.movie_id
JOIN stores ON stock.store_id = stores.store_id
LEFT JOIN rentals ON stock.stock_id = rentals.stock_id
WHERE movies.classification = 'U' AND stores.city = 'Birmingham'
GROUP BY movies.title;
