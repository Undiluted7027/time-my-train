import train_timetable
import get_trains, routes
import time, json
from datetime import datetime

def find_trains(from_code=745, to_code=249, via = 4885,dates = 1):
    trains_all = [] # stores all train numbers
    if dates: # find for today
        stations = routes.create_route(from_code, to_code, via)
        print(stations)
        #trains_bw_stns = {}
        for i in range(len(stations)-1): # len(stations)-1
            for j in range(i+1, len(stations)): # len(stations)
                train_numbers = get_trains.train_bw_stn_ry(stations[i], stations[j]) # gets trains between stations from railyatri
                trains_all.extend(train_numbers)
                print(f"{stations[i]}_{stations[j]}")
                #trains_bw_stns[f"{stations[i]}_{stations[j]}"] = train_numbers 
                
        trains_all = list(set(trains_all)) # creates a unique list of train numbers to save processing bandwidth
        #print(json.dumps(trains_bw_stns, indent = 3))

        for k in trains_all: # for creating csv files of train timetables
            # print(k)
            train_timetable.get_timetable(k)

        return trains_all


def trains_near_me(train_lst, nearest_stn_code, time): # for finding trains around railway station
    time = datetime.strptime(time, "%H:%M")
    data = train_timetable.get_timetable(train_lst, time, nearest_stn_code)
    print(data[0])

trains = find_trains(664, 452)
trains_near_me(trains, "GZB", "19:45")
