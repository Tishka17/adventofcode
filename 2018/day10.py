from dataclasses import dataclass

from PIL import Image


@dataclass
class P:
    x: int
    y: int
    vx: int
    vy: int

    def move(self, k=1):
        self.x += self.vx * k
        self.y += self.vy * k


points = []
maxx, maxy = 512, 512

with open("in10.txt") as f:
    for s in f:
        x, v = s.split('<')[1:]
        x, y = x.split('>')[0].split(',')
        v, w = v.split('>')[0].split(',')
        p = P(int(x), int(y), int(v), int(w))
        points.append(p)


def draw():
    f = 0
    img = Image.new('RGB', (maxx, maxy))
    for p in points:
        x, y = p.x + 50, p.y + 50
        if maxx > x > 0 and maxy > y > 0:
            img.putpixel((x, y), 0xffffff)
    f = 1
    if f:
        # img.save('/sdcard/src/img.png')
        return img


images = []

for x in range(1022):
    for p in points:
        p.move(10)

for x in range(80):
    img = draw()
    if img:
        print('img')
        images.append(draw())
    for p in points:
        p.move(1)

images[0].save(
    'o.gif',
    save_all=True,
    append_images=images[1:],
    duration=100,
    loop=1
)
