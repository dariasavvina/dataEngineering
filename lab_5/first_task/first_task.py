import json
import pandas as pd
from pymongo import MongoClient


def transform_str_to_object(string: str) -> object:
    cleaned_input_str = string.strip()
    split_string = cleaned_input_str.split('\n')
    job_str = split_string[0]
    job = job_str.split('::')[1]
    salary_str = split_string[1]
    salary = salary_str.split('::')[1]
    id_str = split_string[2]
    id = id_str.split('::')[1]
    city_str = split_string[3]
    city = city_str.split('::')[1]
    year_str = split_string[4]
    year = year_str.split('::')[1]
    age_str = split_string[5]
    age = age_str.split('::')[1]
    return {
        "job": job,
        "salary": int(salary),
        "id": id,
        "city": city,
        "year": int(year),
        "age": int(age)
    }


def transform_list_object(string):
    cleaned_input_str = string.strip()
    lists = list(filter(lambda s: len(s) > 0, cleaned_input_str.split('=====')))
    list_of_object = list(map(transform_str_to_object, lists))
    # print(list_of_object)
    return list_of_object



with open('data/task_1_item.text', 'r', encoding='utf-8') as f:
    data = f.read()
    transformed_data = transform_list_object(data)


client = MongoClient("localhost", 27017)
db = client["test-database"]
collection = db["jobs"]
collection.insert_many(transformed_data)

def find_10_desc_salary():
     elem = collection.find({}, {"_id": 0}).limit(10).sort({"salary": -1})
     lst = []
     for i in elem:
         lst.append(i)
     json_object = json.dumps(lst, indent=4, ensure_ascii=False)
     with open('first_task_first_query.json', 'w', encoding='utf-8') as outfile:
         outfile.write(json_object)


def find_15_age_desc_salary():
    elem = collection.find({ "age": { "$lt": "30" } }, {"_id": 0}).limit(15).sort({"salary": -1})
    lst = []
    for i in elem:
        lst.append(i)
    json_object = json.dumps(lst, indent=4, ensure_ascii=False)
    with open('first_task_second_query.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def find_age_and_year_and_salary():
    or_f = {"$or":[{"salary" :{ "$gt": "50000", "$lte": "75000"}}, { "salary" : {"$gt": "125000", "$lt": "150000"}}]}
    and_f = {"$and": [{ "age":{ "$gt": "20", "$lt" : "30"}},  {"year": { "$gte": "2019", "$lte": "2022"}}]}
    all_f = { "$and": [or_f, and_f]}
    elem = collection.find(all_f, {"_id": 0})
    lst = []
    for i in elem:
        lst.append(i)
    json_object = json.dumps(lst, indent=4, ensure_ascii=False)
    with open('first_task_third_query.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)



def find_city_and_profession_desc_age():
    elem = collection.find({"$and": [{"city": "Фигерас"}, {"job": {"$in": ["Строитель", "Водитель", "Архитектор"]}}]}, {"_id": 0}).limit(10).sort({"age": 1})
    lst = []
    for i in elem:
        lst.append(i)
    json_object = json.dumps(lst, indent=4, ensure_ascii=False)
    with open('first_task_fourth_query.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)

find_10_desc_salary()
find_age_and_year_and_salary()
find_15_age_desc_salary()
find_city_and_profession_desc_age()