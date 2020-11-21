import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import json


def scrape_weekly_sched(url):

    response = requests.get(url)

    if response.status_code != 200:
        print("page read failed...")
        exit(2)

    soup = BeautifulSoup(response.text, "html.parser")

    week_sched = soup.findAll('table')[2]

    no_attendance_list = [
        'Sunday 8am Weightlifting Class',
        'Session 2 - CrossFit Lions',
        'Session 2 - CrossFit Cubs',
        'Session 2 - CrossFit Teens',
        'Session 1 - CrossFit Lions',
        'Session 1 - CrossFit Cubs',
        'Session 1 - CrossFit Teens',
        'Saturday Partner / Team WOD',
        'Weightlifting Class - Level II',
        'Sunday Weightlifting Class',
        'Paleo Potluck - Doc talk - Power from the Feet',
        'Weightlifting Class',
        'CrossFit Teens (session 2)',
        'CrossFit Teens (session 1)',
        'CrossFit Kids (session 2)',
        'CrossFit Kids (session 1)'
    ]

    time_format = '%A, %B %d, %Y, %I:%M %p'
    weekly_attendance = []
    for l in week_sched.find_all('tr'):
        if l.attrs['class'] == ['group']:
            date_str = l.find_next('td').text
        else:
            i = 0
            cell_data = {}
            for cell in l.find_all('td'):
                if cell.attrs['class'] == ["label"]:
                    tod = cell.find_next('div').text
                    date_str_full = date_str + ", " + tod
                else:
                    if i == 1:
                        regex_match = re.match(r'(.*)\((\d+)', cell.text)
                        if not regex_match:
                            cell_data['session'] = cell.text
                        else:
                            cell_data['session'] = regex_match.group(1)
                        if cell_data['session'] not in no_attendance_list:
                            try:
                                cell_data['attendance'] = int(regex_match.group(2))
                            except AttributeError:
                                print(cell.text)
                                exit(2)
                        else:
                            cell_data['attendance'] = 0
                    elif i == 2:
                        cell_data['coach'] = cell.text
                i+=1
            ts = int(time.mktime(time.strptime(date_str_full, time_format)))
            cell_data['tod'] = time.strftime('%I:%M%p', time.localtime(ts))
            cell_data['dow'] = time.strftime('%a', time.localtime(ts))
            cell_data['timestamp'] = ts
            cell_data['date'] = time.strftime('%Y-%m-%d', time.localtime(ts))
            weekly_attendance.append(cell_data)
    return weekly_attendance


def create_week_list(start_week_date):
    weeks_list = []
    time_format = '%Y-%m-%d'
    start_date_ts = int(time.mktime(time.strptime(start_week_date, time_format)))
    seconds_in_week = 60*60*24*7
    for i in range(0, 52, 1):
        week_ts = start_date_ts - seconds_in_week*i
        weeks_list.append(time.strftime(time_format, time.localtime(week_ts)))
    
    return weeks_list


def main():
    weeks_list = create_week_list('2019-06-30')
    yearly_attendance = []
    for week in weeks_list:
        print('Reading data for week: ', week)
        url = 'https://crossfitjohnscreek.sites.zenplanner.com/calendar.cfm?DATE={}&VIEW=list'.format(week)
        yearly_attendance += scrape_weekly_sched(url)
    
    with open('yearly_attendance.json', 'w') as f:
        json.dump(yearly_attendance, f, indent=4, separators=(',', ':'), sort_keys=True)
        f.write('\n')


if __name__ == '__main__':
    main()