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

    def draw(self, screen) -> None:
        pygame.draw.circle(
            surface=screen,
            color=self.colour,
            center=self.position,
            radius=self.radius
        )

    def draw_velocity(self, screen) -> None:
        colour = (255, 0, 0) # Red
        scale_factor = 0.1
        start_x, start_y = self.position
        end_x, end_y = (self.x + self.vx*scale_factor), (self.y + self.vy*scale_factor)
        pygame.draw.line(
            screen,
            color = colour,
            start_pos=(start_x, start_y),
            end_pos=(end_x, end_y),
            width=5
        )


    def update(self, screen_x, screen_y, elapsed_time, gravity) -> None:
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
                    if g == 0:
                        hit_time = distance_floor / self.vy
                    else:
                        discriminant = self.vy ** 2 + 2 * g * distance_floor
                        hit_time = (-self.vy + discriminant ** 0.5) / g
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

    def move(self, elapsed_time, gravity):
        self.y += self.vy * elapsed_time + 0.5 * gravity * elapsed_time ** 2
        self.vy += gravity * elapsed_time
        self.x += self.vx * elapsed_time

    def time_to_wall_collision(self, screen_x):
        wall_left = self.radius
        wall_right = screen_x - self.radius

        if self.vx > 0:
            distance = wall_right - self.x
            if distance <= 0:
                return 0
            return distance / self.vx

        elif self.vx < 0:
            distance = self.x - wall_left
            if distance <= 0:
                return 0
            return distance / abs(self.vx)

        return None

    def time_to_floor_collision(self, screen_y, gravity):
        floor = screen_y - self.radius
        distance = floor - self.y

        # Solve:
        # distance = vy*t + 0.5*gravity*t²

        a = 0.5 * gravity
        b = self.vy
        c = -distance

        if gravity == 0:
            if self.vy <= 0:
                return None

            hit_time = distance / self.vy

            if hit_time >= 0:
                return hit_time

            return None

        discriminant = b ** 2 - 4 * a * c

        if discriminant < 0:
            return None

        t1 = (-b - discriminant ** 0.5) / (2 * a)
        t2 = (-b + discriminant ** 0.5) / (2 * a)

        for t in sorted((t1, t2)):
            if t >= 0 and self.vy + gravity * t > 0:
                return t

        return None

    @property
    def position(self) -> tuple[int, int]:
        return round(self.x), round(self.y)

    @property
    def velocity(self)-> tuple[float | int, float | int]:
        return self.vx, self.vy
