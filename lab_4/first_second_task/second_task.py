import sqlite3
import pandas as pd


def init_table_championships_place():
    with sqlite3.connect('data.db', autocommit=True) as conn:
        cur = conn.cursor()
        cur.execute('''
    CREATE TABLE IF NOT EXISTS Championships_place  (
    name VARCHAR,
    place INTEGER,
    prise INTEGER )
        ''')


def fill_table_championships_place(items):
    with sqlite3.connect('data.db', autocommit=True) as conn:
        cur = conn.cursor()
        cur.executemany("INSERT INTO Championships_place VALUES(?, ?, ?)", items)

def transform_str_to_object(string: str) -> object:
    cleaned_input_str = string.strip()
    split_string = cleaned_input_str.split('\n')
    name_str = split_string[0]
    name = name_str.split('::')[1]
    place_str = split_string[1]
    place = place_str.split('::')[1]
    prise_str = split_string[2]
    prise = prise_str.split('::')[1]
    return {
        "name": name,
        "place": place,
        "prise": prise
    }

def transform_list_object(string):
    cleaned_input_str = string.strip()
    lists = list(filter(lambda s: len(s) > 0, cleaned_input_str.split('=====')))
    list_of_object = list(map(transform_str_to_object, lists))
    print(list_of_object)
    return list_of_object

# with open('data/subitem.text', 'r', encoding='utf-8') as f:
#     data = f.read()
#     transformed_data = transform_list_object(data)


def transform_list_object_to_tuple(list_of_object):
    return list(map(lambda item: tuple(item.values()), list_of_object))

#init_table_championships_place()
#data_tuple = transform_list_object_to_tuple(transformed_data)
#fill_table_championships_place(data_tuple)

with sqlite3.connect('data.db', autocommit=True) as conn:
    first_query = '''
    SELECT  Championships.name, Championships.id, C.place   FROM Championships
    LEFT JOIN Championships_place C on Championships.name = C.name;
    '''
    second_query = '''
    SELECT  Championships.name  FROM Championships
    JOIN Championships_place C on Championships.name = C.name
    ORDER BY C.prise desc
    LIMIT 10;
    '''
    third_query = '''
    SELECT  Championships.name, Championships.city   FROM Championships
    JOIN Championships_place C on Championships.name = C.name
    WHERE C.place == 2;
    '''

    first_df = pd.read_sql(first_query, conn)
    second_df = pd.read_sql(second_query, conn)
    third_df = pd.read_sql(third_query, conn)

first_json = first_df.to_json(orient='records', force_ascii=False, indent=4)
with open('second_task_first_query_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(first_json)

second_json = second_df.to_json(force_ascii=False, indent=4)
with open('second_task_second_query_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(second_json)

third_json = third_df.to_json(orient='records', force_ascii=False, indent=4)
with open('second_task_third_query_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(third_json)
