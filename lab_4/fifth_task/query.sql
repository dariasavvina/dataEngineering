SELECT * FROM Results
JOIN Drivers  on Results.driverId = Drivers.driverId
WHERE Drivers.forename = 'David' and Drivers.surname = 'Coulthard';

SELECT * FROM Races
WHERE round < 10
ORDER BY year desc
LIMIT 50;

SELECT COUNT(name = 'Australian Grand Prix') FROM Races;

SELECT position, Drivers.forename, Drivers.surname FROM Results
JOIN Drivers  on Results.driverId = Drivers.driverId
JOIN Races  on Results.raceId = Races.raceId
WHERE Races.year = 2017
LIMIT 100;

SELECT MIN(round) as min_round, MAX(round) as max_round, AVG(round) as avg_round
FROM Races;

SELECT points, laps, Races.name FROM Results
JOIN Races  on Results.raceId = Races.raceId
WHERE Races.year > 2016
LIMIT 100;





