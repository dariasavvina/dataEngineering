import pickle
import json

with open('fourth_task_updates.json', mode='r', encoding='utf-8') as f:
    updates = json.load(f)

updates_dict = {item['name']: item for item in updates}

def update_price(product):
    new_price = product['price']
    if product['name'] in updates_dict:
        update = updates_dict[product['name']]
        if update['method'] == 'add':
            new_price = add(product['price'], update['param'])
        if update['method'] == 'sub':
            new_price = sub(product['price'], update['param'])
        if update['method'] == 'percent+':
            new_price = add_percent(product['price'], update['param'])
        if update['method'] == 'percent-':
            new_price = sub_percent(product['price'], update['param'])
    return {'name': product['name'], 'price': new_price, 'quantity': product['quantity'], 'category': product['category']}


def add(price: float, param: float) -> float:
    new_price = price + param
    return new_price

def sub(price: float, param: float) -> float:
    new_price = price - param
    return new_price

def add_percent(price: float, param: float) -> float:
    new_price = price + (price * param)
    return new_price

def sub_percent(price: float, param: float) -> float:
    new_price = price - (price * param)
    return new_price

with open('fourth_task_products.json', mode='rb') as f:
    products = pickle.load(f)


new_products = list(map(update_price, products))

with open('fourth_task_result.pkl', mode='wb') as f:
    pickle.dump(new_products, f)

