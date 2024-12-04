import msgpack
import pandas as pd
import sqlite3


def init_table_championships():
    with sqlite3.connect('data_songs.db', autocommit=True) as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Songs  (
            artist VARCHAR,
            song VARCHAR,
            duration_ms INTEGER,
            year INTEGER,
            tempo REAL,
            genre VARCHAR,
            energy REAL,
            key REAL,
            loudness REAL,
            mode INTEGER,
            speechiness REAL,
            acousticness REAL,
            instrumentalness REAL)
        ''')


def fill_table_songs():
    with sqlite3.connect('data_songs.db', autocommit=True) as conn:
        main_df.to_sql(name='Songs', con=conn, if_exists='append', index=False)

df_1 = pd.read_csv('data/_part_1.csv',sep=';')

with open ('data/_part_2.msgpack','rb') as file:
    data_bytes = file.read()
    data = msgpack.unpackb(data_bytes)
    df_2 = pd.DataFrame(data)

main_df = pd.concat([df_1,df_2])
print(main_df)

# init_table_championships()
# fill_table_songs()

with sqlite3.connect('data_songs.db', autocommit=True) as conn:
    first_query = '''
    SELECT * from Songs
    ORDER BY  year desc
    LIMIT 92;
    '''
    second_query = '''
    SELECT SUM(duration_ms) as sum_duration_ms, MIN(duration_ms) as min_duration_ms, MAX(duration_ms) as max_duration_ms, AVG(duration_ms) as avg_duration_ms
    from Songs;
    '''
    third_query = '''
    SELECT  genre, COUNT(*) AS cnt
    FROM Songs
    GROUP BY genre
    ORDER BY cnt desc;
    '''
    fourth_query = '''
    SELECT * FROM Songs
    WHERE genre == 'pop'
    ORDER BY year desc
    LIMIT 97;
    '''
    first_df = pd.read_sql(first_query, conn)
    second_df = pd.read_sql(second_query, conn).iloc[0]
    third_df = pd.read_sql(third_query, conn)
    fourth_df = pd.read_sql(fourth_query, conn)

sort_json = first_df.to_json(orient='records', force_ascii=False, indent=4)
with open('third_task_sorted_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(sort_json)

aggr_json = second_df.to_json(force_ascii=False, indent=4)
with open('third_task_aggregation_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(aggr_json)

freq_json = third_df.to_json(orient='records', force_ascii=False, indent=4)
with open('third_task_freq_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(freq_json)

filtered_json = fourth_df.to_json(orient='records', force_ascii=False, indent=4)
with open('third_task_filtered_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(filtered_json)
