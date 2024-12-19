import pandas as pd
import os
import json
from matplotlib import pyplot as plt
import seaborn as sns


def calc_column(col_item, total_mem, dtypes):
    name_col = col_item[0]
    col_mem = col_item[1]
    share = col_mem/total_mem
    type_col = dtypes[name_col]
    return {'name_col': name_col, 'col_mem': int(col_mem), 'share': float(share), 'type_col': str(type_col)}

# https://www.kaggle.com/datasets/ankurnapa/brewery-operations-and-market-analysis-dataset
df = pd.read_csv('data/brewery_data_complete_extended.csv')

file_info = os.stat('data/brewery_data_complete_extended.csv')
file_size = file_info.st_size
print( f" Объем памяти, который файл занимает на диске:   {file_size / 1024 /1024} МБ")

memory_usage = df.memory_usage(index=False, deep=True)
total = int(memory_usage.sum())
print( f" Объем памяти, который файл занимает в памяти:   {total / 1024 / 1024} МБ")

result = list(map(lambda item: calc_column(item, total, df.dtypes), memory_usage.items()))

result.sort(key=lambda x: x['col_mem'])
json_object = json.dumps(result, indent=4)
with open('task_result_without_optimisation.json', 'w') as outfile:
    outfile.write(json_object)


object_cols = df.select_dtypes(include='object')
all_count = object_cols.count(axis='rows')
unique_count = object_cols.nunique(axis='rows')
result = unique_count / all_count
columns_transform = list(result.loc[result < 0.5].index)
df[columns_transform].astype('category', copy=False)


int_cols = df.select_dtypes(include='int')
int_col_names = list(int_cols.columns)
for col in int_col_names:
    df[col] = pd.to_numeric(df[col], downcast='signed', errors='coerce')

float_cols = df.select_dtypes(include='float')
float_col_names = list(float_cols.columns)
for col in float_col_names:
    df[col] = pd.to_numeric(df[col], downcast='float', errors='coerce')


memory_usage_2 = df.memory_usage(index=False, deep=True)
total_2 = int(memory_usage_2.sum())
print( f" Объем памяти, который файл занимает в памяти:   {total_2 / 1024 / 1024} МБ")

result_2 = list(map(lambda item: calc_column(item, total_2, df.dtypes), memory_usage.items()))

result_2.sort(key=lambda x: x['col_mem'])
json_object_2 = json.dumps(result_2, indent=4)
with open('task_result_with_optimisation.json', 'w') as outfile:
    outfile.write(json_object_2)



# need_columns = ['SKU', 'Location', 'Beer_Style', 'Fermentation_Time', 'Color', 'Volume_Produced', 'Bitterness', 'Total_Sales', 'Quality_Score', 'Alcohol_Content']
# types_need_columns = df[need_columns].dtypes.to_dict()
# path_optimize = "data_optimize.csv"
# header = True
# for ch in pd.read_csv('data/brewery_data_complete_extended.csv', dtype=types_need_columns, usecols=need_columns, chunksize=10000):
#     ch.to_csv(path_optimize, mode='a', header=header, index=False)
#     header = False

main_df = pd.read_csv('data_optimize.csv')

plt.figure(figsize=(10, 10))
sns.heatmap(main_df.corr(numeric_only=True))
plt.savefig('first_chart.png')
plt.show()

plt.figure(figsize=(10, 10))
sns.boxplot(data=main_df)
plt.savefig('second_chart.png')

plt.figure(figsize=(10, 10))
main_df['Beer_Style'].value_counts().sort_values(ascending=False).plot(kind='pie', subplots=True, autopct='%.2f%%')
plt.savefig('third_chart.png')

plt.figure(figsize=(10, 10))
main_df['Location'].value_counts().sort_values(ascending=False).plot(kind='bar')
plt.savefig('fourth_chart.png')


plt.figure(figsize=(20, 7))
main_df.groupby('Beer_Style')['Total_Sales'].mean().plot(legend=True)
plt.savefig('fifth_chart.png')


