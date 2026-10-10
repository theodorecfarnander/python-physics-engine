import pygame
class Ball:
    def __init__(
            self,
            radius: int = 50,
            colour: tuple = (255, 255,255),
            x_pos: float = 0.0,
            y_pos: float = 0.0,
            x_velocity: float = 0.0,
            y_velocity: float = 0.0,
    ) -> None:
        self.colour = colour
        self.radius = radius
        self.x, self.y = x_pos, y_pos
        self.vx, self.vy = x_velocity, y_velocity

    def draw(self, screen):
        pygame.draw.circle(
            surface=screen,
            color=self.colour,
            center=self.position,
            radius=self.radius
        )

    def update(self, screen_x, screen_y, elapsed_time, gravity):
        g = gravity
        wall_left = 0 + self.radius
        wall_right = screen_x -self.radius
        floor = screen_y - self.radius
        remaining_time = elapsed_time
        while remaining_time > 0:
            # Floor collision
            if self.vy > 0:
                distance_floor = floor - self.y

                # Time until ball reaches floor[
                if distance_floor <=0:
                    hit_time = 0
                else:
                    discriminant = self.vy ** 2 + 2 * g * distance_floor
                    hit_time = (-self.vy + discriminant**0.5) / g
                #]

                if 0 <= hit_time <= remaining_time:
                    # Move ball to the exact collision time
                    self.y += self.vy * hit_time + 0.5 * g * hit_time**2
                    self.vy += g * hit_time

                    # Resolve collision
                    self.y = floor
                    self.vy = -self.vy

                    # Account for remaining time after bounce
                    remaining_time -= hit_time
                    continue

            # Wall collision
            if self.vx > 0:
                distance_wall_right = wall_right - self.x

                # Time until ball reaches wall[
                if distance_wall_right <= 0:
                    hit_time = 0
                else:
                    hit_time = distance_wall_right/self.vx
                #]

                if 0 <= hit_time <= remaining_time:
                    # Move ball to the exact collision time
                    self.x += self.vx * hit_time

                    #Resolve collision
                    self.x = wall_right
                    self.vx = -self.vx

                    remaining_time -= hit_time
                    continue

            elif self.vx < 0:
                distance_wall_left = self.x - wall_left

                # Time until ball reaches wall[
                if distance_wall_left <= 0:
                    hit_time = 0
                else:
                    hit_time = distance_wall_left / abs(self.vx)
                # ]

                if 0 <= hit_time <= remaining_time:
                    # Move ball to the exact collision time
                    self.x += self.vx * hit_time

                    # Resolve collision
                    self.x = wall_left
                    self.vx = -self.vx

                    remaining_time -= hit_time
                    continue

                    # No collision: update normally using constant acceleration
            self.y += self.vy * remaining_time + 0.5 * g * remaining_time**2
            self.vy += g * remaining_time
            self.x += self.vx * remaining_time
            remaining_time = 0

    @property
    def position(self) -> tuple[int, int]:
        return round(self.x), round(self.y)

    @property
    def velocity(self)-> tuple[float | int, float | int]:
        return self.vx, self.vy