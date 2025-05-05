import os
import torch
from PIL import Image
import cv2
import torchvision.transforms as T
from torchvision.models.detection import maskrcnn_resnet50_fpn



device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#  Загружаем предобученную Mask R-CNN (ResNet-50 + FPN)
model = maskrcnn_resnet50_fpn(pretrained=True).to(device)
model.eval()

# COCO-классы и целевые индексы
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train',
    'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe',
    'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
    'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
    'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet',
    'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven',
    'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
    'hair drier', 'toothbrush'
]
TARGET_IDS = {
    COCO_INSTANCE_CATEGORY_NAMES.index('person'),
    COCO_INSTANCE_CATEGORY_NAMES.index('cat'),
    COCO_INSTANCE_CATEGORY_NAMES.index('dog'),
}

#  Пути к папкам
base_dir      = os.path.dirname(os.path.abspath(__file__))
image_folder  = os.path.join(base_dir, 'images')
output_folder = os.path.join(base_dir, 'detections')
os.makedirs(output_folder, exist_ok=True)

#  Функция для обработки одного изображения
def process_image(fn):
    img_path = os.path.join(image_folder, fn)
    # читаем в OpenCV (BGR)
    orig = cv2.imread(img_path)
    if orig is None:
        print(f"⚠️ Не удалось прочитать {fn}")
        return

    # готовим тензор для модели
    pil_img = Image.open(img_path).convert('RGB')
    tensor  = T.ToTensor()(pil_img).to(device)

    # инференс
    with torch.no_grad():
        output = model([tensor])[0]

    # отрисовка
    threshold = 0.5
    for box, label, score in zip(output['boxes'], output['labels'], output['scores']):
        lbl = label.item()
        conf = score.item()
        if conf < threshold or lbl not in TARGET_IDS:
            continue

        x1, y1, x2, y2 = [int(v) for v in box]
        cls_name = COCO_INSTANCE_CATEGORY_NAMES[lbl]
        text     = f"{cls_name}: {conf:.2f}"

        # рамка
        cv2.rectangle(orig, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # подложка для текста
        (tw, th), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(orig, (x1, y1 - th - baseline), (x1 + tw, y1), (0, 255, 0), -1)
        # текст
        cv2.putText(orig, text, (x1, y1 - baseline),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # показать и сохранить
    win = f"Mask R-CNN: {fn}"
    cv2.imshow(win, orig)
    cv2.waitKey(0)
    cv2.destroyWindow(win)

    out_path = os.path.join(output_folder, f"det_{fn}")
    cv2.imwrite(out_path, orig)
    print(f"✅ {fn} → {out_path}")

#  Основной цикл по всем файлам
for fn in sorted(os.listdir(image_folder)):
    if fn.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        process_image(fn)

print("✔️ Все файлы обработаны.")
