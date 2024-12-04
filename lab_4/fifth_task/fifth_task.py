import pandas as pd
import sqlite3

df_drivers = pd.read_csv('data/drivers.csv')
df_races = pd.read_csv('data/races.csv')
df_results = pd.read_csv('data/results.csv')


def init_table_drivers():
    with sqlite3.connect('data_formula_1.db', autocommit=True) as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Drivers  (
            driverId INTEGER,
            driverRef VARCHAR,
            number VARCHAR,
            code VARCHAR,
            forename VARCHAR,
            surname VARCHAR,
            dob VARCHAR,
            nationality VARCHAR,
            url VARCHAR)
        ''')

def fill_table_drivers():
    with sqlite3.connect('data_formula_1.db', autocommit=True) as conn:
        df_drivers.to_sql(name='Drivers', con=conn, if_exists='append', index=False)


def init_table_races():
    with sqlite3.connect('data_formula_1.db', autocommit=True) as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Races (
            raceId INTEGER,
            year INTEGER,
            round INTEGER,
            circuitId INTEGER,
            name VARCHAR,
            date DATE,
            time VARCHAR,
            url VARCHAR,
            fp1_date VARCHAR,
            fp1_time VARCHAR,
            fp2_date VARCHAR,
            fp2_time VARCHAR,
            fp3_date VARCHAR,
            fp3_time VARCHAR,
            quali_date VARCHAR,
            quali_time VARCHAR,
            sprint_date VARCHAR,
            sprint_time VARCHAR
            )
        ''')


def fill_table_races():
    with sqlite3.connect('data_formula_1.db', autocommit=True) as conn:
        df_races.to_sql(name='Races', con=conn, if_exists='append', index=False)


def init_table_results():
    with sqlite3.connect('data_formula_1.db', autocommit=True) as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Results  (
            resultId INTEGER,
            raceId INTEGER,
            driverId INTEGER,
            constructorId INTEGER,
            number INTEGER,
            grid INTEGER,
            position VARCHAR,
            positionText VARCHAR,
            positionOrder VARCHAR,
            points VARCHAR,
            laps VARCHAR,
            time VARCHAR,
            milliseconds VARCHAR,
            fastestLap VARCHAR,
            rank INTEGER,
            fastestLapTime VARCHAR,
            fastestLapSpeed VARCHAR,
            statusId VARCHAR)
        ''')


def fill_table_results():
    with sqlite3.connect('data_formula_1.db', autocommit=True) as conn:
        df_results.to_sql(name='Results', con=conn, if_exists='append', index=False)


# init_table_drivers()
# fill_table_drivers()
# init_table_races()
# fill_table_races()
# init_table_results()
# fill_table_results()

with sqlite3.connect('data_formula_1.db', autocommit=True) as conn:
    first_query = '''
    SELECT Results.*, Drivers.driverRef, Drivers.number as driver_number, Drivers.forename, Drivers.surname FROM Results
    JOIN Drivers  on Results.driverId = Drivers.driverId
    WHERE Drivers.forename = 'David' and Drivers.surname = 'Coulthard';
    '''
    second_query = '''
    SELECT * FROM Races
    WHERE round < 10
    ORDER BY year desc
    LIMIT 50;
    '''
    third_query = '''
    SELECT COUNT(name = 'Australian Grand Prix') FROM Races;
    '''
    fourth_query = '''
    SELECT position, Drivers.forename, Drivers.surname FROM Results
    JOIN Drivers  on Results.driverId = Drivers.driverId
    JOIN Races  on Results.raceId = Races.raceId
    WHERE Races.year = 2017
    LIMIT 100;
    '''
    fifth_query = '''
    SELECT MIN(round) as min_round, MAX(round) as max_round, AVG(round) as avg_round
    FROM Races;
    '''
    sixth_query = '''
    SELECT points, laps, Races.name FROM Results
    JOIN Races  on Results.raceId = Races.raceId
    WHERE Races.year > 2016
    LIMIT 100;
    '''

    first_df = pd.read_sql(first_query, conn)
    second_df = pd.read_sql(second_query, conn)
    third_df = pd.read_sql(third_query, conn)
    fourth_df = pd.read_sql(fourth_query, conn)
    fifth_df = pd.read_sql(fifth_query, conn)
    sixth_df = pd.read_sql(sixth_query, conn)

first_json = first_df.to_json(orient='records', force_ascii=False, indent=4)
with open('fifth_task_result_query_1.json', 'w', encoding='utf-8') as outfile:
    outfile.write(first_json)

second_json = second_df.to_json(orient='records', force_ascii=False, indent=4)
with open('fifth_task_result_query_2.json', 'w', encoding='utf-8') as outfile:
    outfile.write(second_json)

third_json = third_df.to_json(orient='records', force_ascii=False, indent=4)
with open('fifth_task_result_query_3.json', 'w', encoding='utf-8') as outfile:
    outfile.write(third_json)

fourth_json = fourth_df.to_json(orient='records', force_ascii=False, indent=4)
with open('fifth_task_result_query_4.json', 'w', encoding='utf-8') as outfile:
    outfile.write(fourth_json)

fifth_json = fifth_df.to_json(orient='records', force_ascii=False, indent=4)
with open('fifth_task_result_query_5.json', 'w', encoding='utf-8') as outfile:
    outfile.write(fifth_json)

sixth_json = sixth_df.to_json(orient='records', force_ascii=False, indent=4)
with open('fifth_task_result_query_6.json', 'w', encoding='utf-8') as outfile:
    outfile.write(sixth_json)