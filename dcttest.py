import pygame
from math import cos, pi

pygame.init()
pygame.font.init()

display = pygame.display.set_mode((1440, 800))
clock = pygame.time.Clock()
font = pygame.font.SysFont(pygame.font.get_default_font(), 16)
running = True

image = pygame.image.load("80905.png")

for x in range(image.get_width()):
    for y in range(image.get_height()):
        R, G, B = image.get_at((x, y))[0:3]
        Y = 16 + 65.738 * (R / 256) + 129.057 * (G / 256) + 25.064 * (B / 256)
        image.set_at((x, y), (Y, Y, Y))


for x in range(45):
    for y in range(25):
        if x % 2 == y % 2:
            pygame.draw.rect(display, (5, 5, 5), (x * 32, y * 32, 32, 32))
        else:
            pygame.draw.rect(display, (6, 6, 6), (x * 32, y * 32, 32, 32))

subx, suby = 0, 0


Q = [
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
]


def a(_):
    return 1 / (2 ** 0.5) if _ == 0 else 1


while running:
    # https://en.wikipedia.org/wiki/JPEG#Discrete_cosine_transform

    pygame.display.update()
    clock.tick(1)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    display.blit(image, (0, 0))

    g = [
        [image.get_at((x + subx * 8, y + suby * 8))[0] - 128 for x in range(8)] for y in range(8)
    ]

    for yi, sg in enumerate(g):
        for xi, c in enumerate(sg):
            pygame.draw.rect(display, (c + 128, c + 128, c + 128), (xi * 32 + 288, yi * 32, 32, 32))
            display.set_at((xi + 576 + subx * 8, yi + suby * 8), (c + 128, c + 128, c + 128))

    G = [[
        int(
            (
                0.25 * a(u) * a(v) * sum([sum([
                    g[y][x] * cos((2 * x + 1) * u * pi / 16) * cos((2 * y + 1) * v * pi / 16)
                for y in range(8)]) for x in range(8)])
            )
            / Q[v][u]
        )
    for u in range(8)] for v in range(8)]

    m = lambda _: max(min(_, 255), 0)

    for yi, sg in enumerate(G):
        for xi, c in enumerate(sg):
            pygame.draw.rect(display, (m(abs(c)*10), m(abs(c)*10), m(abs(c)*10)), (xi * 32 + 288, yi * 32 + 288, 32, 32))

            display.blit(font.render(str(c), True, (255, 0, 0)), (xi * 32 + 288, yi * 32 + 288))

    if not (subx == image.get_width() // 8 - 1 and suby == image.get_height() // 8 - 1):
        subx += 1

    if subx == image.get_width() // 8:
        subx = 0
        suby += 1
