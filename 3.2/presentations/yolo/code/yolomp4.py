from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')

# Открываем файл вместо веб-камеры
video_path = '/Users/arkadijnetot/Documents/projects/3-course/3.2/presentations/yolo/code/videos/cat.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Не удалось открыть видео: {video_path}")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, conf=0.25, verbose=False)
    annotated = results[0].plot()

    cv2.imshow('YOLOv8 Video', annotated)
    if cv2.waitKey(1) & 0xFF in (ord('q'), 27):
        break

cap.release()
cv2.destroyAllWindows()
