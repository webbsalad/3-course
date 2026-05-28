from PIL import Image, ImageColor, ImageDraw
import math

we = 1000
hg = 1000

image = Image.new("RGB", (we, hg))
draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, we, hg), fill = 
               ImageColor.getrgb(("white")))  # значения экрана

# центральные линии стрелочки х, у
draw.line((we * 0.5, 0, we * 0.5, we), fill = 
          ImageColor.getrgb("black"))
draw.line((0, hg * 0.5, hg, hg * 0.5), fill = 
          ImageColor.getrgb("black"))

print("Введите колличество лет:")
years = float(input()) * 365



### Земля - Марс
draw.text((20, 20), "Earth Mars", fill = ("#000000"))
draw.rectangle((15, 15, 85, 35), outline = ("#000000"))
def siny1(x):
    return ((228 * math.sin(0.009 * x) - 
                149 * math.sin(0.017 * x)) * 
                    0.5 + 0.25 * hg) 
def cosx1(x):
    return ((228 * math.cos(0.009 * x) -
                149 * math.cos(0.017 * x)) * 
                    0.5 + 0.25 * we) 



### Земля - Уран
draw.text((we * 0.5 + 20, 20), "Earth Uranium", fill = ("#000000"))
draw.rectangle((515, 15, 605, 35), outline = ("#000000"))
def siny2(x):
    return ((2871 * math.sin(0.0002 * x) - 
             149 * math.sin(0.0172 * x)) *
                0.08 + 0.25 * hg) 
def cosx2(x):
    return ((2871 * math.cos(0.0002 * x) - 
             149 * math.cos(0.0172 * x)) *
                0.08 + 0.75 * we) 


### Земля - Меркурий
draw.text((20, hg * 0.5 + 20), "Earth Mercury", fill = ("#000000"))
draw.rectangle((15, 515, 105, 535), outline = ("#000000"))
def siny3(x):
    return (108 * math.sin(0.028 * x) - 149 *
                math.sin(0.017 * x) * 0.5 + 0.75 * hg)
def cosx3(x):
    return (108 * math.cos(0.028 * x) - 149 * 
                math.cos(0.017 * x) * 0.5 + 0.25 * we)


### Сатурн - Юпитер
draw.text((we * 0.5 + 20, hg * 0.5 + 20), "Saturn Jupiter", fill = ("#000000"))
draw.rectangle((515, 515, 605, 535), outline = ("#000000"))
def siny4(x):
    return ((1429 * math.sin(0.0005 * x) - 
                778 * math.sin(0.0014 * x)) * 
                    0.08 + 0.75 * hg) 
def cosx4(x):
    return ((1429 * math.cos(0.0005 * x) -
                778 * math.cos(0.0014 * x)) * 
                    0.08 + 0.75 * we) 


class Point:
    """values XY"""
    def __init__(self, x, y):
        self.x = x
        self.y = y


# 1
start_x1 = 247
x = start_x1
step_x1 = 1

points1 = [] # xy для Земли - Марса


while x < (years + start_x1):
    points1.append(Point(cosx1(x), siny1(x)))
    x += step_x1

print("Рисуется (Земля - Марс)")

for point in points1:
    draw.point((point.x, point.y), fill = 
               ImageColor.getcolor("#073606", "RGB"))



# 2
start_x2 = 7945
x = start_x2
step_x2 = 1
points2 = [] # xy Для Земли - Урана


while x < (years + start_x2):
    points2.append(Point(cosx2(x), siny2(x)))
    x += step_x2
x = start_x2

print("Рисуется (Земля - Уран)")

for point in points2:
    p = (point)
    draw.point((p.x, p.y), fill = 
               ImageColor.getcolor("#073606", "RGB"))


# 3
start_x3 = 280
x = start_x3
step_x3 = 1

points3 = [] # xy для Земли - Меркурия


while x < (years + start_x3):
    points3.append(Point(cosx3(x), siny3(x)))
    x += step_x3
x = start_x3

print("Рисуется (Земля - Меркурий)")

for point in points3:
    p = (point)
    draw.point((p.x, p.y), fill = 
               ImageColor.getcolor("#073606", "RGB"))


# 4
start_x4 = 3323
x = start_x4
step_x4 = 1

points4 = [] # xy для Сатурна - Юпитера


while x < (years + start_x4):
    points4.append(Point(cosx4(x), siny4(x)))
    x += step_x4
x = start_x4

print("Рисуется (Сатурн - Юпитер)")

for point in points4:
    p = (point)
    draw.point((p.x, p.y), fill = 
               ImageColor.getcolor("#073606", "RGB"))

print("Конец рисования")


image.save("траектория движений планет.png", "png")
image.show("траектория движений планет.png")