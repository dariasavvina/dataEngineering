import pandas as pd
import sqlite3

df = pd.read_json('data/_product_data.json')
print(df)


def init_table_products():
    with sqlite3.connect('data_products.db', autocommit=True) as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Products  (
            name VARCHAR,
            price REAL CHECK ( price > 0 ),
            quantity INTEGER CHECK ( quantity >= 0 ),
            category VARCHAR,
            fromCity VARCHAR,
            isAvailable VARCHAR,
            views INTEGER,
            update_counter INTEGER DEFAULT 0)
        ''')


def fill_table_products():
    with sqlite3.connect('data_products.db', autocommit=True) as conn:
        df.to_sql(name='Products', con=conn, if_exists='append', index=False)


# init_table_products()
# fill_table_products()

def transform_str_to_object(string: str) -> object:
    cleaned_input_str = string.strip()
    split_string = cleaned_input_str.split('\n')
    name_str = split_string[0]
    name = name_str.split('::')[1]
    method_str = split_string[1]
    method = method_str.split('::')[1]
    param_str = split_string[2]
    param = param_str.split('::')[1]
    return {
        "name": name,
        "method": method,
        "param": param
    }


def transform_list_object(string):
    cleaned_input_str = string.strip()
    lists = list(filter(lambda s: len(s) > 0, cleaned_input_str.split('=====')))
    list_of_object = list(map(transform_str_to_object, lists))
    print(list_of_object)
    return list_of_object


with open('data/_update_data.text', 'r', encoding='utf-8') as f:
    data = f.read()
    transformed_data = transform_list_object(data)


def update_products(product):
    param = product['param']
    method = product['method']
    name = product['name']
    if method == 'price_percent':
        price_percent(param, name)
    if method == 'quantity_sub':
        quantity_sub(param, name)
    if method == 'quantity_add':
        quantity_add(param, name)
    if method == 'price_abs':
        price_abs(param, name)
    if method == 'remove':
        remove(name)
    if method == 'available':
        available(param, name)


def price_percent(param, name):
    with sqlite3.connect('data_products.db') as conn:
        try:
            cur = conn.cursor()
            query = '''
            UPDATE Products
            SET price = price + (price * ?), update_counter = update_counter + 1
            WHERE name = ?
            '''
            cur.execute(query, (float(param), name))
            conn.commit()
        except:
            conn.rollback()


def quantity_sub(param, name):
    with sqlite3.connect('data_products.db') as conn:
        try:
            cur = conn.cursor()
            query = '''
            UPDATE Products
            SET quantity = quantity + ?, update_counter = update_counter + 1
            WHERE name = ?
            '''
            cur.execute(query, (int(param), name))
            conn.commit()
        except:
            conn.rollback()


def quantity_add(param, name):
    with sqlite3.connect('data_products.db') as conn:
        try:
            cur = conn.cursor()
            query = '''
            UPDATE Products
            SET quantity = quantity + ?, update_counter = update_counter + 1
            WHERE name = ?;
            '''
            cur.execute(query, (int(param), name))
            conn.commit()
        except:
            conn.rollback()


def price_abs(param, name):
    with sqlite3.connect('data_products.db') as conn:
        try:
            cur = conn.cursor()
            query = '''
                UPDATE Products
                SET price = price + ?, update_counter = update_counter + 1
                WHERE name = ?;
                '''
            cur.execute(query, (float(param), name))
            conn.commit()
        except:
            conn.rollback()


def remove(name):
    with sqlite3.connect('data_products.db') as conn:
        try:
            cur = conn.cursor()
            query = '''
                DELETE FROM Products
                WHERE name = ?;
                '''
            cur.execute(query, name)
            conn.commit()
        except:
            conn.rollback()


def available(param, name):
    with sqlite3.connect('data_products.db') as conn:
        try:
            cur = conn.cursor()
            query = '''
            UPDATE Products
            SET isAvailable = ?, update_counter = update_counter + 1
            WHERE name = ?;
                '''
            cur.execute(query, (bool(param), name))
            conn.commit()
        except:
            conn.rollback()


for product in transformed_data:
    update_products(product)



with sqlite3.connect('data_products.db', autocommit=True) as conn:
    first_query = '''
    SELECT name, category, fromCity FROM Products
    ORDER BY update_counter desc
    LIMIT 10;
    '''
    second_query = '''
    SELECT SUM(price) as sum_price, MIN(price) as min_price, MAX(price) as max_price, AVG(price) as avg_price, category from Products
    GROUP BY category
    ORDER BY price desc;
    '''
    third_query = '''
    SELECT SUM(quantity) as sum_quantity, MIN(quantity) as min_quantity, MAX(quantity) as max_quantity, AVG(quantity) as avg_quantity, category from Products
    GROUP BY category
    ORDER BY quantity desc;
    '''
    fourth_query = '''
    SELECT isAvailable, category, name FROM Products;
    '''
    first_df = pd.read_sql(first_query, conn)
    second_df = pd.read_sql(second_query, conn)
    third_df = pd.read_sql(third_query, conn)
    fourth_df = pd.read_sql(fourth_query, conn)

sort_json = first_df.to_json(orient='records', force_ascii=False, indent=4)
with open('fourth_task_update_10.json', 'w', encoding='utf-8') as outfile:
    outfile.write(sort_json)

aggr_json = second_df.to_json(force_ascii=False, indent=4)
with open('fourth_task_aggregation_price_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(aggr_json)

freq_json = third_df.to_json(orient='records', force_ascii=False, indent=4)
with open('fourth_task_aggregation_quantity_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(freq_json)

filtered_json = fourth_df.to_json(orient='records', force_ascii=False, indent=4)
with open('fourth_task_random_query.json', 'w', encoding='utf-8') as outfile:
    outfile.write(filtered_json)