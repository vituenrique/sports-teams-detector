import numpy as np
import cv2

# Crop detections creating the players dataset for futher training
def cropBoundingBox(x, y, w, h, img, name):
	cropedImg = img[y:h, x:w]
	cv2.imwrite("dataset/" + str(name) + ".png", cropedImg)

# Use contours to draw box in a img
def drawBoundingBox(img, rects, thickness = 1, createImg = False):
	for x, y, w, h in rects:
		# Slightly shrink the rectangles to get a nicer output.
		pad_w, pad_h = int(0.15 * w), int(0.05 * h)
		# Check for small boxes to avoid false positives
		if (x + w - pad_w) > x + 64 and (y + h - pad_h) > y + 128:    
			# Draw rectangle around contour on original image
			cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (255,0,255), thickness)
			if createImg:
				cropBoundingBox(x+pad_w+thickness, y+pad_h+thickness, x+w-pad_w-thickness, y+h-pad_h-thickness, img, x)

# Main program
def main():

	capWorking = False

	# Constants variables
	kernel = np.ones((5,5),np.uint8)

	# Event variables
	pause = False
	detectionMode = True

	# Video Path
	handball = "./base/handballCroaciaVsHungria.avi"
	basketball = "./base/basketballLakesrVsCeltics.avi"
	futsal = "./base/futsalPortuvalVsAzerbaijan.avi"

	videoPath = futsal

	# Open Video
	cap = cv2.VideoCapture(videoPath)

	# Checks whether the camera is open or not. The detection only starts when the camera is working!
	if cap.isOpened():
		capWorking = True
		
	frameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
	frames = 0

	#Create Hog Descriptor
	hog = cv2.HOGDescriptor()
	hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

	if capWorking == True:
		
		print('Aplication Started!')
		print('Runnig video ' + videoPath)

		while True:
			# Capture frame
			ret, frame = cap.read(0)
			frames += 1
			
			print('Total frames: ' + str(frameCount))
			print('Current frame: ' + str(frames))

			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

			frame = cv2.medianBlur(frame,5)
			closedImg = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)

			(contours, weights) = hog.detectMultiScale(frame)

			# Checks whether the detection mode is enabled or not
			if detectionMode == True:
				drawBoundingBox(frame, contours, 2, False)

			# Display the resulting frame
			cv2.imshow('Frame', frame)
			#cv2.imshow('Hsv', hsv)
			
			# Keyboard events
			key = cv2.waitKey(30) & 0xff
			if key == 27: # Esc to exit
				break
			if key == 112: # P to pause 
				pause = True
				print('Paused!')
				while pause == True:
					k = cv2.waitKey(30) & 0xff
					if k == 112:
						pause = False
				print('Resumed!')
			if key == 116: # T to enable Tracking Mode
				if detectionMode == True:
					print('Tracking Mode disabled!')
					detectionMode = False
				else:
					print('Tracking Mode enabled!')
					detectionMode = True

	cap.release()
	cv2.destroyAllWindows()

# Main Call
if __name__ == "__main__":
    main()