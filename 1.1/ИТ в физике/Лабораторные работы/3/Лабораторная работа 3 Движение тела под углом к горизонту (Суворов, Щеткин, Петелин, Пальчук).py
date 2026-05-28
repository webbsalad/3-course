from PIL import Image, ImageColor, ImageDraw, ImageFont
import math, random

# list
we = 1000
hg = 1000
font = ImageFont.truetype("calibri", 20)
image = Image.new("RGB", (we, hg))
draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, we, hg), fill = 
               ImageColor.getrgb("white"))
draw.line((50, 0, 50, we), fill = 
          ImageColor.getrgb("black"))
draw.line((0, hg * 0.5, hg, hg * 0.5), fill = 
          ImageColor.getrgb("black"))
draw.text((70, 0), "X", fill = ImageColor.getrgb("black"), font = font)
draw.text((we-20, hg*0.5 - 35), "Y", fill = ImageColor.getrgb("black"), font = font)
draw.text((60, hg*0.5 + 12), "0", fill = ImageColor.getrgb("black"), font = font)

draw.line((50, 0, 35, 15), fill = ImageColor.getrgb("black"))
draw.line((50, 0, 65, 15), fill = ImageColor.getrgb("black"))
draw.line((we, hg*0.5, we-15, hg*0.5 + 15), fill = ImageColor.getrgb("black"))
draw.line((we, hg*0.5, we-15, hg*0.5 - 15), fill = ImageColor.getrgb("black"))

# help func
def r(x): # вывод радиан
    return x * (math.pi) / 180
def ar(x): # вывод градусов
    return x * 180 / math.pi

# func
def co_x(t, v, a):
    return v * math.cos(r(a)) * t
def co_y(t, v, a):  
    return v * math.sin(r(a)) * t - ((9.8 * t**2) / 2)
def co_v(t, v, a): 
    return ((v * math.cos(r(a)))**2 + (v * math.sin(r(a)) - 9.8 * t)**2)**0.5
def co_ur(t, v, a, s):
    return math.tan(r(a)) * co_x(t, v, a) - (((9.8) / (2 * v**2 * math.cos(r(a))**2)) * int(s)**2)
def co_co(t, v, a):
    return ((v * math.sin(r(a)) - 9.8 * t) / (v * math.cos(r(a))))


v = int(input('Input start speed: ' ))
a = int(input('Input start corner for first answer:'))


t = 0
S = []
V = []
Y = []
A = []


# val for first ex
last_x = int(co_x(t, v, a)) / 5 + 50
last_y = int(co_y(t, v, a)) / -5 + 500
while co_y(t, v, a) >= 0:
    b = (co_x(t, v, a))
    c = (co_y(t, v, a))
    S.append(co_x(t, v, a))
    V.append(co_v(t, v, a))
    Y.append(co_ur(t, v, a, b))
    A.append(math.tan(co_co(t, v, a)))
    draw.line((last_x, last_y, (b / 5) + 50, (c / -5) + 500), fill = ImageColor.getrgb("black"))
    last_x = (b / 5) + 50
    last_y = (c / -5) + 500
    t += 0.1

draw.text (((co_x(t, v, a) / 5) + 50, (co_y(t, v, a) / -5) + 500),
          "58 Degrees",  fill = ImageColor.getrgb("blue"))
t = int(t) * 10
print('')

# text on list
k = "Range = " + str("%.2f" % S[t]) + " meters"
print(k)
draw.text((750, 50), k, fill = ImageColor.getrgb("blue"), font = font)
k = 'End speed = ' + ("%.2f" % V[t]) + " m/s"
print(k)
draw.text((750, 70), k, fill = ImageColor.getrgb("blue"), font = font)
k = 'End corner = ' + ("%.2f" % abs(A[t])) + " Degrees"
print(k)
draw.text((750, 90), k, fill = ImageColor.getrgb("blue"), font = font)
k = 'Trajectory equation = ' + ("%.2f" % (Y[t]))
print(k)
draw.text((750, 110), k, fill = ImageColor.getrgb("blue"), font = font)


image.save("tra.png", "png")
input()
image.show("tra.png")
input()

class Corner:
    """"numbs for true corner"""
    def __init__(self, S, A):
        self.s = S
        self.a = A



# list for 2 ex
image = Image.new("RGB", (we, hg))
draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, we, hg), fill = 
               ImageColor.getcolor("#ffffff", "RGB"))

draw.line((50, 0, 50, we), fill = 
          ImageColor.getrgb("black"))
draw.line((0, hg * 0.5, hg, hg * 0.5), fill = 
          ImageColor.getrgb("black"))


