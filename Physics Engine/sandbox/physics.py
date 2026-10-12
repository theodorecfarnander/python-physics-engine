from ball import Ball

def find_earliest_event(events):
    valid_events = [
        event for event in events
        if event[0] is not None and event[0] >= 0
    ]

    if not valid_events:
        return None

    return min(valid_events, key=lambda event: event[0])

def get_ball_collision_events(physics_objects, max_time):
    events = []

    for i in range(len(physics_objects)):
        for j in range(i + 1, len(physics_objects)):
            ball_a = physics_objects[i]
            ball_b = physics_objects[j]

            collision_time = get_collision_time(
                ball_a, ball_b, max_time
            )

            if collision_time is not None:
                events.append(
                    (collision_time, "ball", (ball_a, ball_b))
                )

    return events

def get_collision_time(ball_a, ball_b, max_time):
    """
    get_collision_time() takes inputs ball_a, ball_b, max_time

    This function aims to work out the time until collision between 2 balls
        - Firstly we check whether the 2 balls are already touching or overlapping, c > 0
        - The balls are checked to see whether they have any relative movement, a != 0
        - The balls are then checked to see if they will collide, D >= 0
        - The collision is checked to see if it will happen within the next frame, 0 <= collision_time <= max_time
        - The balls are finally checked to see if they are approaching each other, b < 0
    If all conditions pass the collision time will be returned otherwise None will be returned
    """
    # Find the x and y difference of the coordinates of the centers of ball_a an ball_b
    dx = ball_a.x - ball_b.x
    dy = ball_a.y - ball_b.y
    # Work out the relative velocity between ball_a and ball_b
    v_rx = ball_a.vx - ball_b.vx
    v_ry = ball_a.vy - ball_b.vy
    # The sum of the radius of ball_a and _b this represents the distance at which ball_a and _b touch
    radius_sum = ball_a.radius + ball_b.radius

    # Pythagoras Theorem a²+b²=c²
    # dx²+dy²=(distance between ball_a and ball_b)²
    # dx and dy are changing due do velocity
    # future dx = current dx + v*t
    # future dy = current dy + v*t
    # radius_sum = R
    # use relative v as we want to see how the distance between the balls change
    # dxₙ=dxₒ+vᵣₓt, dyₙ=dyₒ+vᵣᵧt
    # (dxₙ)²+(dyₙ)²=(Some distance in the future)²
    # We are trying to predict time until collsion so we set future distance to R to find the exact collision point
    # (dx+vᵣₓt)²+(dy+vᵣᵧt)²=R²
    # expand and simplify bringing R² to the left
    # (vᵣₓ² + vᵣᵧ²)t² + 2(dx*vᵣₓ + dx*vᵣᵧ)t + (dx² + dy² - R²) = 0
    # at² + bt + c = 0
    # a = vᵣₓ² + vᵣᵧ²
    # b = 2(dx*vᵣₓ + dx*vᵣᵧ)
    # c = dx² + dy² - R²

    a = v_rx**2 + v_ry**2
    b = 2 * (dx * v_rx + dy * v_ry)
    c = dx**2 + dy**2 - radius_sum**2

    # c = dx² + dy² - R²
    # dx² + dy² = distance² = d²
    # c = d² - R²
    # if c = 0, the distance = R the balls are touching so are ignored as we wish to predict time of future collisions
    # if c < 0, the distance < R the balls are overlapping so are ignored as we wish predict time of future collisions
    # if c > 0, the distance > R the balls have not touched
    # We only care if the balls have not touched
    if c <= 0:
        return None

    # a = vᵣₓ² + vᵣᵧ²
    # if a = 0 than both relative velocities, vᵣₓ² and vᵣᵧ², must be = 0 meaning the balls have no relative movement
    # and collisions cannot be predicted
    if a == 0:
        return None

    # t = (-b±√(b² - 4ac))/2a
    # D = discriminant = b² - 4ac
    # if D < 0 there are no real solutions, the balls do not collide
    # if D >= 0 the balls may collide
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return None
    # t1 = (-b - √D)/2a
    # t2 = (-b + √D)/2a
    t1 = (-b - discriminant**0.5) / (2 * a)
    t2 = (-b + discriminant**0.5) / (2 * a)

    # One time is when the balls first touch, the other is when they pass and stop touching we want the shorter time
    # as it represents the first point of contact
    collision_time = min(t1, t2)

    # Checks the balls will collide within the next frame
    if 0 <= collision_time <= max_time:

        # Ensure the balls are approaching, not separating.
        if b < 0:
            return collision_time

    return None

