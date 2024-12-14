import json

import pandas as pd
from pymongo import MongoClient

df = pd.read_csv('data/task_3_item.csv',sep=';')


client = MongoClient("localhost", 27017)
db = client["test-database"]
collection = db["jobs"]
result_dict = df.to_dict(orient='records')
# collection.insert_many(result_dict)

def delete_predicate():
    collection.delete_many({"$or":[{"salary" :{ "$gt": 25000}}, { "salary" : { "$lt": "175000"}}]})

def update_age():
    collection.update_many({},  {"$inc": {"age": 1}})

def update_salary_profession():
    collection.update_many({"$or":[{"job" :"Строитель"}, { "job" : "Водитель"}]}, {"$mul": {"salary": 1.05}})

def update_salary_city():
    collection.update_many({"$or": [{"city": "Фигерас"}, {"city": "Душанбе"}]}, {"$mul": {"salary": 1.07}})

def update_salary_city_profession_age():
    collection.update_many({"$and": [{"$and": [{"city": "Москва"}, {"age": {"$gt": 10}}]}, {"job": "Инженер"}]}, {"$mul": {"salary": 1.1}})

def delete_random_predicate():
    collection.delete_many({"$and":[{"year" :{ "$gt": 2001}}, { "city" : "Прага"}]})



element = collection.find( {}, {"_id": 0})
lst = []
for i in element:
    lst.append(i)
json_object = json.dumps(lst, indent=4, ensure_ascii=False)
with open('third_task_after_update_queries.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json_object)