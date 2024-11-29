from bs4 import BeautifulSoup
import re
import os
import pandas as pd
import json
import itertools

def transform_html_to_object_catalog(soup) -> object:
    name_selector = "a.product-name"
    price_selector = 'span[aria-label="Product price"]'
    bonus_selector = 'sd-bonus-widget div span.amount'
    code_selector = ".code-value"
    name = soup.select_one(name_selector).get_text()
    price = int(re.sub(r'[^0-9]*', '',soup.select_one(price_selector).get_text().strip()))
    bonusTag = soup.select_one(bonus_selector)
    bonus = int(bonusTag.get_text()) if bonusTag is not None else None
    code = int(soup.select_one(code_selector).get_text())
    return {
        "name": name,
        "price": price,
        "bonus": bonus,
        "code": code
    }

def transform_list_object(html):
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.select('sd-product-grid-item')
    list_of_object = list(map(transform_html_to_object_catalog, tags))
    return list_of_object

files = list(os.walk('data/catalog'))[0][2]
file_contents = []
for name_file in files:
    path_file = 'data/catalog/' + name_file
    with open(path_file, 'r', encoding='utf-8') as f:
        data = f.read()
    file_contents.append(data)

result = list(itertools.chain.from_iterable(map(transform_list_object, file_contents)))

json_object = json.dumps(result, indent=4, ensure_ascii=False)

with open('fifth_task_result_catalog.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


df = pd.DataFrame(result)
sort = df.sort_values(by=['price'], ascending=False)
filtered_df  = df[df['bonus'] > 200]
sum_price = df['price'].sum()
mean_price = df['price'].mean()
min_price = df['price'].min()
max_price = df['price'].max()
freq_name = df['name'].value_counts().to_dict()

result_obj = {
    "sum_price": int(sum_price),
    "mean_price": float(mean_price),
    "min_price": int(min_price),
    "max_price": int(max_price),
    "freq_name": freq_name
}

sort_json = sort.to_json(orient='records', force_ascii=False)
with open('fifth_task_sorted_result_catalog.json', 'w', encoding='utf-8') as outfile:
    outfile.write(sort_json)

filtered_json = filtered_df.to_json(orient='records', force_ascii=False)
with open('fifth_task_filtered_result_catalog.json', 'w', encoding='utf-8') as outfile:
    outfile.write(filtered_json)


json_stat_object = json.dumps(result_obj, indent=4, ensure_ascii=False)

with open('fifth_task_result_stat_catalog.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json_stat_object)