import pygame
from ball import Ball

pygame.init()
clock = pygame.time.Clock()
FPS = 60
highest_point = 700
screen_x = 1200
screen_y = 700
g = 700 #pixels/s²
peach = (255, 228, 176)
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Physics Engine")
screen.fill(peach)

colours = {
    "light_blue": (41, 135, 230),
    "pink": (255, 121, 255),
    "light_green": (111, 250, 150)
}

ball_1 = Ball(radius=100, colour=colours["light_blue"], x_pos=600, y_pos=300, x_velocity=-100, y_velocity=0)
ball_2 = Ball(radius=100, colour=colours["pink"], x_pos=100, y_pos=300, x_velocity=100, y_velocity=0)
ball_3 = Ball(radius=10, colour=colours["light_green"], x_pos=1000, y_pos=400, x_velocity=0, y_velocity=0)

physics_objects = [ball_1, ball_2, ball_3]

def check_collision(ball_a, ball_b):
    distance = ( (ball_a.x - ball_b.x)**2 + (ball_a.y - ball_b.y)**2 )**0.5
    r = ball_a.radius + ball_b.radius
    if distance <= r:
        return True
    else:
        return False

def get_collision_normal(ball_a, ball_b):
    dx = ball_a.x - ball_b.x
    dy = ball_a.y - ball_b.y
    d = (dx**2 + dy**2) ** 0.5
    nx = dx/d
    ny = dy/d
    return nx, ny

def get_relative_velocity_along_normal(ball_a, ball_b):
    v_relative_x = ball_a.vx - ball_b.vx
    v_relative_y = ball_a.vy - ball_b.vy
    nx, ny = get_collision_normal(ball_a, ball_b)
    s = v_relative_x*nx + v_relative_y*ny
    return s # s < 0 balls are approaching, s > 0 balls are separating, s = there is no relative movement along the collision normal

def separate_balls(ball_a, ball_b):
    dx = ball_a.x - ball_b.x
    dy = ball_a.y - ball_b.y
    d = (dx ** 2 + dy ** 2) ** 0.5
    overlap = ball_a.radius + ball_b.radius - d
    nx, ny = get_collision_normal(ball_a, ball_b)
    ball_a.x = ball_a.x + (overlap / 2)*nx
    ball_a.y = ball_a.y + (overlap / 2) * ny
    ball_b.x = ball_b.x - (overlap / 2) * nx
    ball_b.y = ball_b.y - (overlap / 2) * ny

def resolve_collision(ball_a, ball_b):
    s = get_relative_velocity_along_normal(ball_a, ball_b)

    if s >= 0:
        return

    nx, ny = get_collision_normal(ball_a, ball_b)
    j = -s

    ball_a.vx = ball_a.vx + j*nx
    ball_a.vy = ball_a.vy + j*ny

    ball_b.vx = ball_b.vx - j*nx
    ball_b.vy = ball_b.vy - j*ny



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(FPS)
    elapsed_time = dt / 1000

    screen.fill(peach)

    for i in range(len(physics_objects)):
        for j in range(i+1, len(physics_objects)):
            ball_a = physics_objects[i]
            ball_b = physics_objects[j]
            collision = check_collision(ball_a, ball_b)
            if collision == True:
                resolve_collision(ball_a, ball_b)
                separate_balls(ball_a, ball_b)


    for physics_object in physics_objects:
        physics_object.update(screen_x, screen_y, elapsed_time, g)
        physics_object.draw(screen)

    pygame.display.flip()


pygame.quit()



