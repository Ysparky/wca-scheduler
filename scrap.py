from bs4 import BeautifulSoup
from dateutil import parser
from ics import Calendar, Event
from utils import get_datetime
import requests

from competition import Competition

comp_url = 'https://www.worldcubeassociation.org/competitions/PucallpaCubea2022'
url = f'{comp_url}#competition-schedule'
words_to_ignore = ['From', 'To', 'Format', 'Time limit', 'Cutoff', 'Proceed', '*', '**']
page = requests.get(url, verify=False)
soup = BeautifulSoup(page.content, 'html.parser')

h3_tags = soup.find_all('h3')
comp_name = h3_tags[0].text.strip()
comp_dates = list()
for tag in h3_tags:
    sentence = tag.text.strip()
    if "(" in sentence and ")" in sentence:
        date = sentence[sentence.find('(') + 1:sentence.find(')')]
        comp_dates.append(date)

comp_days = len(comp_dates)

schedules = soup.find_all('div', class_='schedule-table')

if comp_days != len(schedules):
    raise Exception('Schedules length do not match dates length')

comp_schedules = list()
for schedule in schedules:
    schedule_table_list = list()
    for item in schedule.children:
        if item != "\n":
            schedule_table_list.append(item)

    row_schedule = list()

    for item in schedule_table_list:
        stripped_item = list()
        for line in item.text.splitlines():
            if line.strip():
                stripped_line = line.strip()
                if stripped_line not in words_to_ignore:
                    stripped_item.append(stripped_line)
        row_schedule.append(stripped_item)

    for item in row_schedule:
        item_length = len(item)
        if item_length == 7:
            last_item = item[6]
            first_char = last_item[0]
            if first_char.isnumeric():
                item.append('')
            else:
                item.insert(6, '')
        else:
            difference = 8 - item_length
            if difference > 0:
                for x in range(0, difference):
                    item.append('')
    comp_schedules.append(row_schedule)

competition = Competition(comp_name, comp_dates, comp_schedules)

c = Calendar()
for i in range(0, competition.days):
    # days
    parsed_date = parser.parse(competition.dates[i])
    for row in competition.schedules[i]:
        e = Event()
        e.name = row[2]
        e.location = row[3]
        e.begin = get_datetime(parsed_date, parser.parse(row[0]))
        e.end = get_datetime(parsed_date, parser.parse(row[1]))
        c.events.add(e)
with open(f'{competition.name}.ics', 'w') as f:
    f.writelines(c.serialize_iter())

# 1 - start
# 2 - end
# 3 - event
# 4 - room
# 5 - format
# 6 - time limit
# 7 - cutoff
# 8 - proceed
