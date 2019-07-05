# a good idea to make this script a function part of a while loop in the main drone code
# while true:
#       press a key
#           tracking function()
#       press another key
#           break
# that way this is called whenever we enter commands prompted by the main drone code
# and the ROI selection would be automatically refreshed from there

from imutils.video import VideoStream
import imutils
import time
import cv2

# use the built-in CSRT tracker
tracker = cv2.TrackerCSRT_create()

# initialize the bounding box coordinates
initBB = None

# reference the webcam
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(1.0)

# loop over frames from the video stream
while True:
	# grab the current frame, and check if we have reached the end of the stream
	frame = vs.read()
	if frame is None:
		break

	# resize the frame for faster processing and grab the frame dimensions
	frame = imutils.resize(frame, width=500)
	(H, W) = frame.shape[:2]
	centerX = W / 2
	centerY = H / 2

	# check to see if we are currently tracking an object
	if initBB is not None:
		# grab the new bounding box coordinates of the object
		(success, box) = tracker.update(frame)

		# check to see if the tracking was a success
		if success:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(frame, (x, y), (x + w, y + h),
				(0, 255, 0), 2)
			if centerX > x and centerX < x + w:
                            print("move")
                            # [TO DO] NEED TO SET ROLL MAGNITUDE AND DIRECTION
                        else:
                            print("turn")
                            # [TO DO] NEED TO SET YAW MAGNITUDE AND DIRECTION

	# show the output frame
	cv2.circle(frame,(centerX,centerY),(2),(255,51,255),5)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# press the 's' key to set a bounding box to track
	# [TO DO] AUTOMATE ROI SELECTION
	if key == ord("s"):
                # [TO DO] MANUALLY SELECT NEW ROI
                initBB = None
		# press 'ENTER' or 'SPACE' to select the ROI
		initBB = cv2.selectROI("Frame", frame, fromCenter=False,
			showCrosshair=True)

		# start OpenCV object tracker using the supplied bounding box coordinates
		tracker.init(frame, initBB)

        # [TO DO] NEED TO ADD CODE TO PAUSE THE DRONE'S RECORDING PROCESS

	# if the 'q' key was pressed, break from the loop
	elif key == ord("q"):
		break
	    	# [TO DO] NEED TO ADD CODE FOR LANDING THE DRONE

# release the webcam pointer
vs.stop()

# close all windows
cv2.destroyAllWindows()
