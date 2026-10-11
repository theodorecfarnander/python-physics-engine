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
    dx = ball_a.x - ball_b.x
    dy = ball_a.y - ball_b.y

    v_rx = ball_a.vx - ball_b.vx
    v_ry = ball_a.vy - ball_b.vy

    radius_sum = ball_a.radius + ball_b.radius

    a = v_rx**2 + v_ry**2
    b = 2 * (dx * v_rx + dy * v_ry)
    c = dx**2 + dy**2 - radius_sum**2

    # Already overlapping or touching:
    if c <= 0:
        return None

    # No relative movement:
    if a == 0:
        return None

    discriminant = b**2 - 4 * a * c

    if discriminant < 0:
        return None

    t1 = (-b - discriminant**0.5) / (2 * a)
    t2 = (-b + discriminant**0.5) / (2 * a)

    # The first root represents initial contact.
    collision_time = min(t1, t2)

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
    dx = ball_a.x - ball_b.x
    dy = ball_a.y - ball_b.y
    distance = (dx**2 + dy**2)**0.5

    return distance <= ball_a.radius + ball_b.radius


def get_collision_normal(ball_a, ball_b):
    dx = ball_a.x - ball_b.x
    dy = ball_a.y - ball_b.y
    distance = (dx**2 + dy**2)**0.5

    if distance == 0:
        return 1, 0

    return dx / distance, dy / distance


def get_relative_velocity_along_normal(ball_a, ball_b):
    relative_vx = ball_a.vx - ball_b.vx
    relative_vy = ball_a.vy - ball_b.vy

    nx, ny = get_collision_normal(ball_a, ball_b)

    return relative_vx * nx + relative_vy * ny


def separate_balls(ball_a, ball_b):
    dx = ball_a.x - ball_b.x
    dy = ball_a.y - ball_b.y
    distance = (dx**2 + dy**2)**0.5

    overlap = ball_a.radius + ball_b.radius - distance
    nx, ny = get_collision_normal(ball_a, ball_b)

    ball_a.x += (overlap / 2) * nx
    ball_a.y += (overlap / 2) * ny

    ball_b.x -= (overlap / 2) * nx
    ball_b.y -= (overlap / 2) * ny


def resolve_collision(ball_a, ball_b):
    relative_speed = get_relative_velocity_along_normal(ball_a, ball_b)

    # Don't apply an impulse if the balls are separating.
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