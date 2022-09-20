import cv2
import mediapipe as mp
import pyautogui

class MouseHumanHand:

	def __init__(self, mode=False, maxHands=2, detectionCon=0.5, modelComplexity=1, trackCon=0.5):
		self.x_screen, self.y_screen = pyautogui.size()
		self.x_screen = self.x_screen+600
		self.mpHands = mp.solutions.hands
		self.finger_coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
		self.dumb = (4, 2)
		self.hands = self.mpHands.Hands(False, 2)
		self.mpDraw = mp.solutions.drawing_utils
		self.smile_cascade = cv2.CascadeClassifier('smile.xml')
		self.face_cascade = cv2.CascadeClassifier('face.xml')

	def handsFingure(self,image,draw=True):
		imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		self.results = self.hands.process(imageRGB)

		if self.results.multi_hand_landmarks:
			for handLms in self.results.multi_hand_landmarks:
				if draw:
					self.mpDraw.draw_landmarks(image, 
											   handLms, 
											   self.mpHands.HAND_CONNECTIONS)

		return image


	def detectFingure(self, image, draw=True):
		movelist = []
		handlist = []
		if self.results.multi_hand_landmarks:
			Hand = self.results.multi_hand_landmarks[0]
			for idx, lm in enumerate(Hand.landmark):
				h, w, c = image.shape
				cx, cy = int(lm.x*w), int(lm.y*h)
				mouse_x, mouse_y = int(lm.x*self.x_screen), int(lm.y*self.y_screen)
				handlist.append((cx, cy))
				movelist.append((mouse_x, mouse_y))
				print(mouse_x, mouse_y, cx, cy)

		if len(handlist)!=0:
			cv2.circle(image, handlist[8], 10, (255, 0, 255), cv2.FILLED)
			pyautogui.moveTo(movelist[8][0], movelist[8][1], 0.01)

		return handlist


	def DetectSmile(self, frame):
	    faces = self.face_cascade.detectMultiScale(frame, 1.3, 5)
	    for (x, y, w, h) in faces:
	        cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)
	        roi_gray = frame[y:y + h, x:x + w]
	        roi_color = frame[y:y + h, x:x + w]
	        smiles = self.smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
	        for (sx, sy, sw, sh) in smiles:
	            cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)
	    return frame

	def CountFingures(self, handlst):
		count = 0
		if len(handlst)!=0:
			for coord in self.finger_coord:
				if handlst[coord[0]][1] < handlst[coord[1]][1]:
					count += 1

		return count



