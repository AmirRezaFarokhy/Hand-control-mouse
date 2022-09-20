import cv2
import time
import pyautogui
from hand_mouse import MouseHumanHand

def main():
	cap = cv2.VideoCapture(0)
	tracker = MouseHumanHand()

	while True:
		success, image = cap.read()
		image = tracker.handsFingure(image)
		#image = tracker.DetectSmile(image)
		lmList = tracker.detectFingure(image)
		counter = tracker.CountFingures(lmList)
		if counter==2:
			pyautogui.click()
		cv2.imshow("mouse_hands", image)
		cv2.waitKey(1)


if __name__ == "__main__":
	main()
