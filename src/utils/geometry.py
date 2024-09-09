from math import dist, sqrt


def point_to_line_distance(point, line_start, line_end):
    x0, y0 = point
    x1, y1 = line_start
    x2, y2 = line_end

    # Line segment length squared
    line_len_sq = (x2 - x1) ** 2 + (y2 - y1) ** 2
    if line_len_sq == 0:
        return dist(point, line_start)  # Line start and end are the same

    # Projection of point onto the line (parametric equation)
    t = ((x0 - x1) * (x2 - x1) + (y0 - y1) * (y2 - y1)) / line_len_sq

    # Clamp t to be within [0, 1] to ensure the projection is on the segment
    t = max(0, min(1, t))

    # Find the projection point on the line
    proj_x = x1 + t * (x2 - x1)
    proj_y = y1 + t * (y2 - y1)

    # Return the distance between the point and its projection on the line
    return sqrt((x0 - proj_x) ** 2 + (y0 - proj_y) ** 2)
