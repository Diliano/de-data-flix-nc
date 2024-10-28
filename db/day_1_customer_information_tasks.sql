\c nc_flix

-- Create an output to display the information on our customers
-- It should include name, location, loyalty membership status
-- - 'doesn't even go here' - 0 points
-- - 'bronze status' - < 10 points
-- - 'silver status' - 10 - 100 points
-- - 'gold status' - > 100 points
-- We can assume if the customer has no point information, they have yet to receive any loyalty points.

SELECT customer_name, location, COALESCE(loyalty_points, 0),
    CASE 
        WHEN loyalty_points > 100 THEN 'gold status'
        WHEN loyalty_points >= 10 THEN 'silver status'
        WHEN loyalty_points > 0 THEN 'bronze status'
    ELSE 
        'doesn''t even go here'
    END AS loyalty_membership_status
FROM customers;

-- We want more information on our customers: name, age, location, loyalty points
-- We would also like to order them by location, and then within their location groups, order by number of loyalty points, high to low.

SELECT customer_name, date_of_birth, location, COALESCE(loyalty_points, 0) AS loyalty_points,
    RANK() OVER (
        PARTITION BY location
        ORDER BY COALESCE(loyalty_points, 0) DESC
    )
FROM customers;