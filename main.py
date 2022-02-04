import pygame


COLOR_DOWNSAMPLE = 2


pygame.init()

image = pygame.image.load("80905.png")

display = pygame.display.set_mode((1440, 864))
clock = pygame.time.Clock()
running = True

ysur = pygame.Surface((256, 256))
cbsur = pygame.Surface((128, 128))
crsur = pygame.Surface((128, 128))

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    for x in range(45):
        for y in range(27):
            if x % 2 == y % 2:
                pygame.draw.rect(display, (5, 5, 5), (x * 32, y * 32, 32, 32))
            else:
                pygame.draw.rect(display, (6, 6, 6), (x * 32, y * 32, 32, 32))

    display.blit(image, (0, 0))

    for x in range(image.get_width()):
        for y in range(image.get_height()):
            R, G, B = image.get_at((x, y))[0:3]

            display.set_at((x + 288, y), (R, 0, 0))
            display.set_at((x + 288, y + 288), (0, G, 0))
            display.set_at((x + 288, y + 576), (0, 0, B))

            Y = 16 + 65.738 * (R / 256) + 129.057 * (G / 256) + 25.064 * (B / 256)

            if x % COLOR_DOWNSAMPLE and y % COLOR_DOWNSAMPLE:
                try:
                    R, G, B = [sum(n) / len(n) for n in list(zip(
                        *[image.get_at((x + _x, y + _y))[0:3] for _x in range(COLOR_DOWNSAMPLE) for _y in range(COLOR_DOWNSAMPLE)]
                    ))]
                except IndexError:
                    ...

                Cb = 128 - 37.945 * (R / 256) - 74.494 * (G / 256) + 112.439 * (B / 256)
                Cr = 128 + 112.439 * (R / 256) - 94.154 * (G / 256) - 18.285 * (B / 256)

                cbsur.set_at((x // COLOR_DOWNSAMPLE, y // COLOR_DOWNSAMPLE), (Cb, Cb, Cb))
                crsur.set_at((x // COLOR_DOWNSAMPLE, y // COLOR_DOWNSAMPLE), (Cr, Cr, Cr))

            ysur.set_at((x, y), (Y, Y, Y))

    display.blit(ysur, (576, 0))
    display.blit(cbsur, (576, 288))
    display.blit(crsur, (576, 576))

    for x in range(image.get_width()):
        for y in range(image.get_height()):
            Y = ysur.get_at((x, y))[0]
            Cb = cbsur.get_at((x // COLOR_DOWNSAMPLE, y // COLOR_DOWNSAMPLE))[0]
            Cr = crsur.get_at((x // COLOR_DOWNSAMPLE, y // COLOR_DOWNSAMPLE))[0]

            R = 298.082 * (Y / 256) + 408.583 * (Cr / 256) - 222.921
            G = 298.082 * (Y / 256) - 100.291 * (Cb / 256) - 208.120 * (Cr / 256) + 135.576
            B = 298.082 * (Y / 256) + 516.412 * (Cb / 256) - 276.836

            R = min(max(0, R), 255)
            G = min(max(0, G), 255)
            B = min(max(0, B), 255)

            display.set_at((x + 864, y), (R, G, B))

    pygame.display.update()
    clock.tick(30)
