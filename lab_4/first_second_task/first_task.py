import sqlite3
import pandas as pd


def init_table_championships():
    with sqlite3.connect('data.db', autocommit=True) as conn:
        cur = conn.cursor()
        cur.execute('''
    CREATE TABLE IF NOT EXISTS Championships  (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    city VARCHAR,
    begin DATE,
    system VARCHAR,
    tours_count INTEGER,
    min_rating INTEGER,
    time_on_game INTEGER )
        
        ''')


def fill_table_championships(items):
    with sqlite3.connect('data.db', autocommit=True) as conn:
        cur = conn.cursor()
        cur.executemany("INSERT INTO Championships VALUES(?, ?, ?, ?, ?, ?, ?, ? )", items)


def transform_str_to_object(string: str) -> object:
    cleaned_input_str = string.strip()
    split_string = cleaned_input_str.split('\n')
    id_str = split_string[0]
    id = id_str.split('::')[1]
    name_str = split_string[1]
    name = name_str.split('::')[1]
    city_str = split_string[2]
    city = city_str.split('::')[1]
    begin_str = split_string[3]
    begin = begin_str.split('::')[1]
    system_str = split_string[4]
    system = system_str.split('::')[1]
    tours_count_str = split_string[5]
    tours_count = tours_count_str.split('::')[1]
    min_rating_str = split_string[6]
    min_rating = min_rating_str.split('::')[1]
    time_on_game_str = split_string[7]
    time_on_game = time_on_game_str.split('::')[1]
    return {
        "id": id,
        "name": name,
        "city": city,
        "begin": begin,
        "system": system,
        "tours_count": tours_count,
        "min_rating": min_rating,
        "time_on_game": time_on_game
    }


def transform_list_object(string):
    cleaned_input_str = string.strip()
    lists = list(filter(lambda s: len(s) > 0, cleaned_input_str.split('=====')))
    list_of_object = list(map(transform_str_to_object, lists))
    return list_of_object


def transform_list_object_to_tuple(list_of_object):
    return list(map(lambda item: tuple(item.values()), list_of_object))


# with open('data/item.text', 'r', encoding='utf-8') as f:
#     data = f.read()
#     transformed_data = transform_list_object(data)

# init_table_championships()
# data_tuple = transform_list_object_to_tuple(transformed_data)
# fill_table_championships(data_tuple)


with sqlite3.connect('data.db', autocommit=True) as conn:
    first_query = '''
    SELECT * from Championships
    ORDER BY  min_rating desc
    LIMIT 92;
    '''
    second_query = '''
    SELECT SUM(tours_count) as sum_tours_count, MIN(tours_count) as min_tours_count, MAX(tours_count) as max_tours_count, AVG(tours_count) as avg_tours_count
    from Championships;
    '''
    third_query = '''
    SELECT  system, COUNT(*) AS cnt
    FROM Championships
    GROUP BY system
    ORDER BY cnt desc;
    '''
    fourth_query = '''
    SELECT * FROM Championships
    WHERE system == 'circular'
    ORDER BY time_on_game desc;
    '''
    first_df = pd.read_sql(first_query, conn)
    second_df = pd.read_sql(second_query, conn).iloc[0]
    third_df = pd.read_sql(third_query, conn)
    fourth_df = pd.read_sql(fourth_query, conn)

sort_json = first_df.to_json(orient='records', force_ascii=False, indent=4)
with open('first_task_sorted_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(sort_json)

aggr_json = second_df.to_json(force_ascii=False, indent=4)
with open('first_task_aggregation_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(aggr_json)

freq_json = third_df.to_json(orient='records', force_ascii=False, indent=4)
with open('first_task_freq_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(freq_json)

filtered_json = fourth_df.to_json(orient='records', force_ascii=False, indent=4)
with open('first_task_filtered_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(filtered_json)
