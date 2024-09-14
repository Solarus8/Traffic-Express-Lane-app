from math import dist, sqrt


def point_to_line_distance(point, line_start, line_end):
    # https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
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


def is_point_in_triangle(p, a, b, c):
    # Function to calculate the signed area of a triangle (with vertices in 2D)
    def signed_area(p1, p2, p3):
        return 0.5 * (
            (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])
        )

    # Calculate areas of the triangles formed by (p, a, b), (p, b, c), and (p, c, a)
    area_total = abs(signed_area(a, b, c))
    area1 = abs(signed_area(p, b, c))
    area2 = abs(signed_area(p, a, c))
    area3 = abs(signed_area(p, a, b))

    # If the sum of area1, area2, and area3 equals the total area, the point lies within the triangle
    return (
        abs(area_total - (area1 + area2 + area3)) < 1e-9
    )  # Account for floating-point precision


def is_point_in_quadrilateral(point, quad):
    """
    Check if the given point is inside a quadrilateral.
    Arguments:
    - point: a tuple (x, y) representing the point.
    - quad: a list of 4 tuples, each representing the vertices of the quadrilateral in order.

    Returns:
    - True if the point is inside the quadrilateral, False otherwise.
    """
    if len(quad) != 4:
        raise ValueError("The quadrilateral must have exactly 4 vertices")

    # Split the quadrilateral into two triangles (quad[0], quad[1], quad[2]) and (quad[0], quad[2], quad[3])
    return is_point_in_triangle(
        point, quad[0], quad[1], quad[2]
    ) or is_point_in_triangle(point, quad[0], quad[2], quad[3])
