from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import sys
import json
import re


def open_page(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver


def zenplanner_login(driver):
    with open('.cf_cred') as f:
        cred = json.load(f)
    element_user = driver.find_element_by_id('idUsername')
    element_password = driver.find_element_by_id('idPassword')
    input_array = driver.find_elements_by_tag_name('input')
    for i in input_array:
        if i.get_attribute('type') == 'SUBMIT':
            break
    element_user.send_keys(cred['user'])
    element_password.send_keys(cred['pass'])
    i.submit()


def navigate_to_workout_page(driver):
    workout_link = driver.find_element_by_partial_link_text('Workouts')
    workout_link.click()



def select_crossfit_workout(driver):
    select = Select(driver.find_element_by_name('objectid'))
    try:
        select.select_by_visible_text('CrossFit - All levels')
    except NoSuchElementException as e:
        print(e)
    close_driver(driver)
    sys.exit(2)

def parse_wod(workout):
    divs = workout.find_elements_by_tag_name('div')

    wod_breakdown = {}
    for div in divs:
        class_name = div.get_attribute('class')
        if class_name == 'sectionTitle':
            title = div.find_element_by_tag_name('h2').text.lower()
            wod_breakdown[title] = ''
            continue
        if class_name == 'skillName':
            if title == 'strength':
                wod_breakdown[title] = {
                    'skill': div.text.lower(),
                    'desc': ''
                }
            if title == 'conditioning':
                wod_breakdown[title] = {
                    'name': div.text.lower(),
                    'desc': ''
                }
            continue
        if class_name == 'skillDesc':
            if title == 'context' or title == 'skill':
                wod_breakdown[title] = div.text.lower()
            elif title == 'strength' or title =='conditioning':
                wod_breakdown[title]['desc'] += div.text.lower()
            elif title == 'optional':
                wod_breakdown[title] = parse_optional(div.text.lower())
            continue
    return wod_breakdown


def parse_optional(content):
    cash_out = re.search("cash out:(\s\S.*)", content).group(1)
    hypertrophy = re.search("hypertrophy:(\s\S.*)", content).group(1)
    optional = {
        'cash_out': cash_out.strip(),
        'hypertophy': hypertrophy.strip()
    }
    return optional

def close_driver(driver):
    driver.close()
