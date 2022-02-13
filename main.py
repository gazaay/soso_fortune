from fastapi import FastAPI
from pydantic import BaseModel
import json
from datetime import date, timedelta

app = FastAPI()


class Birthday(BaseModel):
    birth_year: int = 1971
    birth_month: int = 6
    birth_day: int = 28


class Birthday_FixDate(BaseModel):
    birth_year: int = 1971
    birth_month: int = 6
    birth_day: int = 28
    fix_year: int = 2022
    fix_month: int = 2
    fix_day: int = 1


with open("reference/reference_data.json") as jsonFile:
    ref_data = json.load(jsonFile)
    jsonFile.close()

today = date.today()
base_year = ref_data["base_date_element"]["start_year"]
base_month = ref_data["base_date_element"]["start_month"]
base_day = 1
date_x = date(base_year, base_month, base_day)

# test date
# today = date(2022,1, 15)


@app.get("/")
async def root():
    # date.timedelta(days=10)
    gap_days = today - date_x
    gap_days_count = gap_days.total_seconds() / (60*60*24)
    gap_cycles = int(gap_days_count / 12)
    gap_cycles_offset = int(gap_days_count % 12)
    return {"message": "Hello World",
            "file data": ref_data["time_element"],
            "today": today, "gap_date": gap_cycles_offset,
            "life_element": ref_data["life_element"],
            "time_element": ref_data["time_element"][gap_cycles_offset]}


@app.post("/my_luck_today")
async def luck_today(birthday: Birthday):
    my_birthday = date(birthday.birth_year,
                       birthday.birth_month, birthday.birth_day)

    gap_days = today - date_x
    gap_days_count = gap_days.total_seconds() / (60*60*24)
    gap_cycles_offset = int(gap_days_count % 12)

    my_life_element = life_element(my_birthday)
    advice_message = "I have no advice for you today. "

    if ref_data["life_element"][my_life_element]["enhance_element"] == ref_data["time_element"][gap_cycles_offset]["main_element"]:
        advice_message = """Congratulations! It will be your lucky day because your life charater is \'{}\'. Your elemental would like to see {} which could enchanced by {}. The date that you picked is {} - In Chinese it is {} and it means it's main element for the day is {}. It will enhance your power.""".format(
                        ref_data["life_element"][my_life_element]["life_element"],
                        ref_data["life_element"][my_life_element]["favour_element"],
                        ref_data["life_element"][my_life_element]["enhance_element"],
                        today, 
                        ref_data["time_element"][gap_cycles_offset]["chinese"],
                        ref_data["time_element"][gap_cycles_offset]["main_element"],
                    )
    return {"message": "Test day's element is",
            "today": today, "gap_date": gap_cycles_offset,
            "time_element": ref_data["time_element"][gap_cycles_offset],
            "my_life_element": ref_data["life_element"][my_life_element],
            "advice": advice_message}


@app.post("/my_luck_fix_day")
async def luck_fix_day(test_day: Birthday_FixDate):
    my_birthday = date(test_day.birth_year,
                       test_day.birth_month, test_day.birth_day)

    test_day = date(test_day.fix_year, test_day.fix_month, test_day.fix_day)
    gap_days = test_day - date_x
    gap_days_count = gap_days.total_seconds() / (60*60*24)
    gap_cycles_offset = int(gap_days_count % 12)

    my_life_element = life_element(my_birthday)
    advice_message = "I have no advice for you today. "

    if ref_data["life_element"][my_life_element]["enhance_element"] == ref_data["time_element"][gap_cycles_offset]["main_element"]:
        advice_message = """Congratulations! It will be your lucky day because your life charater is \'{}\'. Your elemental would like to see {} which could enchanced by {}. The date that you picked is {} - In Chinese it is {} and it means it's main element for the day is {}. It will enhance your power.""".format(
                        ref_data["life_element"][my_life_element]["life_element"],
                        ref_data["life_element"][my_life_element]["favour_element"],
                        ref_data["life_element"][my_life_element]["enhance_element"],
                        test_day, 
                        ref_data["time_element"][gap_cycles_offset]["chinese"],
                        ref_data["time_element"][gap_cycles_offset]["main_element"],
                    )
    return {"message": "Test day's element is",
            "today": today, "gap_date": gap_cycles_offset,
            "time_element": ref_data["time_element"][gap_cycles_offset],
            "my_life_element": ref_data["life_element"][my_life_element],
            "advice": advice_message}


@app.get("/today_element")
async def luck_today():
    gap_days = today - date_x
    gap_days_count = gap_days.total_seconds() / (60*60*24)
    gap_cycles_offset = int(gap_days_count % 12)
    return {"message": "Today's element is",
            "today": today, "gap_offset": gap_cycles_offset,
            "time_element": ref_data["time_element"][gap_cycles_offset]}


@app.post("/my_next_ten_lucky_day")
async def next_ten_lucky_day(birthday: Birthday):
    my_birthday = date(birthday.birth_year,
                       birthday.birth_month, birthday.birth_day)

    test_day = today
    my_lucky_days = []
    while len(my_lucky_days) < 11:
        gap_days = test_day - date_x
        gap_days_count = gap_days.total_seconds() / (60*60*24)
        gap_cycles_offset = int(gap_days_count % 12)

        my_life_element = life_element(my_birthday)
        advice_message = "I have no advice for you. "

        if ref_data["life_element"][my_life_element]["enhance_element"] == ref_data["time_element"][gap_cycles_offset]["main_element"]:
            my_lucky_days.append(test_day)
        test_day += timedelta(days=1)


    return {"message": "Test day's element is",
            "today": today, "gap_date": gap_cycles_offset,
            "time_element": ref_data["time_element"][gap_cycles_offset],
            "my_life_element": ref_data["life_element"][my_life_element],
            "my_lucky_days": my_lucky_days,
            "advice": advice_message}



def life_element(a_date: date):
    switcher = {
        0: "cold",
        1: "cold_2",
        2: "hot",
        3: "balance"
    }

    for x in range(4):
        element = switcher.get(x, "nothing")
        start_month = ref_data["life_element"][element]["start_month"]
        end_month = ref_data["life_element"][element]["end_month"]
        start_date = ref_data["life_element"][element]["start_date"]
        end_date = ref_data["life_element"][element]["end_date"]
        start = date(1980, start_month, end_month)
        end = date(1980, end_month, end_date)
        compare = date(1980, a_date.month, a_date.day)
        if start <= compare < end:
            return element

    return 'nothing'
