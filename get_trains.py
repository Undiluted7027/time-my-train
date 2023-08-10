from train_timetable import train_timings, time_in_range
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import routes, re, requests, time
import pandas as pd


def get_station_code_num(stn_code_word):
    df = pd.read_csv("stations.csv")
    s_names, s_name_nums = df['S_Code'].to_list(), df['S_No'].to_list()
    stn_code_num = s_name_nums[s_names.index(stn_code_word)]
    print(stn_code_num)
    return stn_code_num

def setup():
    '''Sets up selenium for chrome'''
    options = Options()
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    driver = webdriver.Chrome(chrome_options=
    options,executable_path= r'C:\reqs\chromedriver_win32\chromedriver.exe')
    return driver

def get_arrivals_departures(s_code_num):
    i = 1
    link = f"https://indiarailinfo.com/departures/745/1?i=1&date=undefined&stptype=0&&kkk=1654527360810"
    req = requests.get(link,
    headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"
    })
    soup = BeautifulSoup(req.content, "lxml")
    element = soup.find_all("div", attrs={"style": "line-height:20px;"})
    trains = []
    for i in element:
        children = i.findChildren("div" , recursive=False)
        print(children[1].text)
        

def start_browser(iteration = 0, trigger=False):
    code = get_station_code_num("GWL")
    driver = setup()
    url = f"https://indiarailinfo.com/departures/{740}/"
    driver.get(url)
    trains = []
    while True:
        try:
            driver.find_element_by_class_name("nextbtn").click()
            time.sleep(5)
            
        except NoSuchElementException:
            html = driver.page_source
            soup = BeautifulSoup(html)
            element = soup.find_all("div", attrs={"style": "line-height:20px;"})
            for i in element:
                children = i.findChildren("div" , recursive=False)
                trains.append([children[0].text, children[1].text,children[7].text])
                #print(f"{children[0].text}, {children[1].text}")
            break
    #print(trains)
    timing = datetime.strptime("19:05", "%H:%M")
    start, end = timing - timedelta(minutes=10), timing + timedelta(minutes=10)
    for j in range(len(trains)):
        trains[j][2] = datetime.strptime(trains[j][2], "%H:%M")
        if time_in_range(start, end, trains[j][2]):
            print(trains[j][0], trains[j][1], trains[j][2])


code = get_station_code_num("PWL")
get_arrivals_departures(code)

start_browser()