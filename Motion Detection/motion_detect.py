0# import the necessary packages
from inspect import currentframe
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import telegram_send as ts
import os
import sys

script_path = os.path.dirname(os.path.realpath(sys.argv[0]))

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=30000, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
# otherwise, we are reading from a video file
else:
    vs = cv2.VideoCapture(args["video"])
# initialize the first frame in the video stream

firstFrame = None
i = 1
count = 0


last_time = time.time()

def send_notification(image):
    global last_time
    current_time = time.time()
    
    now = datetime.datetime.now()
    d = now.strftime('%d/%m/%Y %I:%M:%S %p') #12-hour format

    if current_time - last_time > 15:
        # imgRead = cv2.imread(image)
        cv2.imwrite(script_path + "\\last_sent_image.jpeg", image)
        with open(script_path + "\\last_sent_image.jpeg", 'rb') as img:
            ts.send(messages=["Motion Detected: " + str(d)], images=[img])
        last_time = current_time

# loop over the frames of the video
while True:
    # grab the current frame
    frame = vs.read()
    currentFrame = frame
    frame = frame if args.get("video", None) is None else frame[1]

    # if the frame could not be grabbed, then we have reached the end of the video
    if frame is None:
        break

	# resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=720)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    i += 1
	# if the first frame is None, initialize it
    if firstFrame is None or (i % 1000) == 0:
        firstFrame = gray
        continue

    # compute the absolute difference between the current frame and first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue
        # compute the bounding box for the contour, draw it on the frame
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # count += 1
        # print("Count: ", count, end='\r')
        send_notification(currentFrame)


    # draw the timestamp on the frame
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    # show the frame and record if the user presses a key
    cv2.imshow("Cam Feed", frame)
    # cv2.imshow("Thresh", thresh)
    # cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    # if `q` or Esc (key == 27) key is pressed, break from the loop
    if key == ord("q") or key == 27:
        break

# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()