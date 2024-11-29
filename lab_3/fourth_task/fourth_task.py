from bs4 import BeautifulSoup
import re
import os
import pandas as pd
import json
import itertools

def transform_xml_to_object(soup)-> object:
    id =  soup.find_all('id')[0].get_text().strip()
    name = soup.find_all('name')[0].get_text().strip()
    category = soup.find_all('category')[0].get_text().strip()
    size = soup.find_all('size')[0].get_text().strip()
    color = soup.find_all('color')[0].get_text().strip()
    material = soup.find_all('material')[0].get_text().strip()
    price = soup.find_all('price')[0].get_text().strip()
    rating = soup.find_all('rating')[0].get_text().strip()
    reviews = soup.find_all('reviews')[0].get_text().strip()
    exclusive_tag = soup.find_all('exclusive')
    exclusive = exclusive_tag[0].get_text().strip() if len(exclusive_tag) > 0 else None
    sporty_tag = soup.find_all('sporty')
    sporty = sporty_tag[0].get_text().strip() if len(sporty_tag) > 0  else None
    new_tag = soup.find_all('new')
    new = new_tag[0].get_text().strip() if len(new_tag) > 0 else None
    return {
        'id': int(id),
        'name': name,
        'category': category,
        'size': size,
        'color': color,
        'material': material,
        'price': int(price),
        'rating': float(rating),
        'reviews': int(reviews),
        'exclusive': exclusive,
        'sporty': sporty,
        'new': new
    }


def transform_list_object(xml):
    soup = BeautifulSoup(xml, "xml")
    tags = soup.find_all('clothing')
    list_of_object = list(map(transform_xml_to_object, tags))
    return list_of_object

files = list(os.walk('data/4'))[0][2]
file_contents = []
for name_file in files:
    path_file = 'data/4/' + name_file
    with open(path_file, 'r', encoding='utf-8') as f:
        data = f.read()
    file_contents.append(data)

result = list(itertools.chain.from_iterable(map(transform_list_object, file_contents)))

json_object = json.dumps(result, indent=4, ensure_ascii=False)

with open('fourth_task_result.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)

df = pd.DataFrame(result)

sort = df.sort_values(by=['rating'], ascending=False, axis=0)
filtered_df  = df[df['category'] !='Skirt']
sum_reviews = df['reviews'].sum()
mean_reviews = df['reviews'].mean()
min_reviews = df['reviews'].min()
max_reviews = df['reviews'].max()
freq_category = df['category'].value_counts().to_dict()

result_obj = {
    "sum_reviews": int(sum_reviews),
    "mean_reviews": float(mean_reviews),
    "min_reviews": int(min_reviews),
    "max_reviews": int(max_reviews),
    "freq_category": freq_category
}

sort_json = sort.to_json(orient='records', force_ascii=False, indent=4)
with open('fourth_task_sorted_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(sort_json)

filtered_json = filtered_df.to_json(orient='records', force_ascii=False, indent=4)
with open('fourth_task_filtered_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(filtered_json)


json_stat_object = json.dumps(result_obj, indent=4, ensure_ascii=False)

with open('fourth_task_result_stat.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json_stat_object)

