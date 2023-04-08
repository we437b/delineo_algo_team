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
        self.current_people = deque(temp_queue)
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

    def send_person(self, person, poi_dict):
        #print(self.same_day_brands)
        instate_sum = 0
        next_poi_count = 1 #bc outstate is already a part of next poi list
        outstate_sum = 0
        outstate_count = 0
        home_constant = 2
        next_poi_list = []

        for brand_name in self.same_day_brands.keys():
            if brand_name in poi_dict.keys():
                instate_sum += self.same_day_brands[brand_name]
                next_poi_count += 1
                next_poi_list.append(brand_name)
            else:
                outstate_sum += self.same_day_brands[brand_name]
                outstate_count += 1

        outstate_avg = outstate_sum / outstate_count 
        next_poi_sum = outstate_avg + instate_sum
        home_weight = next_poi_sum / next_poi_count
        home_weight_modified = home_weight / home_constant
        

        next_poi_list.append("out of state")
        next_poi_list.append("home")

        #next_poi_list = ['Dollar General', 'out of state', 'home']
        #final total sum
        next_poi_sum += home_weight_modified
        next_poi_weights = []
        for brand_name in next_poi_list:
            if brand_name in poi_dict.keys():
                next_poi_weights.append(self.same_day_brands[brand_name] / next_poi_sum)
            else:
                continue
        
        next_poi_weights.append(outstate_avg / next_poi_sum)
        next_poi_weights.append(home_weight_modified / next_poi_sum) 
       

        next_poi = random.choices(next_poi_list, weights=next_poi_weights)[0]

        # print(instate_sum)
        # print(outstate_count)
        # print(outstate_sum)
        # print(next_poi_count)
        # print(next_poi_sum)
        # print(home_weight_modified)
        print(next_poi_list)
        print(next_poi_weights)
        print(next_poi)
        
        return [person, next_poi]
        

    #def move_time_step():

    #def toString? 

def timestep(poi_dict):
    '''
        Calculates Each Timestep
    '''
    #print("timestep 1 result")
    # for poi in poi_dict.keys():
    #     print(poi)
        


def get_info(city_info):

    poi_dict = {}

    for poi_name in city_info:
        visit = city_info[poi_name]['raw_visit_counts']
        bucket = city_info[poi_name]['bucketed_dwell_times']
        same_day = city_info[poi_name]['related_same_day_brand']
        pop_hr = city_info[poi_name]['popularity_by_hour']
        pop_day = city_info[poi_name]['popularity_by_day']

        cur_poi = POI(poi_name, visit, bucket, same_day, pop_hr, pop_day)
        poi_dict[poi_name] = cur_poi

    return poi_dict


def simulation(settings, city_info):

    poi_dict = get_info(city_info)
    a = poi_dict["American Heritage Bank"]
    a.send_person(None, poi_dict)
    #poi all set

    #TODO delete, test code

    # for i in range(10):
    #     timestep(poi_dict)

if __name__=="__main__":

    print("main function loading")

    with open('simul_settings.yaml', mode="r") as settingstream:
        settings = yaml.full_load(settingstream)

    with open('barnsdall.yaml') as citystream:
        city_info = yaml.full_load(citystream)
    
    simulation(settings, city_info)



    