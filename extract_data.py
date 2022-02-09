from selenium import webdriver
from constants import *
from datetime import datetime
import re


def update_data(extracted_data):
    with open('data/past_meetings_data.txt', 'a+') as file:
        for meeting in extracted_data[::-1]:
            file.write('>'.join(meeting) + "\n")


def find_last_meeting():
    prev_data = []
    same_day_meetings = []
    try:
        with open('data/past_meetings_data.txt', 'r') as file:
            prev_meetings = file.readlines()
        last_meeting = prev_meetings[-1].split('>')
        for line in prev_meetings:
            prev_data.append(line.split('>'))
        for dat in prev_data:
            if last_meeting[1] == dat[1]:
                same_day_meetings.append(dat[0])
        return last_meeting[1], same_day_meetings
    except:
        return 'April 29, 1999', []


def fix_date(date):
    fixed_date = date
    fixed_date = fixed_date.replace(',', '')
    fixed_date = fixed_date.split(' ')
    for i, mon in enumerate(MONTHS):
        if fixed_date[0] == mon:
            fixed_date[0] = MONTHS_TICKER[i]
    fixed_date = ' '.join(fixed_date)
    datetime_object = datetime.strptime(fixed_date, '%b %d %Y')
    return datetime_object


def compare_dates(last_meeting_date, meeting_data, same_day_meetings):
    last_meeting_date = fix_date(last_meeting_date)
    current_meeting_date = fix_date(meeting_data[1])
    if last_meeting_date > current_meeting_date:
        return -1
    if last_meeting_date == current_meeting_date:
        if meeting_data[0] in same_day_meetings:
            return 1
    return 0


def fix_ticker(ticker):
    fixed_ticker = ticker[::-1]
    if len(fixed_ticker) > 9:
        return 'NONE'
    if len(fixed_ticker) < 4:
        fixed_ticker = fixed_ticker + '_' * (4 - len(fixed_ticker))
    return fixed_ticker


def get_ticker(link):
    ticker = ''
    for let in (link[::-1]):
        if let == '=':
            return fix_ticker(ticker)
        elif let.isalpha():
            ticker += let.capitalize()
    return 'NONE'


def fix_name_date(name_date):
    for month in MONTHS:
        if name_date.find(month) > 0:
            fixed_info = name_date.split(month)
            fixed_info[1] = month + fixed_info[1]
            return fixed_info


def edit_html_info(link, name_date):
    edited_info = (re.split(r'\s{2,}', name_date))
    if len(edited_info) == 1:
        edited_info = fix_name_date(name_date)
    edited_info.append(link)
    edited_info.append(get_ticker(link))
    edited_info.append('EMPTY')
    edited_info.append('EMPTY')
    edited_info.append('EMPTY')
    edited_info.append('EMPTY')
    return edited_info


def extract_data(driver, lst_meeting_date, same_day_meetings, i=1):
    data_array = []
    while True:
        try:
            past_meeting = driver.find_element_by_xpath('//*[@id="past-list-group-mobile"]/a[' + str(i) + ']')
            name_date = past_meeting.get_attribute('text')
            link = past_meeting.get_attribute('href')
            edited_info = edit_html_info(link, name_date)
            dates_compared = compare_dates(lst_meeting_date, edited_info, same_day_meetings)
            if dates_compared == -1:
                return data_array
            elif dates_compared == 0:
                print("i = " + str(i))
                print(edited_info)
                data_array.append(edited_info)
                print("_______________")
            i += 1
        except:
            break
    return data_array


def main():
    lst_meeting_date, same_day_meetings = find_last_meeting()
    driver = webdriver.Chrome(PATH)
    driver.get(URL)
    driver.implicitly_wait(5)
    driver.get(URL)
    driver.implicitly_wait(15)
    extracted_data = extract_data(driver, lst_meeting_date, same_day_meetings)
    update_data(extracted_data)
    driver.close()
    print("Data Extracted")


if __name__ == '__main__':
    main()
