import cv2
import os

vid_name = 'BHB_18052021.mp4'

cap = cv2.VideoCapture(vid_name)
count = 0
index = 0

while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        cv2.imwrite('frames\\frame{:d}.jpg'.format(index), frame)
        count += 26*60  # i.e. at 26 fps, this advances one second
        index += 1
        cap.set(1, count)
    else:
        cap.release()
        break

try:
    os.remove('frames\\frame0.jpg')
except:
    pass