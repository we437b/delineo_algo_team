from collections import deque
import numpy as np
import pandas as pd
import yaml
from household import Household, Person, Population


class POI(Household):

    def __init__(self, visit, bucket, same_day, pop_hr, pop_day): # time_step field?
        super().__init__() # 이거 할 필요가 없나?
        self.current_people = deque()
        self.visit = visit
        self.bucketed_dwell_time = bucket
        self.same_day_brands = same_day
        self.pop_hr = pop_hr
        self.pop_day = pop_day

    def add_person(self, person):
        self.current_people.append(person)

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

    for poi_name in city_info:
        visit = city_info[poi_name]['visit']
        cur_poi = POI(visit, bucket, same_day, pop_hr, pop_day)

if __name__=="__main__":
    print("main function loading")


    with open('simul_settings.yaml', mode="r") as settingstream:
        settings = yaml.full_load(settingstream)

    with open('barnsdall.yaml') as citystream:
        city_info = yaml.full_load(citystream)
    
    simulation(settings, city_info)
    