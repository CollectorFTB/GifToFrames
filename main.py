import cv2
import numpy
import sys
import os


def main():
    file_name = sys.argv[1]
    if file_name[-4:] != '.gif':
        print('bad file name', file_name)
        return False

    if not os.path.exists(file_name[:-4]):
        os.makedirs(file_name[:-4])

    cap = cv2.VideoCapture(file_name)
    frame, last_frame, i = [0], [1], 1
    while True:
        frame = cap.read()[1]
        if numpy.array_equal(last_frame, frame):
            break
        cv2.imwrite(file_name[:-4]+'/' + file_name[:-4] + str(i) + '.png', frame)
        last_frame = frame
        i += 1
    os.remove(file_name[:-4]+'/' + file_name[:-4] + str(i-1) + '.png')


if __name__ == '__main__':
    main()


