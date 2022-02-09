import cv2
from skimage.metrics import structural_similarity
import os
import get_vid_links as gvl
import download_vids as dv
from constants import *


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        return False


def get_frames(vid_name, path):
    cap = cv2.VideoCapture(vid_name)
    count = 0
    index = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            cv2.imwrite(path+'\\frame{:d}.jpg'.format(index), frame)
            count += 26 * 20  # i.e. at 26 fps, this advances one second
            index += 1
            cap.set(1, count)
        else:
            cap.release()
            break

    os.remove(path+'\\frame0.jpg')
    return index-1


def structural_sim(img1, img2):
    sim, diff = structural_similarity(img1, img2, full=True)
    if sim > 0.80:
        return True
    return False


def frames_to_keep(num_of_frames, path):
    frames_to_save = [1]

    for frame in frames_to_save:
        img0 = cv2.imread(path + '\\frame{}.jpg'.format(frame), 0)
        for i in range(frame, num_of_frames):
            img1 = cv2.imread(path + '\\frame{}.jpg'.format(i + 1), 0)
            if structural_sim(img0, img1) is False:
                if check_black_frames(img1):
                    frames_to_save.append(i + 1)
                break
    return frames_to_save


def check_black_frames(frame):
    if frame.shape != (720, 1280):
        print("resized")
        frame = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_AREA)
    for path in BAD_FRAMES:
        black_frame = cv2.imread(path, 0)
        if structural_sim(frame, black_frame) is True:
            return False
    return True


def delete_unnecessary_frame(num_of_frames, frames_to_save, path):
    for i in range(1, num_of_frames + 1):
        if i not in frames_to_save:
            os.remove(path+'\\frame{}.jpg'.format(i))


def fix_frame_names(frames_to_save, path):
    for i, frame in enumerate(frames_to_save):
        try:
            os.rename(path + '\\frame{}.jpg'.format(frame), path + '\\frame{}.jpg'.format(i))
        except:
            pass


def find_number_of_frames(ticker):
    video_name = 'videos\\' + ticker + '.mp4'  # G_DRIVE_PATH + ticker + '.mp4'
    path = 'frames\\' + ticker + '_frames'
    if create_folder(path) is False:
        return False

    number_of_frames = get_frames(video_name, path)
    frames_to_save = frames_to_keep(number_of_frames, path)
    delete_unnecessary_frame(number_of_frames, frames_to_save, path)
    fix_frame_names(frames_to_save, path)

    return len(frames_to_save)


def main():
    data = gvl.load_data()
    i = 1
    for meeting in data:
        if meeting[VIDEO_STATUS] == 'VIDEO_DOWNLOADED' and meeting[NUMBER_OF_SLIDES] in NEED_TO_CHECK:
            ticker = dv.get_file_name(meeting)
            number_of_slides = find_number_of_frames(ticker)
            meeting[NUMBER_OF_SLIDES] = str(number_of_slides)
            if i % 25 == 0:
                gvl.update_data(data)
    gvl.update_data(data)
    print("Done!")