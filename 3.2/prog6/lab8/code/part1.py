import cv2
import os

def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)
    net.setInput(blob)
    detections = net.forward()
    faceBoxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            faceBoxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)
    return frameOpencvDnn, faceBoxes

def process_image_file(image_path, net):
    if not os.path.exists(image_path):
        print(f"Ошибка: Файл '{image_path}' не найден.")
        return None
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Ошибка: Не удалось загрузить изображение из файла '{image_path}'.")
        return None
    resultImg, faceBoxes = highlightFace(net, frame)
    if not faceBoxes:
        print(f"Лица не распознаны в файле '{image_path}'.")
    return resultImg

faceProto = "/Users/arkadijnetot/Documents/projects/3-course/3.2/prog6/lab8/code/opencv_face_detector.pbtxt"
faceModel = "/Users/arkadijnetot/Documents/projects/3-course/3.2/prog6/lab8/code/opencv_face_detector_uint8.pb"

if not os.path.exists(faceProto) or not os.path.exists(faceModel):
    print("Ошибка: Не найдены файлы модели нейросети.")
    print(f"Убедитесь, что '{faceProto}' и '{faceModel}' находятся в той же директории, что и скрипт.")
    exit()

faceNet = cv2.dnn.readNet(faceModel, faceProto)

print("\n--- Тестирование обработки изображения из файла ---")
image_file_path = "/Users/arkadijnetot/Documents/projects/3-course/3.2/prog6/lab8/code/image.png"

if not os.path.exists(image_file_path):
    print(f"Внимание: Файл '{image_file_path}' не найден для тестирования изображений.")
    print("Создайте его или измените переменную 'image_file_path' на существующее изображение.")
else:
    processed_image = process_image_file(image_file_path, faceNet)

    if processed_image is not None:
        cv2.imshow(f"Face Detection from Image: {image_file_path}", processed_image)
        print("Нажмите любую клавишу для закрытия окна с изображением.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

print("\n--- Тестирование обработки видео с камеры ---")
video = cv2.VideoCapture(0)

if not video.isOpened():
    print("Ошибка: Не удалось открыть видеопоток с камеры. Убедитесь, что камера подключена и не используется другим приложением.")
else:
    print("Нажмите 'Esc' или любую другую клавишу для выхода из видеопотока.")
    while True:
        hasFrame, frame = video.read()
        if not hasFrame:
            print("Не удалось получить кадр с камеры. Возможно, поток завершился.")
            break
        
        resultImg, faceBoxes = highlightFace(faceNet, frame)
        if not faceBoxes:
            pass
        
        cv2.imshow("Face Detection (Camera)", resultImg)

        if cv2.waitKey(1) != -1:
            break

    video.release()
    cv2.destroyAllWindows()

print("\n--- Программа завершена ---")