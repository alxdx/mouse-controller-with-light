import cv2 as cv
import imutils
import numpy as np


def colorCoords(src , low_bound_color, upp_bound_color, resize=False, showCircle=False, showCamera=False) -> 	list:
	(_,frame) = camera.read()
	frame= cv.flip(frame,1)
		
	if resize:
		frame= cv.resize(frame,screenSize)
		
	mask = cv.GaussianBlur(frame,(7,7),cv.BORDER_DEFAULT)
	mask = cv.inRange(mask,low_bound_color,upp_bound_color)

	moments = cv.moments(mask)
	area = moments["m00"]
	x=0
	y=0
	if area > 10000:
		x = int(moments['m10'] / area)
		y = int(moments['m01'] / area)
		if showCircle:
			frame=cv.circle(frame, (x, y), 2, (255, 0, 0), 10)

	if showCamera:
		cv.imshow("camera view", np.hstack([frame]))

	return [x,y]
