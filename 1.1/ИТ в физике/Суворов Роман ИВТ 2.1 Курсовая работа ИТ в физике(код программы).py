from PIL import Image, ImageColor, ImageDraw, ImageFont
import math


MaxLoad = int(input('Введите максимальную нагрузку на цепь: '))
Corner = 90 - int(input('Введите угол: '))
b = 90 - Corner
HelpMas = {b}
EndCalculations = MaxLoad
n = []
for i in range(1, EndCalculations):
    if (((3 * i - MaxLoad) / (2 * i))) >= -1:
        n.append(i) 
        break 
if len(n) == 0:
    print('При заданных значениях нет ни одного возможного примера массы')
    input()
    exit(0)
StartCalculations = n[0]

print('При заданных значениях будет рассматриваться масса груза от ',
        StartCalculations, ' до ', EndCalculations, '\n так как если взать значения меньше минимального,\n',
      'то для груза приумлем любой градус, а если больше то груз сразу упадет.')
input()


we = 1000
hg = 1000
font = ImageFont.truetype("calibri", 20)
image = Image.new("RGB", (we, hg))
draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, we, hg), fill = 
               ImageColor.getrgb("white"))
draw.line((100, 0, 100, 1000), fill = ImageColor.getrgb('black'))
    
def var(m, c):
    return (math.acos(((3 * m - c) / (2 * m)))) * 180 / math.pi

def rad(x):
    return x * math.pi / 180


for mas in range(StartCalculations, EndCalculations, 3):
    x = abs(int(var(mas, MaxLoad)))
    fx = 800 * math.cos(rad(x)) + 100
    fy = 800 * math.sin(rad(x)) + 100
    if x in HelpMas:
        ans = mas
        smas = 'Максимальная масса:\n ' + str(ans / 10) + 'кг'
    if x == Corner:
        if math.cos(rad(x)) > 0: 
            draw.line((100, 100, fx , fy), fill = ImageColor.getrgb('red'), width = 5)
            draw.text((fx, fy), smas, fill = ImageColor.getrgb('black'), font = font)
    if x > Corner:
        if math.cos(rad(x)) > 0: 
            draw.line((100, 100, fx, fy), fill = ImageColor.getcolor('#0020c2', 'RGB'))
print('Максимальная масса груза = ', ans, 'Н или ', ans/10, 'кг')


image.save('cur.png', 'PNG')
image.show()
