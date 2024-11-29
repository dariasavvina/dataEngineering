import pandas as pd
from bs4 import BeautifulSoup
import os
import json
import re



def transform_html_to_object(html: str)-> object:
    soup = BeautifulSoup(html, "html.parser")
    type_tag = soup.select(".chess-wrapper div:first-child span")[0].get_text()
    type = type_tag.split(":")[-1].strip()
    name_tag = soup.select("h1.title")[0].get_text()
    name = name_tag.split(":")[-1].strip()
    city_tag = soup.select(".address-p")[0].get_text()
    city = city_tag.split(":")[1].strip().replace('Начало', '').rstrip()
    date = city_tag.split(":")[2].strip()
    count_tag = soup.select("span.count")[0].get_text()
    count = count_tag.split(":")[1].strip()
    time_tag = soup.select("span.year")[0].get_text()
    time = re.sub(r'[^0-9]*', '', time_tag.split(":")[1]).strip()
    min_rating_tag = soup.select(".chess-wrapper div:nth-child(3) span:last-child")[0].get_text()
    min_rating = min_rating_tag.split(":")[1].strip()
    rating_tag = soup.select(".chess-wrapper div:last-child span:first-child")[0].get_text()
    rating = rating_tag.split(":")[1].strip()
    views_tag = soup.select(".chess-wrapper div:last-child span:last-child")[0].get_text()
    views = views_tag.split(":")[1].strip()
    return {
        "type": type,
        "name": name,
        "city": city,
        "date": date,
        "count_round": int(count),
        "time_round": int(time),
        "min_rating": int(min_rating),
        "rating": float(rating),
        "views": int(views)
    }

lists = []

files = list(os.walk('data/1'))[0][2]

for name_file in files:
    path_file = 'data/1/' + name_file
    with open(path_file, 'r', encoding='utf-8') as f:
        data = f.read()
    data_object = transform_html_to_object(data)
    lists.append(data_object)

json_object = json.dumps(lists, indent=4, ensure_ascii=False)

with open('first_task_result.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


df = pd.DataFrame(lists)
sort = df.sort_values(by=['countRound'], ascending=False)
filtered_df  = df[df['type'] !='Olympic']
sum_views = df['views'].sum()
mean_views = df['views'].mean()
min_views = df['views'].min()
max_views = df['views'].max()
freq_type = df['type'].value_counts().to_dict()

result_obj = {
    "sum_views": int(sum_views),
    "mean_views": float(mean_views),
    "min_views": int(min_views),
    "max_views": int(max_views),
    "freq_type": freq_type
}

sort_json = sort.to_json(orient='records', force_ascii=False)
with open('first_task_sorted_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(sort_json)

filtered_json = filtered_df.to_json(orient='records', force_ascii=False)
with open('first_task_filtered_result.json', 'w', encoding='utf-8') as outfile:
    outfile.write(filtered_json)


json_stat_object = json.dumps(result_obj, indent=4, ensure_ascii=False)

with open('first_task_result_stat.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json_stat_object)