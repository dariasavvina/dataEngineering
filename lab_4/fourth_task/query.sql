SELECT name, category, fromCity FROM Products
ORDER BY update_counter desc
LIMIT 10;

SELECT SUM(price), MIN(price), MAX(price), AVG(price), category from Products
GROUP BY category
ORDER BY price desc;

SELECT SUM(quantity), MIN(quantity), MAX(quantity), AVG(quantity), category from Products
GROUP BY category
ORDER BY quantity desc;

SELECT isAvailable, category, name FROM Products;