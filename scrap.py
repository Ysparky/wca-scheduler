from bs4 import BeautifulSoup
from dateutil import parser
import requests
import pandas as pd

url = 'https://www.worldcubeassociation.org/competitions//RealCube2022#competition-schedule'
page = requests.get(url, verify=False)
soup = BeautifulSoup(page.content, 'html.parser')

words_to_ignore = ['From', 'To', 'Format', 'Time limit', 'Cutoff', 'Proceed', '*', '**']

h3_tags = soup.find_all('h3')

competition_name = h3_tags[0].text.strip()
competition_dates = list()

for item in h3_tags:
    sentence = item.text.strip()
    if "(" in sentence and ")" in sentence:
        date = sentence[sentence.find('(')+1:sentence.find(')')]
        competition_dates.append(parser.parse(date))

# schedule_table = soup.find('div', class_='schedule-table')
# schedule_table_list = list()
#
# for item in schedule_table.children:
#     if item != "\n":
#         schedule_table_list.append(item)
#
# row_schedule = list()
# for item in schedule_table_list:
#     stripped_item = list()
#     for line in item.text.splitlines():
#         if line.strip():
#             stripped_line = line.strip()
#             if stripped_line not in words_to_ignore:
#                 stripped_item.append(stripped_line)
#     row_schedule.append(stripped_item)
#
# for item in row_schedule:
#     item_length = len(item)
#     if item_length == 7:
#         last_item = item[6]
#         first_char = last_item[0]
#         if first_char.isnumeric():
#             item.append('')
#         else:
#             item.insert(6, '')
#     else:
#         difference = 8 - item_length
#         if difference > 0:
#             for x in range(0, difference):
#                 item.append('')

# print(row_schedule)

# 1 - start
# 2 - end
# 3 - event
# 4 - room
# 5 - format
# 6 - time limit
# 7 - cutoff
# 8 - proceed
