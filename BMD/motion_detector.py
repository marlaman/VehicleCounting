
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import csv

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

if args.get("video", None) is None:
	vs = VideoStream(src=0).start()
	time.sleep(1.0)

else:
	vs = cv2.VideoCapture(args["video"])

times= datetime.datetime.now()
firstFrame = None
count=0
n=0
row = [n, times, 'Begumpet', count ]

csvFile = open('traffic.csv', 'a')
writer = csv.writer(csvFile)
writer.writerow(row)

def get_centroid(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1

    return (cx, cy)

##def timesegment():
##    a = datetime.datetime.now()
##    if a.microsecond == 10:
##        return 1

temp=0;
timet=0;



while True:
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]

	min_contour_width= 10
	min_contour_height= 10
	text = count

	if frame is None:
		break

	frame = imutils.resize(frame, width=500)
	cv2.line(frame,(450,0),(450,450),(255,0,0),5)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	if firstFrame is None:
		firstFrame = gray
		continue

	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 13, 255, cv2.THRESH_BINARY)[1]


	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	for c in cnts:
		if cv2.contourArea(c) < args["min_area"]:
			continue


		(x, y, w, h) = cv2.boundingRect(c)
		(t,r) = get_centroid(x, y, w, h)
		times = datetime.datetime.now()
		#print(times.microsecond)

		if t >385 and t< 400 :
			temp=1;

		if t> 400 and temp == 1:
		   count += 1
		   temp=0
		   n += 1
		   row = [n, times, 'Begumpet', count ]
		   writer.writerow(row)

		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		#contour_valid = (w >= min_contour_width) and (h >= min_contour_height)
		#if contour_valid:
			#count += 1
			#break




	cv2.putText(frame, "Vehicles: {}".format(count), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	cv2.imshow("Threshold", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	cv2.imshow("Security Feed", frame)
	cv2.waitKey(20)

	#cv2.imshow("Thresh", thresh)
	#cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break
count = len(detect_vehicles(thresh.copy(), 20, ))
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()


def detect_vehicles(vs, min_contour_width=20, min_contour_height=20):

    matches = []

    # finding external contours
    #im, contours, hierarchy = cv2.findContours(
    #    fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

    # filtering by with, height
    for (i, contour) in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(contour)
        contour_valid = (w >= min_contour_width) and (
            h >= min_contour_height)

        if not contour_valid:
            continue

        # getting center of the bounding box
        centroid = get_centroid(x, y, w, h)

        matches.append(((x, y, w, h), centroid))

    return matches
