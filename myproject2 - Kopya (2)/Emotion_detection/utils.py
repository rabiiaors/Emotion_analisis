import cv2
from fer import FER

def analyze_emotions(frame):
    detector = FER(mtcnn=True)
    emotion, score = detector.top_emotion(frame)
    return emotion
