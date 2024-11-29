
import itertools
import pandas as pd
from bs4 import BeautifulSoup
import os
import json
import re


def transform_html_to_object(soup) -> object:
    id = soup.select('.add-to-favorite')[0]['data-id']
    name_tag = soup.select('.product-item span')[0].get_text()
    name = name_tag.strip().replace('"', '')
    price_tag = soup.select('price')[0].get_text()
    price = re.sub(r'[^0-9]*', '', price_tag.strip())
    bonus_tag = soup.select('strong')[0].get_text()
    bonus = re.sub(r'[^0-9]*', '', bonus_tag.strip())
    proc_search_result = soup.select('li[type="processor"]')
    proc_tag = proc_search_result[0].get_text() if len(proc_search_result) > 0 else None
    num_cores = int(proc_tag.split('x')[0].strip()) if proc_tag is not None else None
    freq = float(re.sub(r'[^0-9.]*', '', proc_tag.split('x')[1].strip())) if proc_tag is not None else None
    ram_search_result = soup.select('li[type="ram"]')
    ram_tag = ram_search_result[0].get_text() if len(ram_search_result) > 0 else None
    ram = int(re.sub(r'[^0-9]*', '', ram_tag.strip())) if ram_tag is not None else None
    sim_search_result = soup.select('li[type="sim"]')
    sim_tag = sim_search_result[0].get_text() if len(sim_search_result) > 0 else None
    sim = int(re.sub(r'[^0-9]*', '', sim_tag.strip())) if sim_tag is not None else None
    matrix_search_result = soup.select('li[type="matrix"]')
    matrix_tag = matrix_search_result[0].get_text() if len(matrix_search_result) > 0 else None
    matrix = matrix_tag.strip() if matrix_tag is not None else None
    resolution_search_result = soup.select('li[type="resolution"]')
    resolution_tag = resolution_search_result[0].get_text() if len(resolution_search_result) > 0 else None
    resolution = resolution_tag.strip() if resolution_tag is not None else None
    camera_search_result = soup.select('li[type="camera"]')
    camera_tag = camera_search_result[0].get_text() if len(camera_search_result) > 0 else None
    camera = int(re.sub(r'[^0-9]*', '', camera_tag.strip())) if camera_tag is not None else None
    acc_search_result = soup.select('li[type="acc"]')
    acc_tag = acc_search_result[0].get_text() if len(acc_search_result) > 0 else None
    acc = int(re.sub(r'[^0-9]*', '', acc_tag.strip())) if acc_tag is not None else None
    return {
        "product_id": int(id),
        "name": name,
        "price": int(price),
        "bonus": int(bonus),
        "ram": ram,
        "resolution": resolution,
        "acc": acc,
        "matrix": matrix,
        "camera": camera,
        "num_cores": num_cores,
        "freq": freq,
        "sim": sim,
    }


def transform_list_object(html):
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.select('div.product-item')
    list_of_object = list(map(transform_html_to_object, tags))
    return list_of_object


files = list(os.walk('data/2'))[0][2]
file_contents = []
for name_file in files:
    path_file = 'data/2/' + name_file
    with open(path_file, 'r', encoding='utf-8') as f:
        data = f.read()
    file_contents.append(data)

result = list(itertools.chain.from_iterable(map(transform_list_object, file_contents)))

json_object = json.dumps(result, indent=4, ensure_ascii=False)

with open('second_task_result.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)

df = pd.DataFrame(result)

sort = df.sort_values(by=['camera'], ascending=False, axis=0)
filtered_df  = df[df['matrix'] !='OLED']
sum_bonus = df['bonus'].sum()
mean_bonus = df['bonus'].mean()
min_bonus = df['bonus'].min()
max_bonus = df['bonus'].max()
freq_sim = df['sim'].value_counts().to_dict()

result_obj = {
    "sum_bonus": int(sum_bonus),
    "mean_bonus": float(mean_bonus),
    "min_bonus": int(min_bonus),
    "max_bonus": int(max_bonus),
    "freq_sim": freq_sim
}

sort_json = sort.to_json(orient='records', force_ascii=False, indent=4)
with open('second_task_sorted_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(sort_json)

filtered_json = filtered_df.to_json(orient='records', force_ascii=False, indent=4)
with open('second_task_filtered_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(filtered_json)


json_stat_object = json.dumps(result_obj, indent=4, ensure_ascii=False)

with open('second_task_result_stat.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json_stat_object)