from math import hypot

def collide(r1, r2):
    """ Tests whether two robots overlap
        If they do, stop both """

    dx = r1.x - r2.x
    dy = r1.y - r2.y

    dist = hypot(dx, dy)
    if dist < r1.radius + r2.radius:
        return True