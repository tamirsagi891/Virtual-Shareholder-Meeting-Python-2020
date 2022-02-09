import requests
from constants import *
from get_vid_links import load_data,update_data


def fix_video_status(dat_array):
    for line in dat_array:
        line[VIDEO_LINK] = line[VIDEO_LINK]
    return dat_array


def download_video(vid_link, file_name):
    try:
        r = requests.get(vid_link, stream=True)
        with open(file_name, "wb") as file:
            for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                file.write(chunk)
        print(file_name + " Downloaded!")
        return True
    except:
        return False


def date_to_numbers(date):
    num_date = date.split(' ')
    num_date[1] = num_date[1][:-1]
    for i, mon in enumerate(MONTHS_TICKER):
        if mon == num_date[0]:
            if i < 9:
                num_date[0] = "0" + str(i + 1)
            else:
                num_date[0] = str(i + 1)
            break
    for i, mon in enumerate(MONTHS):
        if mon == num_date[0]:
            if i < 9:
                num_date[0] = "0" + str(i + 1)
            else:
                num_date[0] = str(i + 1)
            break
    num_date[0], num_date[1] = num_date[1], num_date[0]
    return ''.join(num_date)


def get_file_name(meeting):
    num_date = date_to_numbers(meeting[MEETING_DATE])
    file_name = meeting[COMP_TICKER] + num_date
    return file_name


def main():
    data_array = fix_video_status(load_data())
    video_downloaded_counter = 1
    for meeting in data_array:
        if (meeting[VIDEO_STATUS] == 'VIDEO EXIST') and (meeting[VIDEO_LINK] != 'EMPTY'):
            file_name = 'videos\\' + get_file_name(meeting) + '.mp4'
            video_link = meeting[VIDEO_LINK]
            if download_video(video_link, file_name) is True:
                meeting[VIDEO_STATUS] = 'VIDEO_DOWNLOADED'
                print(meeting[COMP_NAME], 'vid - downloaded successfully', str(video_downloaded_counter))
                video_downloaded_counter += 1
                update_data(data_array)


if __name__ == '__main__':
    main()
