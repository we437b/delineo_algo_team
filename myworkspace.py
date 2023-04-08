from collections import deque
import numpy as np
import pandas as pd
import yaml
import json
import random
from household import Household, Person, Population


class POI():

    def __init__(self, name, visit, bucket, same_day, pop_hr, pop_day): # time_step field?
        bucket = json.loads(bucket)
        self.name = name
        temp_queue = [[] for i in range(500)]
        self.current_people = temp_queue
        self.visit = visit
        self.bucketed_dwell_time = bucket
        self.same_day_brands = same_day
        self.pop_hr = pop_hr
        self.pop_day = pop_day

    def add_person(self):
        values = ["<5", "5-10", "11-20", "21-60", "61-120", "121-240", ">240"]
        sum = self.bucketed_dwell_time["<5"] + self.bucketed_dwell_time["5-10"] + self.bucketed_dwell_time["11-20"] + self.bucketed_dwell_time["21-60"] + self.bucketed_dwell_time["61-120"] + self.bucketed_dwell_time["121-240"] + self.bucketed_dwell_time[">240"]
        weights = [self.bucketed_dwell_time["<5"]/sum, self.bucketed_dwell_time["5-10"]/sum, self.bucketed_dwell_time["11-20"]/sum, self.bucketed_dwell_time["21-60"]/sum, self.bucketed_dwell_time["61-120"]/sum, self.bucketed_dwell_time["121-240"]/sum, self.bucketed_dwell_time[">240"]/sum]


        random_string = random.choices(values, weights=weights)[0]
        if(random_string == "<5"):
            random_integer = random.randint(1, 4)
        elif(random_string == "5-10"):
            random_integer = random.randint(5, 10)
        elif(random_string == "11-20"):
            random_integer = random.randint(11, 20)
        elif(random_string == "21-60"):
            random_integer = random.randint(21, 60)
        elif(random_string == "61-120"):
            random_integer = random.randint(61, 120)
        elif(random_string == "121-240"):
            random_integer = random.randint(121, 240)
        elif(random_string == ">240"):
            random_integer = random.randint(241, 500)

        if random_integer > len(self.current_people):
            self.current_people.append(deque())
        
        else:
            self.current_people[random_integer - 1].append(random_integer)
        
        print(random_string)
        print(random_integer)
        print(self.current_people[random_integer - 1])

        #self.current_people.append(person)

    def send_person(self, target_poi):
        if not self.current_people:
            print("No person available to send.")
            return

        person = self.current_people.popleft()
        target_poi.add_person(person)

    #def move_time_step():

    #def toString? 

def timestep():
    '''
        Calculates Each Timestep
    '''

def simulation(settings, city_info):

    poi_list = []

    for poi_name in city_info:
        visit = city_info[poi_name]['raw_visit_counts']
        bucket = city_info[poi_name]['bucketed_dwell_times']
        same_day = city_info[poi_name]['related_same_day_brand']
        pop_hr = city_info[poi_name]['popularity_by_hour']
        pop_day = city_info[poi_name]['popularity_by_day']

        cur_poi = POI(poi_name, visit, bucket, same_day, pop_hr, pop_day)
        poi_list.append(cur_poi)

    #poi all set

if __name__=="__main__":
    print("main function loading")


    with open('simul_settings.yaml', mode="r") as settingstream:
        settings = yaml.full_load(settingstream)

    with open('barnsdall.yaml') as citystream:
        city_info = yaml.full_load(citystream)
    
    simulation(settings, city_info)
    a = POI("American Heritage Bank", 39, city_info["American Heritage Bank"]["bucketed_dwell_times"], city_info["American Heritage Bank"]["related_same_day_brand"], city_info["American Heritage Bank"]['popularity_by_hour'], city_info["American Heritage Bank"]['popularity_by_day'])
    a.add_person()


    