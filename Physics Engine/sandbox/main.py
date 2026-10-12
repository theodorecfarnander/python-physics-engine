import pygame
from ball import Ball
from physics import (
    find_earliest_event,
    get_collision_time,
    get_all_events,
    check_collision,
    resolve_collision,
    separate_balls,
    simulate_step,
)

pygame.init()
clock = pygame.time.Clock()
FPS = 60
highest_point = 700
screen_x = 2700
screen_y = 1500
g = 700 #pixels/s²
light_mode = (255, 228, 176)
dark_mode = (82, 82, 82)
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Physics Engine")
screen.fill(dark_mode)

colours = {
    "light_blue": (41, 135, 230),
    "pink": (255, 121, 255),
    "light_green": (111, 250, 150)
}

ball_1 = Ball(
    radius=100,
    colour=colours["light_blue"],
    x_pos=100,
    y_pos=340,
    x_velocity=1512,
    y_velocity=0
)

ball_2 = Ball(
    radius=100,
    colour=colours["pink"],
    x_pos=2500,
    y_pos=300,
    x_velocity=-10,
    y_velocity=50
)
ball_3 = Ball(radius=100, x_pos=800, y_pos=-50, x_velocity=-50, y_velocity=-50)
ball_4 = Ball(radius=100, colour=colours["light_green"], x_pos=800, y_pos=-50, x_velocity=-50, y_velocity=-50)
ball_5 = Ball(radius=100, colour=colours["light_green"], x_pos=800, y_pos=-50, x_velocity=-50, y_velocity=-50)
ball_6 = Ball(radius=100, colour=colours["light_green"], x_pos=800, y_pos=-50, x_velocity=-50, y_velocity=-50)
physics_objects = [ball_1, ball_2, ball_3, ball_4, ball_5, ball_6]


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(FPS)
    elapsed_time = dt / 1000

    screen.fill(dark_mode)


    for i in range(len(physics_objects)):
        for j in range(i+1, len(physics_objects)):
            ball_a = physics_objects[i]
            ball_b = physics_objects[j]
            collision = check_collision(ball_a, ball_b)
            if collision == True:
                get_collision_time(ball_a, ball_b, elapsed_time)
                resolve_collision(ball_a, ball_b)
                separate_balls(ball_a, ball_b)

    simulate_step(
        physics_objects,
        screen_x,
        screen_y,
        g,
        elapsed_time
    )

    for physics_object in physics_objects:
        physics_object.draw(screen)
        physics_object.draw_velocity(screen)

    pygame.display.flip()


pygame.quit()



