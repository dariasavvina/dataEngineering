import pickle
import pandas as pd
import json
import msgpack
import os

with open('data.csv', mode='r', encoding='utf-8') as f:
    df = pd.read_csv(f)

new_df = df.drop(['VIN (1-10)', 'Postal Code', 'Clean Alternative Fuel Vehicle (CAFV) Eligibility', 'Base MSRP',
                  'Legislative District', 'DOL Vehicle ID', 'Vehicle Location', 'Electric Utility',
                  '2020 Census Tract'], axis=1)

min_model_year = int(new_df['Model Year'].min())
max_model_year = int(new_df['Model Year'].max())
mean_model_year = float(new_df['Model Year'].mean())
sum_model_year = int(new_df['Model Year'].sum())
std_model_year = float(new_df['Model Year'].std())

min_electric_range = int(new_df['Electric Range'].min())
max_electric_range = int(new_df['Electric Range'].max())
mean_electric_range = float(new_df['Electric Range'].mean())
sum_electric_range = int(new_df['Electric Range'].sum())
std_electric_range = float(new_df['Electric Range'].std())

freq_country = new_df['County'].value_counts().to_dict()
freq_city = new_df['City'].value_counts().to_dict()
freq_state = new_df['State'].value_counts().to_dict()
freq_make = new_df['Make'].value_counts().to_dict()
freq_model = new_df['Model'].value_counts().to_dict()
freq_electric_vehicle_type = new_df['Electric Vehicle Type'].value_counts().to_dict()

result = {
    'min_model_year': min_model_year,
    'max_model_year': max_model_year,
    'mean_model_year': mean_model_year,
    'sum_model_year': sum_model_year,
    'std_model_year': std_model_year,
    'min_electric_range': min_electric_range,
    'max_electric_range': max_electric_range,
    'mean_electric_range': mean_electric_range,
    'sum_electric_range': sum_electric_range,
    'std_electric_range': std_electric_range,
    'freq_country': freq_country,
    'freq_city': freq_city,
    'freq_state': freq_state,
    'freq_make': freq_make,
    'freq_model': freq_model,
    'freq_electric_vehicle_type': freq_electric_vehicle_type
}

json_object = json.dumps(result, indent=4)

with open('fifth_task_result.json', 'w') as outfile:
    outfile.write(json_object)

with open('fifth_task_data_results.csv', mode='w', encoding='utf-8') as res_f:
    res_f.write(new_df.to_csv())

json_result = new_df.to_json()
# json_object_data = json.dumps(json_result, indent=4)

with open('fifth_task_result_data.json', 'w') as outfile:
    outfile.write(json_result)

with open('fifth_task_data_result.msgpack', mode='wb') as outfile:
    packed = msgpack.packb(json_result, use_bin_type=True)
    outfile.write(packed)

new_df.to_pickle('fifth_task_result_data.pkl')

# with open('fifth_task_result_data.pkl', mode='wb') as f:
#     new_df.to_pickle(outfile)
#     pickle.dump(json_result, f)

file_info_csv = os.stat('fifth_task_data_results.csv')
file_info_json = os.stat('fifth_task_result_data.json')
file_size_csv = file_info_csv.st_size
file_size_json = file_info_json.st_size

file_info_msgpack = os.stat('fifth_task_data_result.msgpack')
file_size_msgpack = file_info_msgpack.st_size

file_info_pickle = os.stat('fifth_task_result_data.pkl')
file_size_pickle = file_info_pickle.st_size

print(
    f" Разница между файлом fifth_task_result_data.json и fifth_task_data_results.csv {file_size_json - file_size_csv} байт")
print(
    f" Разница между файлом fifth_task_data_result.msgpack и fifth_task_result_data.json {file_size_msgpack - file_size_json} байт")
print(
    f" Разница между файлом fifth_task_data_result.msgpack и fifth_task_result_data.pkl {file_size_msgpack - file_size_pickle} байт")
print(
    f" Разница между файлом fifth_task_data_results.csv и fifth_task_result_data.pkl {file_size_csv - file_size_pickle} байт")