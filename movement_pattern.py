from household import Household
from collections import deque

class POI(Household):

    def __init__(self): # time_step field?
        super().__init__() # 이거 할 필요가 없나?
        self.current_people = deque()
        self.bucketed_dwell_time = {}
        self.same_day_brands = []

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