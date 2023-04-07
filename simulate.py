from collections import deque
import numpy as np
import pandas as pd
import yaml
import json
from household import Household, Person, Population


class POI():

    def __init__(self, name, visit, bucket, same_day, pop_hr, pop_day): # time_step field?

        bucket = json.loads(bucket)
        self.name = name
        self.current_people = deque()
        self.visit = visit
        self.bucketed_dwell_time = bucket
        self.same_day_brands = same_day
        self.pop_hr = pop_hr
        self.pop_day = pop_day

    def add_person(self): #person):
        keys = self.bucketed_dwell_time

        print(type(keys))
        # self.current_people.append(person)

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
    poi_list[0].add_person()

if __name__=="__main__":
    print("main function loading")


    with open('simul_settings.yaml', mode="r") as settingstream:
        settings = yaml.full_load(settingstream)

    with open('barnsdall.yaml') as citystream:
        city_info = yaml.full_load(citystream)
    
    simulation(settings, city_info)
    