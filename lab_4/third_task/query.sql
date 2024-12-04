SELECT * from Songs
ORDER BY  year desc
LIMIT 92;

SELECT SUM(duration_ms), MIN(duration_ms), MAX(duration_ms), AVG(duration_ms)
from Songs;

SELECT  genre, COUNT(*) AS cnt
FROM Songs
GROUP BY genre
ORDER BY cnt desc;

SELECT * FROM Songs
WHERE genre == 'pop'
ORDER BY year desc
LIMIT 97;
