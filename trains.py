from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests, re, time

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
}

LINK = "https://indiarailinfo.com/"


def setup(link):
    response = requests.get(link, headers=HEADERS)
    if response.status_code == 200:
        htmlcontent = response.text
        return htmlcontent
    else:
        raise "Error getting content from webpage!"


def selenium_setup(link):
    cService = webdriver.ChromeService(executable_path="./chromedriver.exe")
    driver = webdriver.Chrome(service=cService)
    driver.get(link)
    inputElement = driver.find_element(
        By.XPATH,
        '//*[contains(concat( " ", @class, " " ), concat( " ", "stntrnboxright", " " ))]',
    )
    inputElement.send_keys("12919")
    time.sleep(4)
    inputElement.send_keys(Keys.DOWN)
    inputElement.send_keys(Keys.ENTER)
    go_button = driver.find_element(By.XPATH, '//*[(@id = "SrhDiv")]')
    go_button.click()
    time.sleep(7)
    html = driver.page_source
    return html


def find_all_occurrences(value, search):
    occurrences = []
    id = -2
    while id != -1:
        id = value.find(search)
        if id != -1:
            occurrences.append(id)
            occurrences = occurrences[id + len(search) :]
    return occurrences


def get_timetable():
    timetable_html = setup(
        "https://indiarailinfo.com/train/timetable/malwa-sf-express-12919/1048/12254/10091"
    )
    soup = BeautifulSoup(timetable_html, "html.parser")
    all_stations_link = soup.find("h3").a.get("href")
    all_stations_content = setup(LINK + all_stations_link)
    all_stations_soup = BeautifulSoup(all_stations_content, "html.parser")
    all_stations_schedule = all_stations_soup.find(
        "div", class_=re.compile("newschtable.*")
    )
    all_stations_divs = all_stations_schedule.select(
        "div.newbg.inline > div, div.noflex.inline > div, div.avblcal > div"
    )
    data = tuple()
    for i in range(3, len(all_stations_divs)):
        # print(all_stations_divs[i].text)
        sub_divs = (
            all_stations_divs[i]
            .select("div.newbg > div > div, div.noflex > div > div")[4]
            .get("title")
        )
        if sub_divs != " | ":
            crossing_define = "with "
            train_num_len = 5
            crossings = [
                i + len(crossing_define)
                for i in range(len(sub_divs))
                if sub_divs.startswith(crossing_define, i)
            ]
            train_numbers = [sub_divs[i : i + train_num_len] for i in crossings]
            print(train_numbers)

        print(sub_divs)
        break
    print(len(all_stations_divs))


# selenium_setup("https://indiarailinfo.com/")
get_timetable()
