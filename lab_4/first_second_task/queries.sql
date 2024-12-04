SELECT * from Championships
ORDER BY  min_rating desc
LIMIT 92;

SELECT SUM(tours_count), MIN(tours_count), MAX(tours_count), AVG(tours_count)
from Championships;



SELECT  system, COUNT(*) AS cnt
FROM Championships
GROUP BY system
ORDER BY cnt desc;

SELECT * FROM Championships
WHERE system == 'circular'
ORDER BY time_on_game desc;

SELECT  Championships.name, Championships.id, C.place   FROM Championships
LEFT JOIN Championships_place C on Championships.name = C.name;

SELECT  Championships.name  FROM Championships
JOIN Championships_place C on Championships.name = C.name
ORDER BY C.prise desc
LIMIT 10;

SELECT  Championships.name, Championships.city   FROM Championships
JOIN Championships_place C on Championships.name = C.name
WHERE C.place == 2;




