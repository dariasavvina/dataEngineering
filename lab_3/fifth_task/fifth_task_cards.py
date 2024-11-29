from bs4 import BeautifulSoup
import re
import os
import pandas as pd
import json
import itertools

def transform_html_to_object_cards(html) -> object:
    soup = BeautifulSoup(html, "html.parser")
    name_selector = "sd-product-intro h1"
    price_selector = 'span[aria-label="Product price"]'
    bonus_selector = 'sd-bonus-widget div span.amount'
    name = soup.select_one(name_selector).get_text()
    price = int(re.sub(r'[^0-9]*', '', soup.select_one(price_selector).get_text()))
    bonus = int(soup.select_one(bonus_selector).get_text())

    sel = 'li.feature'
    features = soup.select(sel)
    features_by_name = {s.select_one('.name').get_text().strip(): s.select_one('.value').get_text().strip() for s in features}
    color = features_by_name['Цвет']
    high = float(features_by_name['Высота излива']) if 'Высота излива' in features_by_name else None
    assignment = features_by_name['Назначение']
    country = features_by_name['Страна бренда']
    return {
        "name": name,
        "price": price,
        "bonus": bonus,
        "color": color,
        "high": high,
        "assignment": assignment,
        "country": country
    }

lists = []

files = list(os.walk('data/cards'))[0][2]

for name_file in files:
    path_file = 'data/cards/' + name_file
    with open(path_file, 'r', encoding='utf-8') as f:
        data = f.read()
    data_object = transform_html_to_object_cards(data)
    lists.append(data_object)

json_object = json.dumps(lists, indent=4, ensure_ascii=False)

with open('fifth_task_result_cards.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


df = pd.DataFrame(lists)
sort = df.sort_values(by=['price'], ascending=False)
filtered_df  = df[df['color'] !='Хром']
sum_high = df['high'].sum()
mean_high = df['high'].mean()
min_high = df['high'].min()
max_high = df['high'].max()
freq_country = df['country'].value_counts().to_dict()

result_obj = {
    "sum_high": int(sum_high),
    "mean_high": float(mean_high),
    "min_high": int(min_high),
    "max_high": int(max_high),
    "freq_country": freq_country
}

sort_json = sort.to_json(orient='records', force_ascii=False)
with open('fifth_task_sorted_result_cards.json', 'w', encoding='utf-8') as outfile:
    outfile.write(sort_json)

filtered_json = filtered_df.to_json(orient='records', force_ascii=False)
with open('fifth_task_filtered_result_cards.json', 'w', encoding='utf-8') as outfile:
    outfile.write(filtered_json)


json_stat_object = json.dumps(result_obj, indent=4, ensure_ascii=False)

with open('fifth_task_result_stat_cards.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json_stat_object)
