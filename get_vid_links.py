from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import *
import time
import os


def update_data(extracted_data):
    try:
        os.remove('data/past_meetings_data.txt')
        with open('data/past_meetings_data.txt', 'w') as file:
            for meeting in extracted_data:
                line = '>'.join(meeting)
                if '\n' in line:
                    file.write(line)
                else:
                    file.write('>'.join(meeting) + "\n")

    except IOError:
        pass


def load_data():
    data_array = []
    with open('data/past_meetings_data.txt', 'r') as file:
        for line in file:
            data_array.append(line.split('>'))
    return data_array


def fill_form(driver):
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, REGISTRATION_XPATH)))
        first_name = driver.find_element_by_xpath(FIRST_NAME_XPATH)
        first_name.send_keys(FIRST_NAME)
        last_name = driver.find_element_by_xpath(LAST_NAME_XPATH)
        last_name.send_keys(LAST_NAME)
        email = driver.find_element_by_xpath(EMAIL_XPATH)
        email.send_keys(EMAIL)
        register_button = driver.find_element_by_xpath(REGISTER_BUTTON_XPATH)
        register_button.click()
    except:
        return FORM_NOT_FILLED


def analyze_page(driver):
    for i in range(10):
        for key in XPATH_DICT:
            try:
                driver.find_element_by_xpath(key)
                action = XPATH_DICT[key]
                return ACTION_DICT[action]
            except:
                pass
        time.sleep(2)
    return ACTION_DICT[6]


def obtain_mp4_link(driver, meeting_data):
    vid = driver.find_element_by_xpath(VID_MP4_XPATH)
    link = vid.get_attribute('src')
    if link == '':
        meeting_data[VIDEO_STATUS] = 'NOT UP YET'
    else:
        meeting_data[VIDEO_STATUS] = 'VIDEO EXIST'
        meeting_data[VIDEO_LINK] = link


def meeting_concluded(driver, meeting_data):
    meeting_status = driver.find_element_by_xpath(MEETING_CONCLUDED_XPATH)
    if MEETING_NOT_UPLOADED_YET_TEXT in meeting_status.text:
        meeting_data[VIDEO_STATUS] = 'NOT UP YET'
    else:
        meeting_data[VIDEO_STATUS] = 'NO REC'


def get_video(driver, meeting_data, check_all):
    if check_all is False and meeting_data[VIDEO_STATUS] != 'EMPTY':
        return
    if meeting_data[VIDEO_STATUS] not in NEED_TO_CHECK:
        return
    if meeting_data[VIDEO_LINK] == NEED_TO_CHECK[1]:
        meeting_data[VIDEO_LINK] = NEED_TO_CHECK[0]
    driver.get(meeting_data[MEETING_LINK])
    for i in range(15):
        action = analyze_page(driver)
        if action == 'FILL FORM':
            fill_form(driver)
        elif action == 'MEETING CONCLUDED':
            meeting_concluded(driver, meeting_data)
            return
        elif action == 'BROKEN LINK':
            meeting_data[VIDEO_STATUS] = action
            return
        elif action == 'MP4':
            obtain_mp4_link(driver, meeting_data)
            return
        elif action == 'VIDEO EXISTS':
            meeting_data[VIDEO_STATUS] = action
            return
        elif action == 'PROBLEMATIC LINK':
            meeting_data[VIDEO_STATUS] = action
            return
        time.sleep(2)
    meeting_data[VIDEO_STATUS] = 'PROBLEMATIC LINK'
    return


def main(check_all):
    driver = webdriver.Chrome(PATH)
    data_array = load_data()
    i = 1
    for meeting_data in data_array[::-1]:
        get_video(driver, meeting_data, check_all)
        print(meeting_data, i, '/', len(data_array))
        i += 1
        if (i % 35) == 0:
            print(i, "updates")
            update_data(data_array)
    update_data(data_array)


if __name__ == '__main__':
    main(check_all=False)
