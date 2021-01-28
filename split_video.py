import cv2

vidcap = cv2.VideoCapture('summer.mp4')
count = 0

while (vidcap.isOpened()):
    ret, image = vidcap.read()

    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))

    if (count < length):
        if (int(vidcap.get(1)) % (fps/2) == 0):
            print('Saved frame number : ' + str(int(vidcap.get(1))))
            cv2.imwrite("frames/frame%d.jpg" % count, image)
            print('Saved frame%d.jpg' % count)
            count += 1
        else:
            count += 1
    else:
        if (int(vidcap.get(1)) % (fps/2) == 0):
            print('Saved frame number : ' + str(int(vidcap.get(1))))
            cv2.imwrite("frames/frame%d.jpg" % count, image)
            print('Saved frame%d.jpg' % count)
        break

vidcap.release()