def get_all_events(physics_objects, screen_x, screen_y, gravity, max_time):
    events = get_ball_collision_events(physics_objects, max_time)

    for ball in physics_objects:
        wall_time = ball.time_to_wall_collision(screen_x)

        if wall_time is not None and wall_time <= max_time:
            events.append((wall_time, "wall", ball))

        floor_time = ball.time_to_floor_collision(screen_y, gravity)

        if floor_time is not None and floor_time <= max_time:
            events.append((floor_time, "floor", ball))

    return events

def resolve_event(event, screen_x, screen_y):
    event_time, event_type, objects = event

    if event_type == "ball":
        ball_a, ball_b = objects

        resolve_collision(ball_a, ball_b)

        if check_collision(ball_a, ball_b):
            separate_balls(ball_a, ball_b)

    elif event_type == "wall":
        ball = objects

        # Place the ball exactly against the wall.
        if ball.vx > 0:
            ball.x = screen_x - ball.radius
        else:
            ball.x = ball.radius

        # Reverse horizontal velocity.
        ball.vx = -ball.vx

    elif event_type == "floor":
        ball = objects

        # Place the ball exactly on the floor.
        ball.y = screen_y - ball.radius

        # Reverse vertical velocity.
        ball.vy = -ball.vy

def check_collision(ball_a, ball_b):
    """
    check_collisions() takes inputs ball_a and ball_b

    check_collisions() checks whether 2 balls are colliding
        - If the 2 balls are touching they are colliding so returns True
        - If the 2 balls are overlapped they are colliding returns True
        - If the 2 balls are not touching or not overlapped they are not colliding returns False
    The 2 balls distance is calculated this is then used with each balls radius to determine whether they are colliding
    or not.
    check_collision() can only check if 2 balls are currently colliding and cannot predict if they will latter.
    """
    # Finds the difference between ball_a and ball_b x-positions, if the result is negative ball_a is to the left of _b
    dx = ball_a.x - ball_b.x
    # Finds the difference between ball_a and ball_b y-positions, if the result is negative ball_a is to the above of _b
    dy = ball_a.y - ball_b.y
    # The results leave's us with a right-angled triangle with ball_a at one corner and _b at another and dx, dy being the straight edges, the hypotenuse being the distance from both balls
    # Uses pythagoras theorem to find the distance between the 2 balls, c²=b²+a², distance² = dx² + dy²
    distance = (dx**2 + dy**2)**0.5
    # If the distance between the balls is the same as the sum of their radius the 2 balls are touching returns True
    # If the distance between the balls is less than the sum of their radius the 2 balls are overlapping returns True
    # If the distance between the balls is more than the sum of their radius they are not touching returns False
    return distance <= ball_a.radius + ball_b.radius

def get_collision_normal(ball_a, ball_b):
    """
    get_collision_normal() works out the normal between the collision of balls _a and _b
    the normal is a unit vector describing the displacement of ball_a's center relative to ball_b's center.
    the normal is (1, 0) by default if the 2 balls are in the exact same location to prevent divide by 0 error.
    """

    # Works out the vector (dx, dy) which describes the size and direction of ball_a from ball_b
    dx = ball_a.x - ball_b.x
    dy = ball_a.y - ball_b.y

    # Works out the size of the vector (dx, dy) to normalize the vector and prevent a divide by 0 error
    distance = (dx**2 + dy**2)**0.5
    # If distance == 0 than the balls are at the same place we cannot work out the direction using this so force ball_a to the right of _b, this is a fallback and does not accurately represent the direction
    if distance == 0:
        return 1, 0
    # Returns the normal as a unit vector
    return dx / distance, dy / distance

