import get_vid_links as gvl
import download_vids as dv
from constants import *
import moviepy.editor
import time


def add_new_empty_col():
    data = gvl.load_data()
    for meeting in data:
        meeting[len(meeting)-1] = meeting[len(meeting)-1][:-1]
        meeting.append('EMPTY')
        gvl.update_data(data)


def update_vid_length():
    data = gvl.load_data()
    for meeting in data:
        if meeting[VIDEO_STATUS] == 'VIDEO_DOWNLOADED':
            if meeting[VIDEO_LENGTH] == 'EMPTY' or meeting[VIDEO_LENGTH] == 'EMPTY\n':
                ticker = dv.get_file_name(meeting)
                vid_length = get_vid_time(ticker)
                meeting[VIDEO_LENGTH] = vid_length
                print(vid_length)
    gvl.update_data(data)


def get_vid_time(ticker):
    vid_name = 'videos\\'+ticker+'.mp4'  # link to google drive file
    video = moviepy.editor.VideoFileClip(vid_name)
    vid_length_in_seconds = int(video.duration)
    vid_length = time.strftime('%H:%M:%S', time.gmtime(vid_length_in_seconds))
    return str(vid_length)




