from math import sqrt
from math import atan2
from math import sin
from math import cos
from math import degrees
from math import pi

def collision_robot_vs_line(robot, line):
    if line.cte_y:
        if line.a0 < robot.x + robot.radius and line.a1 > robot.x - robot.radius and abs(line.b - robot.y) < robot.radius:
            if line.b > robot.y:
                return 0, -3
            elif line.b < robot.y:
                return 0, 3
    else:
        if line.a0 < robot.y + robot.radius and line.a1 > robot.y - robot.radius and abs(line.b - robot.x) < robot.radius:
            if line.b > robot.x:
                return -3, 0
            elif line.b < robot.x:
                return 3, 0
    return 0, 0

def collision_robot_vs_goal(robot, goal):
    dx = robot.x - goal.x
    dy = robot.y - goal.y

    d = sqrt(dx**2 + dy**2)

    if d < robot.radius + goal.radius:
        r = atan2(dy, dx)
        return 3*cos(r), 3*sin(r)

    return 0, 0

def collision_robot_vs_ball(robot, ball):
    delta_x = ball.x - robot.x
    delta_y = robot.y - ball.y

    distance = sqrt(delta_x**2 + delta_y**2)

    if distance < robot.radius + ball.radius:
        reaction_angle = atan2(delta_y, delta_x)

        ball_speed = sqrt(ball.speed_x**2 + ball.speed_y**2)
        ball_angle = atan2(ball.speed_y, ball.speed_x)

        ball_speed_reaction_cos = ball_speed * cos(ball_angle-reaction_angle) + 1
        ball_speed_reaction_sin = ball_speed * sin(ball_angle-reaction_angle)

        new_ball_speed = sqrt(ball_speed_reaction_cos**2 + ball_speed_reaction_sin**2)
        new_ball_angle = atan2(ball_speed_reaction_sin, ball_speed_reaction_cos) + reaction_angle

        ball.put_in_motion(new_ball_speed, degrees(new_ball_angle))

def collision_ball_vs_goal(ball, goal):
    delta_x = ball.x - goal.x
    delta_y = goal.y - ball.y

    distance = sqrt(delta_x**2 + delta_y**2)
    if distance < ball.radius + goal.radius:
        reaction_angle = atan2(delta_y, delta_x)

        ball_speed = sqrt(ball.speed_x**2 + ball.speed_y**2)
        # ball_angle = atan2(ball.speed_y, ball.speed_x)

        # ball_speed_reaction_cos = ball_speed * cos(ball_angle-reaction_angle)
        # ball_speed_reaction_sin = ball_speed * sin(ball_angle-reaction_angle)

        # new_ball_speed = sqrt(ball_speed_reaction_cos**2 + ball_speed_reaction_sin**2)
        # new_ball_angle = atan2(ball_speed_reaction_sin, ball_speed_reaction_cos) + reaction_angle

        ball.put_in_motion(ball_speed, degrees(reaction_angle))

def collision_ball_vs_line(ball, line):
    if line.cte_y:
        if line.a0 < ball.x + ball.radius and line.a1 > ball.x - ball.radius and abs(line.b - ball.y) < ball.radius:
            ball.speed_y = - ball.speed_y
    else:
        if line.a0 < ball.y + ball.radius and line.a1 > ball.y - ball.radius and abs(line.b - ball.x) < ball.radius:
            ball.speed_x = - ball.speed_x

def collision_robot_vs_robot(robot1, robot2):
    delta_x = robot1.x - robot2.x
    delta_y = robot1.y - robot2.y

    d = sqrt(delta_x**2 + delta_y**2)
    if d < robot1.radius + robot2.radius:
        reaction_angle = atan2(delta_y, delta_x)

        robot2.x += cos(reaction_angle + pi)
        robot2.y += sin(reaction_angle + pi)

        return 2 * cos(reaction_angle), 2 * sin(reaction_angle)

    return 0, 0

def telemetry_collision(tele1, tele2):
    if tele1.x <= tele2.x and tele1.x + 260 >= tele2.x:
        if tele1.y <= tele2.y and tele1.y + 20 + tele1.size * (not(tele1.minimize)) >= tele2.y:
            if tele1.x + 260 - tele2.x < tele1.y + 20 + tele1.size * (not(tele1.minimize)) - tele2.y:
                tele1.x -= 1
                tele2.x += 1
            else:
                tele1.y -= 1
                tele2.y += 1
        if tele2.y <= tele1.y and tele2.y + 20 + tele2.size * (not(tele2.minimize)) >= tele1.y:
            if tele1.x + 260 - tele2.x < tele2.y + 20 + tele2.size * (not(tele2.minimize)) - tele1.y:
                tele1.x -= 1
                tele2.x += 1
            else:
                tele1.y += 1
                tele2.y -= 1
    if tele2.x <= tele1.x and tele2.x + 260 >= tele1.x:
        if tele1.y <= tele2.y and tele1.y + 20 + tele1.size * (not(tele1.minimize)) >= tele2.y:
            if tele2.x + 260 - tele1.x < tele1.y + 20 + tele1.size * (not(tele1.minimize)) - tele2.y:
                tele1.x += 1
                tele2.x -= 1
            else:
                tele1.y -= 1
                tele2.y += 1
        if tele2.y <= tele1.y and tele2.y + 20 + tele2.size * (not(tele2.minimize)) >= tele1.y:
            if tele2.x + 260 - tele1.x < tele2.y + 20 + tele2.size * (not(tele2.minimize)) - tele1.x:
                tele1.x += 1
                tele2.x -= 1
            else:
                tele1.y += 1
                tele2.y -= 1

    if tele1.x < 0:
        tele1.x = 0
    elif tele1.x > 782:
        tele1.x = 782

    if tele2.x < 0:
        tele2.x = 0
    elif tele2.x > 782:
        tele2.x = 782

    if tele1.y < 0:
        tele1.y = 0
    elif tele1.y > 722 - tele1.size * (not(tele1.minimize)):
        tele1.y = 722 - tele1.size * (not(tele1.minimize))

    if tele2.y < 0:
        tele2.y = 0
    elif tele2.y > 722 - tele2.size * (not(tele2.minimize)):
        tele2.y = 722 - tele2.size * (not(tele2.minimize))