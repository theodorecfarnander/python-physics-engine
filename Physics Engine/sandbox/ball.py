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
            border: int = 0
    ) -> None:

        self.colour = colour
        self.radius = radius
        self.x, self.y = x_pos, y_pos
        self.vx, self.vy = x_velocity, y_velocity
        self.border = border
        self.resting_on_floor = False

    def draw(self, screen) -> None:
        pygame.draw.circle(
            surface=screen,
            color=self.colour,
            center=self.position,
            radius=self.radius,
            width=self.border,
        )

    def draw_velocity(self, screen) -> None:
        """
        draw_velocity() paints the velocity of the ball as a line starting at the balls centre
        :param screen:
        :return:
        """
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

    def move(self, elapsed_time, gravity) -> None:
        """
        move() takes elapsed_time (time) and gravity as inputs.

        move() does 3 main things:
            1) updates the balls y position using s=u+(1/2)g*t*t to work out displacement then adding the result to current position
            2) updates the balls y velocity using v=gt+u, u being the current velocity
            3) updates the balls x position using s=v*t
        """
        self.x += self.vx * elapsed_time

        # Vertical motion only occurs when not resting on the floor.
        if not self.resting_on_floor:
            self.y += self.vy * elapsed_time + 0.5 * gravity * elapsed_time ** 2
            self.vy += gravity * elapsed_time




    def time_to_wall_collision(self, screen_x):
        """
        time_to_wall_collision() takes screen_x as an input
        time_to_wall_collision() predicts when the ball will come in contact with either the left wall or the right
        by calculating the balls distance from the wall and using that with its constant velocity in s=vt to predict
        the time it will take for the ball to cover that distance and touch the wall.
        """

        # Wall left is the x value at which the ball is touching the left wall, wall right is the x value at which
        # the ball is touching the right wall
        wall_left = self.radius
        wall_right = screen_x - self.radius

        # If the velocity is + the ball is moving towards the right wall
        if self.vx > 0:
            # Checks how far the ball is currently from where it needs to be touching the right wall
            distance = wall_right - self.x
            # If the distance is <= 0 it means the ball is currently touching or overlapping the wall so time to collision
            # is 0
            if distance <= 0:
                return 0
            # Otherwise the ball is not yet touching the wall, and we use s=vt to work out the time it will touch the ball
            return distance / self.vx

        # If the velocity is + the ball is moving towards the right wall
        elif self.vx < 0:
            # Checks how far the ball is currently from where it needs to be touching the left wall
            distance = self.x - wall_left
            # If the distance is <= 0 it means the ball is currently touching or overlapping the wall so time to collision
            # is 0
            if distance <= 0:
                return None

            # Otherwise the ball is not yet touching the wall, and we use s=vt to work out the time it will touch the ball
            return distance / abs(self.vx) # Moving to the left is a - velocity which is why we use abs()

        return None

    def time_to_floor_collision(self, screen_y, gravity):
        """
        time_to_floor_collision() takes the inputs screen_y, gravity
        time_to_floor_collision() aims to calculate the time until the ball makes contact with the floor
        if the ball is heading towards the floor and *

        """
        # floor is the y value at which the ball is touches the floor
        floor = screen_y - self.radius
        # distance is how far the ball is from the collision y coordinate with the floor
        distance = floor - self.y

        # s = vt + (1/2)gt² - see move()
        # (1/2)gt² + vt - s = 0
        # at² + bt + c = 0
        # a = (1/2)g
        # b = v
        # c = -s
        a = 0.5 * gravity
        b = self.vy
        c = -distance

        # if gravity == 0 there is no acceleration and the ball moves at a constant velocity so we use the constant velocity
        # equation s=vt, t=s/v
        if gravity == 0:
            # if the velocity is 0 or - it means that the ball is moving away from the floor so we return None
            if self.vy <= 0:
                return None
            # Calculate the hit time using t=s/v
            hit_time = distance / self.vy

            if hit_time >= 0:
                return hit_time

            return None

        # Use the discriminant to find if there are solutions
        discriminant = b ** 2 - 4 * a * c
        # If discriminant < 0 it means there are no real solutions
        if discriminant < 0:
            return None

        # Find the solutions of t
        t1 = (-b - discriminant ** 0.5) / (2 * a)
        t2 = (-b + discriminant ** 0.5) / (2 * a)

        # the first condition t >= 0 checks that the collision is in the future, the second, self.vy + gravity * t > 0
        # checks that the ball is moving towards the floor
        # we use sorted because we want to find the earliest collision with a valid time
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
