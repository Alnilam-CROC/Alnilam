import requests

# При ошибке при парсе сайта функция getJSON() выдаёт 0
# Если файл пришёл пустым, функция lessons_schedule() выдаёт 1
def getJSON(group):
    headers = {
        'Referer': 'https://rasp.dmami.ru/',
    }

    params = {
        'group': group,
        'session': '0',
    }

    response = requests.get('https://rasp.dmami.ru/site/group', params=params, headers=headers)
    if response.status_code != 200:
        return 0
    try:
        data = response.json()
    except json.JSONDecodeError as e:
        return 0, e
    return data


import json

data = getJSON('211-361')
data = json.dumps(data)
data = json.loads(data)

lesson_time = {"1": ["090000", "103000"], "2": ["104000", "121000"], "3": ['122000', '135000'],
               "4": ['143000', '160000'], "5": ['161000', '174000'], "6": ['175000', '192000'],
               "7": ['193000', '210000']}
# week_day_real = {1: ["20230904", "MN"], 2: ["20230905", "TUE"], 3: ["20230906", "WE"], 4: ["20230907", "THR"], 5: ["20230908", "FR"], 6: ["20230909", "SA"]}
import datetime
from icalendar import Calendar, Event, vText


def date_comparison(d1, d2, x):  # d1, d2 - YYYY-MM-DD, x - 5 ноября 2023 и днём, который парсим
    d1_list = d1.split("-")
    d2_list = d2.split("-")
    d1 = datetime.date(int(d1_list[0]), int(d1_list[1]), int(d1_list[2]))
    d2 = datetime.date(int(d2_list[0]), int(d2_list[1]), int(d2_list[2]))
    if d1 <= datetime.date(2023, 11, 12 + int(x)) <= d2:
        return True
    else:
        return False


def lessons_schedule(json_data):
    if json_data is None:
        return 1
    if "grid" in json_data:
        cal = Calendar()
        cal.add('prodid', '-//Google Ins//Google Calendar 70.9054//EN')
        cal.add('version', '2.0')
        cal.add('dtstart', datetime.datetime(2023, 9, 1, 0, 0, 0))
        cal["X-WR-CALNAME"] = "Раписание пар политеха"
        cal["X_WR_TIMEZONE"] = "Europe/Moscow"
        for week_day in json_data["grid"]:
            for lesson_number in json_data["grid"][week_day]:
                lessons = json_data["grid"][week_day][lesson_number]
                for lesson in lessons:
                    if lesson["sbj"]:
                        df = lesson["df"]
                        dt = lesson["dt"]
                        if date_comparison(df, dt, week_day):
                            lesson_name = lesson["sbj"]
                            teacher = lesson["teacher"]
                            location = lesson["location"] + " "
                            place = lesson["auditories"][0]["title"]
                            type = lesson["type"]
                            if "href" in place: place = place[place.find("https"): place.find('target') - 2]

                            event = Event()

                            dt_list = dt.split("-")

                            dff = datetime.datetime(2023, 11, 5 + int(week_day),
                                                    int(lesson_time[lesson_number][0][0:2]),
                                                    int(lesson_time[lesson_number][0][2:4]),
                                                    int(lesson_time[lesson_number][0][4:6]))
                            dt = datetime.date(int(dt_list[0]), int(dt_list[1]), int(dt_list[2]))
                            event['uid'] = "20230901T" + lesson_time[lesson_number][0] + "/" + str(week_day)
                            event.add('summary', vText(lesson_name, encoding='utf-8'))
                            event.add('dtstart', datetime.datetime(2023, 11, 5 + int(week_day),
                                                                   int(lesson_time[lesson_number][0][0:2]),
                                                                   int(lesson_time[lesson_number][0][2:4]),
                                                                   int(lesson_time[lesson_number][0][4:6])))
                            event.add('dtend', datetime.datetime(2023, 11, 5 + int(week_day),
                                                                 int(lesson_time[lesson_number][1][0:2]),
                                                                 int(lesson_time[lesson_number][1][2:4]),
                                                                 int(lesson_time[lesson_number][1][4:6])))
                            event.add('rrule', {'freq': 'weekly', "interval": 1, 'until': dt})
                            event.add('location', vText(location + place, encoding='utf-8'))
                            event.add('description', vText(type + "; " + teacher, encoding='utf-8'))
                            cal.add_component(event)
                        else:
                            continue
        cal.to_ical()
        f = open('exapmle.ics', 'wb')
        f.write(cal.to_ical())
        f.close()

    return cal.to_ical().decode("utf-8").replace('\r\n', '\n').strip()


print(lessons_schedule(data))
