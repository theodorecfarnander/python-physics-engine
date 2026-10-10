import pygame
from ball import Ball

pygame.init()
clock = pygame.time.Clock()
FPS = 60
highest_point = 700
screen_x = 1200
screen_y = 700
g = 200 #pixels/s²
peach = (255, 228, 176)
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Physics Engine")
screen.fill(peach)

ball = Ball(radius=50, colour=(41, 135, 230), x_pos=600, y_pos=350, x_velocity=550, y_velocity=200)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(FPS)
    elapsed_time = dt / 1000
    screen.fill(peach)

    ball.update(screen_x, screen_y, elapsed_time, g)
    ball.draw(screen)

    pygame.display.flip()


pygame.quit()



