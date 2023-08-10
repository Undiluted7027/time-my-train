import imp
from logging import raiseExceptions
import requests
import pandas as pd
from datetime import datetime, timedelta
from routes import create_csv
from bs4 import BeautifulSoup

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def get_timetable(t_lst, val, stn_code=None):
    trains_near, trains_not_near = [], []
    for train_num in t_lst:
        link = f"https://www.railmitra.com/train-schedule/{train_num}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36" 
        }
        req = requests.get(link, headers=headers)
        soup = BeautifulSoup(req.content, "lxml")
        train_schedule_table_code = soup.find("div", {"id": "trainSchedule"})
        rows = train_schedule_table_code.find_all("td")
        row_dat = [i.text for i in rows]
        arrival = row_dat[row_dat.index(stn_code)+1]
        departure = row_dat[row_dat.index(stn_code)+3]
        #print(arrival, departure)
        #val = datetime.strptime(val, "%H:%M")
        if arrival != "First" or departure != "Last":
            arrival, departure = arrival.replace(".", ":"), departure.replace(".", ":")
            arrival, departure = datetime.strptime(arrival, "%H:%M"), datetime.strptime(departure, "%H:%M")
            start, end = arrival - timedelta(minutes=2), departure + timedelta(minutes=2)
            if time_in_range(start, end, val):
                print(datetime.strftime(arrival, "%H:%M"), train_num)
                trains_near.append((train_num, arrival, departure))
            else:
                print("Train isn't around this station during specified time")
                trains_not_near.append((train_num, arrival, departure))
        else:
            print("Train either originates or terminates at this station")

    return trains_near, trains_not_near
    #create_csv(train_schedule_table_code, train_num)

#get_timetable('04419', "05:18","PWL")



def train_timings(train_num, stn_code, time):
    df = pd.read_csv(f"{train_num}.csv")
    #df.reset_index(drop=True, inplace=True)
    val = df.loc[df['CODE'] == stn_code, 'ARRIVAL'].values[0]
    if val != "First" or val != "Last":
        val = val.replace(".", ":")
        val = datetime.strptime(val, "%H:%M")
        start = time - timedelta(minutes=30)
        end = time + timedelta(minutes=30)
        if time_in_range(start, end, val):
            print(datetime.strftime(val, "%H:%M"), train_num)
        else:
            raiseExceptions("Invalid Time")
    else:
        print("Train either originates or terminates at this station")