def get_relative_velocity_along_normal(ball_a, ball_b):
    """
    get_relative_velocity_along_normal() takes the inputs ball_a and ball_b
    This function works out whether 2 balls are moving towards or away from each other along the line between their centers.
    *
    """
    # Subtract ball_a and ball_b velocities to work out their relative velocity
    relative_vx = ball_a.vx - ball_b.vx
    relative_vy = ball_a.vy - ball_b.vy

    # Find the normal
    nx, ny = get_collision_normal(ball_a, ball_b)

    # returns the dot product of the normal and the relative velocity
    return relative_vx * nx + relative_vy * ny

def separate_balls(ball_a, ball_b):
    """
    separate_balls() takes the inputs ball_a and ball_b
    separate_balls() is called when a collision is detected between 2 balls
        - the difference between the balls x and y coordinates are found to give dx, dy
        - dx and dy are used in pythagoras theorem to work out the distance between these balls
        - the overlap is than calculated if the balls are just touching and not overlapping the overlap is 0
        - each ball is adjusted by half the overlap * the normal this ensures the adjustment is done in the right place
        and that the adjustment is uniform so both balls are displaced by the same amount
    """
    # Work out difference between the balls x and y values to get dx and dy
    dx = ball_a.x - ball_b.x
    dy = ball_a.y - ball_b.y

    # Work out distance between ball_a and _b using pythagoras theorem and their x and y distances
    distance = (dx**2 + dy**2)**0.5

    # Works out the difference between the balls distance and the sum of their radius if the result is >0 they are overlapping
    overlap = ball_a.radius + ball_b.radius - distance
    nx, ny = get_collision_normal(ball_a, ball_b)

    # Adjust ball a's x and why value by half the overlap, this is multiplied by the normal which says where the correction should take place
    ball_a.x += (overlap / 2) * nx
    ball_a.y += (overlap / 2) * ny
    # Adjust ball b's x and why value by other half of the overlap, this is multiplied by the normal which says where the correction should take place
    ball_b.x -= (overlap / 2) * nx
    ball_b.y -= (overlap / 2) * ny

def resolve_collision(ball_a, ball_b):
    relative_speed = get_relative_velocity_along_normal(ball_a, ball_b)

    # A speed of 0 or less means the balls are not moving towards each other
    if relative_speed >= 0:
        return

    nx, ny = get_collision_normal(ball_a, ball_b)

    impulse = -relative_speed

    ball_a.vx += impulse * nx
    ball_a.vy += impulse * ny

    ball_b.vx -= impulse * nx
    ball_b.vy -= impulse * ny

def simulate_step(physics_objects, screen_x, screen_y, gravity, elapsed_time):
    remaining_time = elapsed_time
    event_count = 0
    max_events = 1000

    while remaining_time > 1e-10 and event_count < max_events:

        # Find all collisions that could happen during this interval.
        events = get_all_events(
            physics_objects,
            screen_x,
            screen_y,
            gravity,
            remaining_time
        )

        # Select the earliest collision.
        earliest_event = find_earliest_event(events)

        # No collision: advance every ball through the remaining time.
        if earliest_event is None:
            for ball in physics_objects:
                ball.move(remaining_time, gravity)

            remaining_time = 0

        else:
            collision_time = earliest_event[0]

            # Advance every ball to the collision.
            if collision_time > 0:
                for ball in physics_objects:
                    ball.move(collision_time, gravity)

                remaining_time -= collision_time

            # Resolve the collision at the impact position.
            resolve_event(earliest_event, screen_x, screen_y)

            event_count += 1

    if event_count >= max_events:
        print("Warning: maximum collision events reached.")