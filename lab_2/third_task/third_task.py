import pandas as pd
import json
import msgpack
import os

with open('third_task.json', mode='r', encoding='utf-8') as f:
    df = pd.read_json(f)

min_price = df.groupby(['name'])['price'].min().rename('min_price')
max_price = df.groupby(['name'])['price'].max().rename('max_price')
mean_price = df.groupby(['name'])['price'].mean().rename('mean_price')

total_df = pd.concat([min_price, max_price, mean_price], axis=1)

output_dict = total_df.to_dict('index')
output_json = json.dumps(output_dict, indent=4, ensure_ascii=False)

with open('third_task_result.json', mode='w', encoding='utf-8') as outfile:
    outfile.write(output_json)

with open('third_task_result.msgpack', mode='wb') as outfile:
   packed = msgpack.packb(output_dict)
   outfile.write(packed)

file_info_json = os.stat('third_task_result.json')
file_info_msgpack = os.stat('third_task_result.msgpack')
file_size_json = file_info_json.st_size
file_size_msgpack = file_info_msgpack.st_size

print(f" Разница между файлом third_task_result.json и third_task_result.msgpack {file_size_json - file_size_msgpack} байт")