
import json
import requests
from typing import List,Dict, Tuple
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points
from math import radians, cos, sin, asin, sqrt, degrees, atan2,pi
from time import time

#downloading lists from websites and parsing them into python code

url = "https://jsonplaceholder.typicode.com/posts"
posts_from_web = requests.get(url)
posts_as_list = json.loads(posts_from_web.content.decode())

url2 = "https://jsonplaceholder.typicode.com/users"
users_from_web = requests.get(url2)
users_as_list = json.loads(users_from_web.content.decode())

for dct in users_as_list: #adding a new pair: key and value to each dictionary in list of users
    dct.update({"user's_post": []})

for dct in users_as_list:
    for another_dct in posts_as_list:
        if dct["id"] == another_dct["userId"]:            #now in each user we have a list of posts they have recently added
            dct["user's_post"].append(another_dct)


def how_many() -> List[str]: #how many posts have been written by each user
    list_of_posts_by_each_user = []
    for dct in users_as_list:
        counter = 0
        for post in dct["user's_post"]:
            counter+=1
        each_post = "{} added {} posts".format(dct["name"],counter)
        list_of_posts_by_each_user.append(each_post)

    return list_of_posts_by_each_user


def check_for_unique_titles() -> List[str]: # chech if titles are unique, if not return titles which repeat in posts
    helpful_dict = {}
    list_of_not_unique_titles = []
    for dct in users_as_list:
        for another_dct in dct["user's_post"]:
            for title in another_dct["title"]:
                if title in helpful_dict:
                    list_of_not_unique_titles.append(title)
                    break
                else:
                    helpful_dict["title"] = title
    return list_of_not_unique_titles


def get_latitude_and_longitude() -> Dict[int,List[float]]: #get dict that maps: user's ID: [lat,lng], by that it will be easier to get into
    dct_of_lat_long_by_each_user = {x: [] for x in range(1,11)}
    for dct in users_as_list:
        for place in dct["address"].keys():
            if place=="geo":
                for value in dct["address"][place].values():
                    dct_of_lat_long_by_each_user[dct["id"]].append(float(value)) #values are string type so we need to convert them to float type
    return dct_of_lat_long_by_each_user


dct = get_latitude_and_longitude()


def who_is_theclosest(id: int, dct: Dict[int,List[float]],time_sum: float ) -> Tuple[int,float]:
    time1 = time()
    orig_point = Point(dct[id][0],dct[id][1])
    lst_of_destinations = []
    point_to_array = []
    for i in range(1,len(dct.keys())+1):
        if i == id: continue
        lst_of_destinations.append(Point(dct[i][0],dct[i][1]))
    destinations = MultiPoint(lst_of_destinations)
    nearest_user_lat_and_lng = nearest_points(orig_point,destinations)
    point_to_array.append(nearest_user_lat_and_lng[1].x)
    point_to_array.append(nearest_user_lat_and_lng[1].y)
    for id in dct.keys():
        if dct[id] == point_to_array:
            time2 = time()
            time_diff = time2 - time1
            time_sum += time_diff

            return id,time_sum


"""
Below I implemented function which calculates distances in km for each user passing as arguments user's ID
and dictionary: id: List[Floats]. I wanted to check which solution is more efficient, the first one using 
shapley library or the second using simple iteration over each user and calculating.
"""

def deg2rad(deg):
  return deg * (pi/180)

def getdistance(id: int, dct: Dict[int,List[float]],time_sum: float) -> Tuple[int,float]:
    time1 = time()
    lat1 = dct[id][0]
    lon1 = dct[id][1]
    dict_of_distances = {} # id: distance, we will be able to get the closest user's ID
    for key in range(1,len(dct.keys())+1):
        if id == key: continue
        lat2 = dct[key][0]
        lon2 = dct[key][1]
        r = 6371 # Earth's radius in KM
        dlat = deg2rad(lat2-lat1)
        dlon = deg2rad(lon2-lon1)
        a = sin(dlat/2) * sin(dlat/2) + cos(deg2rad(lat1)) * cos(deg2rad(lat2)) * sin(dlon/2) * sin(dlon/2)
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        d = r * c
        dict_of_distances[key] = d

    users_id  = min(dict_of_distances,key = dict_of_distances.get) #getting minimum user's ID from dict
    time2 = time()
    time_diff = time2 - time1
    time_sum += time_diff
    return users_id, time_sum


def get_time_from_each_solution(id: int) -> Tuple[float,float]:
    i = 0
    end_time = 0
    end_time2 = 0
    while i < 30000:
        if not i:
            end_time = who_is_theclosest(id, dct, i)
            end_time2 = getdistance(id, dct, i)
            i += 1
        else:
            end_time = who_is_theclosest(id, dct, end_time[1])
            end_time2 = getdistance(id, dct, end_time2[1])
            i += 1


    return end_time, end_time2






