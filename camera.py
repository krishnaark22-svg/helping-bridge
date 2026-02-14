import cv2
import mediapipe as mp
import numpy as np
from model_trainer import GestureManager
class VideoCamera:
    def __init__(self):
            self.video=cv2.VideoCapture(0)
            self.mp_hands=mp.solutions.hands
            self.hands=self.mp_hands.Hands(model_complexity=0,min_detection_confidence=0.7,min_tracking_confidence=0.7)
            self.manager=GestureManager()
            self.current_prediction="Waiting" 
            self.is_recording=False
            self.record_label=""
            self.recorded_data=[]
            self.frames_recorded=0
            self.MAX_FRAMES=40
    def __del__(self):
          self.video.release()
    def start_recording(self,label):
          self.record_label=label
          self.is_recording=True
          self.recorded_data=[]
          self.frames_recorded=0
          print(f"Started recording for:{label}")
    def get_frame(self):
        success, image = self.video.read()
        if not success:
            return None, "Camera Error"
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        status_text = self.current_prediction
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                keypoints = np.array([[res.x, res.y, res.z] for res in hand_landmarks.landmark]).flatten()
                if self.is_recording:
                    self.recorded_data.append(keypoints)
                    self.frames_recorded += 1
                    status_text = f"Recording:{self.frames_recorded}/{self.MAX_FRAMES}"
                    if self.frames_recorded >= self.MAX_FRAMES:
                        self.manager.add_data(self.record_label, self.recorded_data)
                        self.is_recording = False
                        status_text = f"Saved'{self.record_label}'!"
                        self.current_prediction = status_text
                else:
                     self.current_prediction=self.manager.predict(keypoints)
                     status_text=self.current_prediction
        color=(0,0,255) if self.is_recording else (0,128,0)
        cv2.rectangle(image,(0,0),(640,50),color,-1)
        cv2.putText(image,status_text,(10,35),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
        ret,jpeg=cv2.imencode('.jpg',image)
        return jpeg.tobytes(),status_text               
