#test changed1
import cv2 as cv
import ctypes
import numpy as np

class Coords(ctypes.Structure):
	_fields_ = [("x",ctypes.c_long),("y",ctypes.c_long)]

def getMousePosition():
    pos = Coords()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pos))
    return [pos.x,pos.y]

def colorCoords(frame , low_bound_color, upp_bound_color, screenSize, resize=False, showCircle=False, showCamera=False) -> 	list:
	top, right, bottom, left = 170 ,1098, 612, 209, 
	
	frame= cv.flip(frame,1)
		
	if resize:
		frame = cv.resize(frame,screenSize)
		roi = frame[top:bottom, left:right]
		#print("frame shape ",roi.shape)
		frame = cv.resize(roi,screenSize)
	

	mask = cv.GaussianBlur(frame,(7,7),cv.BORDER_DEFAULT)
	mask = cv.inRange(mask,low_bound_color,upp_bound_color)

	moments = cv.moments(mask)
	area = moments["m00"]
	x=-1
	y=-1
	if area > 10000:
		x = int(moments['m10'] / area)
		y = int(moments['m01'] / area)
		if showCircle:
			frame=cv.circle(frame, (x, y), 2, (255, 0, 0), 10)

	if showCamera:
		cv.imshow("camera view", np.hstack([frame]))

	return [x,y]


if __name__ == '__main__':
	screenSize = ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1)
	camera = cv.VideoCapture(0)
	lower = np.array([240,240,240],dtype= "uint8")
	upper = np.array([255,255,255],dtype= "uint8")

	ctypes.windll.user32.SetCursorPos(0,0)
	mouse_x,mouse_y=getMousePosition()
	x,y=mouse_x,mouse_y
	lastx,lasty = x,y
	offsetx,offsety = x-lastx, y-lasty 
	#print("init x + {} : {} y + {} : {}".format(offsetx,x,offsety,y))
	wasOff=True
	while True:
		(_,frame) = camera.read()
		x,y = colorCoords(frame,lower,upper,screenSize,resize=True, showCircle=True, showCamera=False)
		if x>=0:
			if wasOff:		
				wasOff= False
				lastx,lasty = x,y
			offsetx,offsety = x-lastx, y-lasty 
			ctypes.windll.user32.SetCursorPos(mouse_x+offsetx,mouse_y+offsety)

		else:
			if not wasOff:
				wasOff=True
				ctypes.windll.user32.mouse_event(2)				
				ctypes.windll.user32.mouse_event(4)
			mouse_x,mouse_y=getMousePosition()
		print("x: {} + {} = {} y: {} + {} = {}".format(mouse_x,offsetx,mouse_x+offsetx,mouse_y,offsety,mouse_y+offsety))
		keypress = cv.waitKey(1) & 0xff
		if keypress == ord("q"):
			break
	
	camera.release()
	cv.destroyAllWindows()
