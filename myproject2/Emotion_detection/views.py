from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2
from fer import FER
import pygame
import numpy as np
import os

detector = FER()

emoji_folder = 'emotion_detection/static/emoji'
emojis = {
    'happy': os.path.join(emoji_folder, 'happy.png'),
    'angry': os.path.join(emoji_folder, 'angry.png'),
    'surprise': os.path.join(emoji_folder, 'surprise.png'),
    'sad': os.path.join(emoji_folder, 'sad.png'),
    'disgust': os.path.join(emoji_folder, 'disgust.png'),
    'fear': os.path.join(emoji_folder, 'fear.png'),
    'neutral': os.path.join(emoji_folder, 'neutral.png')
}

pygame.init()
font_size = 24
font = pygame.font.SysFont('Arial', font_size)
baskin_font_size = 30
baskin_font = pygame.font.SysFont('Arial', baskin_font_size)

def load_emoji(image_path):
    if os.path.exists(image_path):
        emoji_image = pygame.image.load(image_path)
        return pygame.transform.scale(emoji_image, (30, 30))
    else:
        print(f"Emoji dosyası bulunamadı: {image_path}")
        return None

def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break

        emotions = detector.detect_emotions(frame)
        if not emotions:
            continue

        dominant_emotion = max(emotions[0]['emotions'], key=lambda e: emotions[0]['emotions'][e])
        dominant_emotion_score = emotions[0]['emotions'][dominant_emotion]

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))

        loaded_emojis = {emotion: load_emoji(path) for emotion, path in emojis.items()}

        for face in emotions:
            (x, y, w, h) = face['box']
            emotion_scores = face['emotions']

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)

            for i, (e, s) in enumerate(emotion_scores.items()):
                text = f"{e}: {s*100:.2f}%"
                text_surface = font.render(text, True, (0, 0, 0))
                frame_surface.blit(text_surface, (x, y - 10 - (i * 30)))

                emoji = loaded_emojis.get(e)
                if emoji:
                    frame_surface.blit(emoji, (x + w + 10, y - 10 - (i * 30)))

        if dominant_emotion in loaded_emojis:
            dominant_emoji = loaded_emojis.get(dominant_emotion)
            if dominant_emoji:
                frame_surface.blit(dominant_emoji, (10, frame_surface.get_height() - 80))
            dominant_text = f"Baskın Duygu: {dominant_emotion.capitalize()} ({dominant_emotion_score*100:.2f}%)"
            dominant_text_surface = baskin_font.render(dominant_text, True, (255, 255, 255))

            box_width = dominant_text_surface.get_width() + 60
            box_height = dominant_text_surface.get_height() + 20
            pygame.draw.rect(frame_surface, (0, 0, 0, 180), pygame.Rect(10, frame_surface.get_height() - 100, box_width, box_height))
            frame_surface.blit(dominant_text_surface, (20, frame_surface.get_height() - 90))

        frame = pygame.surfarray.array3d(frame_surface)
        frame = frame.swapaxes(0, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def index(request):
    return render(request, 'index.html')

def video_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
