import json
import pandas as pd
from pymongo import MongoClient

df_1 = pd.read_csv('data/club_games.csv')

df_2 = pd.read_json('data/clubs.json')

main_df = df_1.join(df_2.set_index('club_id'), on='club_id', how='left').drop(columns=['url', 'filename', 'coach_name', 'club_code', 'total_market_value'])

client = MongoClient("localhost", 27017)
db = client["test-database"]
collection = db["clubs"]
result_dict = main_df.to_dict(orient='records')


collection.insert_many(result_dict)


def find_age():
    elem = collection.find({"average_age": {"$gte": 20}}, {"_id": 0}).limit(20)
    lst = []
    for i in elem:
        lst.append(i)
    json_object = json.dumps(lst, indent=4, ensure_ascii=False)
    with open('fourth_task_first_query_sampling.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def find_stadion_name():
    elem = collection.find({"stadium_name": "Tottenham Hotspur Stadium"}, {"_id": 0})
    lst = []
    for i in elem:
        lst.append(i)
    json_object = json.dumps(lst, indent=4, ensure_ascii=False)
    with open('fourth_task_second_query_sampling.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def find_hosting():
    elem = collection.find({"hosting": "Home"}, {"_id": 0}).limit(10).sort("club_id", 1)
    lst = []
    for i in elem:
        lst.append(i)
    json_object = json.dumps(lst, indent=4, ensure_ascii=False)
    with open('fourth_task_third_query_sampling.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def find_game_id():
    elem = collection.find({"game_id": 2246637}, {"_id": 0}).sort("club_id", -1)
    lst = []
    for i in elem:
        lst.append(i)
    json_object = json.dumps(lst, indent=4, ensure_ascii=False)
    with open('fourth_task_fourth_query_sampling.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def find_domestic_competition_id():
    elem = collection.find({"domestic_competition_id": "GR1"}, {"_id": 0}).limit(20)
    lst = []
    for i in elem:
        lst.append(i)
    json_object = json.dumps(lst, indent=4, ensure_ascii=False)
    with open('fourth_task_fifth_query_sampling.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def update_one_club_id():
    collection.update_one({"club_id": 2079}, {"$set": {"club_id": 2078}})


def update_many_opponent_id():
    collection.update_many({"opponent_id": 1091}, {"$set": {"opponent_id": 1092}})


def delete_one_club_id():
    collection.delete_one({"club_id": 11194})


def delete_one_opponent_id():
    collection.delete_one({"club_id": 11194, "opponent_manager_name": "Andy Preece"})


def delete_opponent_manager_name():
    collection.delete_many(
        {"$and": [{"opponent_manager_name": "Andy Preece", "game_id": {"$in": [2583546, 3126556]}}]})

find_age()
find_hosting()
find_game_id()
find_domestic_competition_id()
find_stadion_name()

update_one_club_id()
update_many_opponent_id()
delete_one_club_id()
delete_one_opponent_id()
delete_opponent_manager_name()


elem = collection.find({}, {"_id": 0})
lst = []
for i in elem:
    lst.append(i)
json_object = json.dumps(lst, indent=4, ensure_ascii=False)
with open('fourth_task_after_update_queries.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json_object)


def agg_club_id():
    agg = collection.aggregate([
        {
            "$group": {
                "_id": None,
                "minClubId": {"$min": "$club_id"},
                "maxClubId": {"$max": "$club_id"},
                "avgClubId": {"$avg": "$club_id"}
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
    with open('fourth_task_first_query_aggregation.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def own_goals():
    agg = collection.aggregate([
        {
            "$match": {
                "own_goals": {
                    "$exists": True,
                    "$ne": float('nan')
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "minOwnGoals": {"$min": "$own_goals"},
                "maxOwnGoals": {"$max": "$own_goals"},
                "avgOwnGoals": {"$avg": "$own_goals"}
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
    with open('fourth_task_second_query_aggregation.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def opponent_position_and_manager_name_aggregation():
    agg = collection.aggregate([
        {
            "$match": {
                "$and": [
                    {
                        "opponent_position": {
                            "$exists": True,
                            "$ne": float('nan')
                        }
                    },
                    {
                        "opponent_manager_name": "Rasmus Bertelsen"
                    }
                ]
            }
        },
        {
            "$group": {
                "_id": None,
                "minOpponentPosition": {"$min": "$opponent_position"},
                "maxOpponentPosition": {"$max": "$opponent_position"},
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
    with open('fourth_task_third_query_aggregation.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def agg_stadium_seats():
    agg = collection.aggregate([
        {
            "$match": {
                "stadium_seats": {
                    "$exists": True,
                    "$ne": float('NaN')
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "minStadiumSeats": {"$min": "$stadium_seats"},
                "maxStadiumSeats": {"$max": "$stadium_seats"},
                "avgStadiumSeats": {"$avg": "$stadium_seats"}
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
    with open('fourth_task_fourth_query_aggregation.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)


def agg_last_season():
    agg = collection.aggregate([
        {
            "$match": {
                "last_season": {
                    "$exists": True,
                    "$ne": float('NaN')
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "minLastSeason": {"$min": "$last_season"},
                "maxLastSeason": {"$max": "$last_season"}
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
    with open('fourth_task_fifth_query_aggregation.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)

agg_club_id()
own_goals()
opponent_position_and_manager_name_aggregation()
agg_stadium_seats()
agg_last_season()