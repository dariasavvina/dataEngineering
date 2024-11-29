from bs4 import BeautifulSoup
import re
import os
import pandas as pd
import json

def transform_xml_to_object(xml: str)-> object:
    soup = BeautifulSoup(xml, "xml")
    name = soup.find_all('name')[0].get_text().strip()
    constellation = soup.find_all('constellation')[0].get_text().strip()
    spectral_class = soup.find_all('spectral-class')[0].get_text().strip()
    radius = soup.find_all('radius')[0].get_text().strip()
    rotation = re.sub(r'[^0-9.]*', '', soup.find_all('rotation')[0].get_text()).strip()
    age = re.sub(r'[^0-9.]*', '', soup.find_all('age')[0].get_text()).strip()
    distance = re.sub(r'[^0-9.]*', '', soup.find_all('distance')[0].get_text()).strip()
    absolute_magnitude = re.sub(r'[^0-9.]*', '', soup.find_all('absolute-magnitude')[0].get_text()).strip()
    return {
        "name": name,
        "constellation": constellation,
        "spectral-class": spectral_class,
        "radius": int(radius),
        "rotation": float(rotation),
        "age": float(age),
        "distance": float(distance),
        "absolute-magnitude": float(absolute_magnitude)
    }


lists = []

files = list(os.walk('3/'))[0][2]

for name_file in files:
    path_file = '3/' + name_file
    with open(path_file, 'r', encoding='utf-8') as f:
        data = f.read()
    data_object = transform_xml_to_object(data)
    lists.append(data_object)

json_object = json.dumps(lists, indent=4, ensure_ascii=False)

with open('third_task_result.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


df = pd.DataFrame(lists)
sort = df.sort_values(by=['age'], ascending=False)
filtered_df  = df[df['constellation'] !='Скорпион']
sum_radius = df['radius'].sum()
mean_radius = df['radius'].mean()
min_radius = df['radius'].min()
max_radius = df['radius'].max()
freq_spectral_class = df['spectral-class'].value_counts().to_dict()

result_obj = {
    "sum_radius": int(sum_radius),
    "mean_radius": float(mean_radius),
    "min_radius": int(min_radius),
    "max_radius": int(max_radius),
    "freq_spectral_class": freq_spectral_class
}

sort_json = sort.to_json(orient='records', force_ascii=False, indent=4)
with open('third_task_sorted_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(sort_json)

filtered_json = filtered_df.to_json(orient='records', force_ascii=False, indent=4)
with open('third_task_filtered_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(filtered_json)


json_stat_object = json.dumps(result_obj, indent=4, ensure_ascii=False)

with open('third_task_result_stat.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json_stat_object)