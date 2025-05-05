import os
from ultralytics import YOLO
import cv2

# 1. Загружаем модель
model = YOLO('yolov8n.pt')

# 2. Пути
base_dir      = os.path.dirname(os.path.abspath(__file__))
image_folder  = os.path.join(base_dir, 'images')
output_folder = os.path.join(base_dir, 'detections')
os.makedirs(output_folder, exist_ok=True)

# 3. Перебираем все изображения
for fn in sorted(os.listdir(image_folder)):
    if not fn.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        continue

    img_path = os.path.join(image_folder, fn)
    img = cv2.imread(img_path)
    if img is None:
        print(f"⚠️ Не удалось прочитать {fn}, пропускаем")
        continue

    # 4. Детектируем
    results   = model(img, conf=0.25, verbose=False)
    annotated = results[0].plot()

    # 5. Показываем и ждём, пока вы нажмёте любую клавишу
    win = f"Detection: {fn}"
    cv2.imshow(win, annotated)
    cv2.waitKey(0)       
    cv2.destroyWindow(win)   

    # 6. Сохраняем результат
    out_path = os.path.join(output_folder, f"det_{fn}")
    cv2.imwrite(out_path, annotated)
    print(f"✅ {fn} → {out_path}")

print("✔️ Все файлы обработаны.")