draw.text((70, 0), "X", fill = ImageColor.getrgb("black"), font = font)
draw.text((we-20, hg*0.5 - 35), "Y", fill = ImageColor.getrgb("black"), font = font)
draw.text((60, hg*0.5 + 12), "0", fill = ImageColor.getrgb("black"), font = font)

draw.line((50, 0, 35, 15), fill = ImageColor.getrgb("black"))
draw.line((50, 0, 65, 15), fill = ImageColor.getrgb("black"))
draw.line((we, hg*0.5, we-15, hg*0.5 + 15), fill = ImageColor.getrgb("black"))
draw.line((we, hg*0.5, we-15, hg*0.5 - 15), fill = ImageColor.getrgb("black"))


ran = lambda: random.randint(0, 255)
all_grap = []
time = 0
color = ("#%02X%02X%02X" % (ran(), ran(), ran()))
max_s = 0


nac = int(input("Input start value for second task: "))
kon = int(input("Input end value for second task: ")) + 1
step = int(input("Input step for second task: "))
step_m = []
# loop for 2 ex
for a in range(nac, kon, step):
    while co_y (time, v, a) >= 0:
        draw.point(((co_x(time, v, a) / 5) + 50, (co_y(time, v, a) / -5) + 500), 
                   fill = ImageColor.getcolor(color, "RGB"))
        all_grap.append(Corner(co_x(time, v, a), a))
        time += 0.01
    if co_x(time, v, a) > max_s:
        max_s = co_x(time, v, a)
        true_a = a
    if int(co_x(time, v, a)) not in step_m:
        xy = 500
    else:
        xy = 520
    cor = str(a) + " Degrees"
    draw.text (((co_x(time, v, a) / 5) + 50, (co_y(time, v, a) / -5) + xy),
                cor,  fill = ImageColor.getrgb("blue"))

    step_m.append(int(co_x(time, v, a)))

    time = 0
    color = ("#%02X%02X%02X" % (ran(), ran(), ran()))
k = 'Answer to the task number 2 = ' + str(true_a)
draw.text((750, 50), k, fill = ImageColor.getrgb("blue"), font = font)
draw.rectangle((735, 35, 995, 90), outline = ImageColor.getrgb("black"), width = 3)
print("")
print("Answer to the task number 2 = ", true_a, "Degrees")
image.save("tra_2.png", "png")
input()
image.show("tra_2.png")
input()

draw.rectangle((0, 0, we, hg), fill = 
               ImageColor.getcolor("#ffffff", "RGB"))

draw.line((50, 0, 50, we), fill = 
          ImageColor.getrgb("black"))
draw.line((0, hg * 0.5, hg, hg * 0.5), fill = 
          ImageColor.getrgb("black"))


draw.text((70, 0), "X", fill = ImageColor.getrgb("black"), font = font)
draw.text((we-20, hg*0.5 - 35), "Y", fill = ImageColor.getrgb("black"), font = font)
draw.text((60, hg*0.5 + 12), "0", fill = ImageColor.getrgb("black"), font = font)

draw.line((50, 0, 35, 15), fill = ImageColor.getrgb("black"))
draw.line((50, 0, 65, 15), fill = ImageColor.getrgb("black"))
draw.line((we, hg*0.5, we-15, hg*0.5 + 15), fill = ImageColor.getrgb("black"))
draw.line((we, hg*0.5, we-15, hg*0.5 - 15), fill = ImageColor.getrgb("black"))

nac = int(input("Input start value for 3 task: "))
kon = int(input("Input end value for 3 task: ")) + 20
step = int(input("Input step for 3 task: "))
step_m = []


# loop for 3 ex
a = 45
for v in range(nac, kon, step):
    while co_y (time, v, a) >= 0:
        draw.point(((co_x(time, v, a) / 5) + 50, (co_y(time, v, a) / -5) + 500), 
                   fill = ImageColor.getcolor(color, "RGB"))
        all_grap.append(Corner(co_x(time, v, a), a))
        time += 0.01
    if co_x(time, v, a) > max_s:
        max_s = co_x(time, v, a)
        true_a = a
    if int(co_x(time, v, a)) not in step_m:
        xy = 500
    else:
        xy = 520
    cor = str(v) + " km/s"
    draw.text (((co_x(time, v, a) / 5) + 50, (co_y(time, v, a) / -5) + xy),
                cor,  fill = ImageColor.getrgb("blue"))

    step_m.append(int(co_x(time, v, a)))

    time = 0
    color = ("#%02X%02X%02X" % (ran(), ran(), ran()))
k = 'Answer to the task number 3 = ' + str(true_a)
draw.text((750, 50), k, fill = ImageColor.getrgb("blue"), font = font)
draw.rectangle((735, 35, 995, 90), outline = ImageColor.getrgb("black"), width = 3)

image.save("tra_3.png", "png")
image.show("tra_3.png")