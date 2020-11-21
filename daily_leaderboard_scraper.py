from utils import open_page, select_crossfit_workout, parse_wod, zenplanner_login,navigate_to_workout_page
from selenium.webdriver.support.ui import Select
import json
from datetime import date


if __name__ == '__main__':
    login_url = 'https://crossfitjohnscreek.sites.zenplanner.com/login.cfm'

    # Login
    driver = open_page(login_url)
    zenplanner_login(driver)
    # Find the workout
    now_date = date.today().strftime('%Y-%m-%d')
    workout_link = driver.find_element_by_partial_link_text('Workouts')
    workout_link.click()
    day = driver.find_element_by_id('block_{}'.format(now_date))
    day.click()
    view = driver.find_element_by_link_text('View')
    view.click()
    # Choose the right session
    select = Select(driver.find_element_by_name('objectid'))
    select.select_by_visible_text('CrossFit - All levels')

    workout = driver.find_element_by_class_name('workout')
    wod_breakdown = parse_wod(workout)
    driver.close()

    print(json.dumps(wod_breakdown, indent=2))  