import cv2
import os

video = "Bairan.mp4"
cap = cv2.VideoCapture(video)

os.makedirs("wallpapers", exist_ok=True)

count = 0
frame_no = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    if frame_no % 30 == 0:  # every 30 frames
        frame = cv2.resize(frame, (3840,2160))
        cv2.imwrite(f"wallpapers/wp_{count}.jpg", frame)
        count += 1
    
    frame_no += 1

cap.release()