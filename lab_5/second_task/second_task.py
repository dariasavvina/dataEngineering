import json

import pandas as pd
import msgpack
from pymongo import MongoClient

with open('data/task_2_item.msgpack', 'rb') as file:
    data_bytes = file.read()
    data = msgpack.unpackb(data_bytes)
    df_2 = pd.DataFrame(data)

client = MongoClient("localhost", 27017)
db = client["test-database"]
collection = db["jobs"]
result_dict = df_2.to_dict(orient='records')

# collection.insert_many(result_dict)


def agg_salary():
    agg = collection.aggregate([
        {
            "$group": {
                "_id": None,
                "minSalary": {"$min": "$salary"},
                "maxSalary": {"$max": "$salary"},
                "avgSalary": {"$avg": "$salary"}
            }
        },
        {
            "$unset": [
                "_id"
            ]
        }
    ])

    result = agg.next()
    json_object = json.dumps(result, indent=4, ensure_ascii=False)
    with open('second_task_first_query.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def count_job():
    agg = collection.aggregate([
        {
            "$group": {
                "_id": "$job",
                "job_count": {"$count": {}}
            }
        }
    ])
    result = list(map(lambda item: item, agg))
    json_object = json.dumps(result, indent=4, ensure_ascii=False)
    with open('second_task_second_query.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def salary_agg_city():
    agg = collection.aggregate([
        {
            "$group": {
                "_id": "$city",
                "minSalary": {"$min": "$salary"},
                "maxSalary": {"$max": "$salary"},
                "avgSalary": {"$avg": "$salary"}
            }
        }
    ])
    result = list(map(lambda item: item, agg))
    json_object = json.dumps(result, indent=4, ensure_ascii=False)
    with open('second_task_third_query.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def salary_agg_profession():
    agg = collection.aggregate([
        {
            "$group": {
                "_id": "$job",
                "minSalary": {"$min": "$salary"},
                "maxSalary": {"$max": "$salary"},
                "avgSalary": {"$avg": "$salary"}
            }
        }
    ])
    result = list(map(lambda item: item, agg))
    json_object = json.dumps(result, indent=4, ensure_ascii=False)
    with open('second_task_fourth_query.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def age_agg_city():
    agg = collection.aggregate([
        {
            "$group": {
                "_id": "$city",
                "minAge": {"$min": "$age"},
                "maxAge": {"$max": "$age"},
                "avgAge": {"$avg": "$age"}
            }
        }
    ])
    result = list(map(lambda item: item, agg))
    json_object = json.dumps(result, indent=4, ensure_ascii=False)
    with open('second_task_fifth_query.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def age_agg_profession():
    agg = collection.aggregate([
        {
            "$group": {
                "_id": "$job",
                "minAge": {"$min": "$age"},
                "maxAge": {"$max": "$age"},
                "avgAge": {"$avg": "$age"}
            }
        }
    ])
    result = list(map(lambda item: item, agg))
    json_object = json.dumps(result, indent=4, ensure_ascii=False)
    with open('second_task_sixth_query.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def max_salary_min_age():
    agg = collection.aggregate([
        {
            "$sort": {"age": 1}
        },
        {
            "$sort": {"salary": -1}
        }
    ])
    result = agg.next()
    salary = result['salary']
    json_t = {"salary": salary}
    json_object = json.dumps(json_t, indent=4, ensure_ascii=False)
    with open('second_task_7_query.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def min_salary_max_age():
    agg = collection.aggregate([
        {
            "$sort": {"age": -1}
        },
        {
            "$sort": {"salary": 1}
        }
    ])
    result = agg.next()
    salary = result['salary']
    json_t = {"salary": salary}
    json_object = json.dumps(json_t, indent=4, ensure_ascii=False)
    with open('second_task_8_query.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def salary_match_agg_sort():
    agg = collection.aggregate([
        {
            "$match": {
                "salary": {
                    "$gt": 50000
                }
            }
        },
        {
            "$group": {
                "_id": "$city",
                "minAge": {"$min": "$age"},
                "maxAge": {"$max": "$age"},
                "avgAge": {"$avg": "$age"}
            }
        },
        {
            "$sort": {"avgAge": -1}
        }
    ])
    result = list(map(lambda item: item, agg))
    json_object = json.dumps(result, indent=4, ensure_ascii=False)
    with open('second_task_9_query.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def salary_match_agg_sort_city_profession_age():
    agg = collection.aggregate([
        {
            "$match": {
                "$and": [
                    {"city": "Фигерас"},
                    {"job": "Строитель"},
                    {"$or": [
                        {"age": {"$gt": 18, "$lt": 25}},
                        {"age": {"$gt": 50, "$lt": 65}}
                    ]}
                ]
            }
        },
        {
            "$group": {
                "_id": None,
                "minSalary": {"$min": "$salary"},
                "maxSalary": {"$max": "$salary"},
                "avgSalary": {"$avg": "$salary"}
            }
        },
        {
            "$unset": [
                "_id"
            ]
        }
    ])
    result = list(map(lambda item: item, agg))
    json_object = json.dumps(result, indent=4, ensure_ascii=False)
    with open('second_task_10_query.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def random_query():
    agg = collection.aggregate([
        {
            "$match": {
                "age": {
                    "$gt": 25
                }
            }
        },
        {
            "$group": {
                "_id": "$job",
                "minYear": {"$min": "$year"},
                "maxYear": {"$max": "$year"},
                "avgYear": {"$avg": "$year"}
            }
        },
        {
            "$sort": {"avgYear": 1}
        }
    ])
    result = list(map(lambda item: item, agg))
    json_object = json.dumps(result, indent=4, ensure_ascii=False)
    with open('second_task_11_query.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


min_salary_max_age()
