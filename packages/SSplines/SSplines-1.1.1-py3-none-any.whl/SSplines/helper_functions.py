import numpy as np


def barycentric_coordinates(triangle, x, tol=1.0e-14):
    """
    Computes the barycentric coordinates of a point x with respect to the given triangle.
    :param np.ndarray triangle: vertices of triangle
    :param np.ndarray x:
    :param float tol: tolerance used for removing round of errors in computation
    :return np.ndarray: barycentric_coordinates
    """

    p1, p2, p3 = triangle

    area_triangle = signed_area(triangle)
    b2 = signed_area([p1, x, p3]) / area_triangle
    b3 = signed_area([p1, p2, x]) / area_triangle

    # necessary clamping to avoid false reporting of sub-triangles.
    if abs(b2) < tol:
        b2 = 0
    elif abs(b2 - 1) < tol:
        b2 = 1
    if abs(b3) < tol:
        b3 = 0
    elif abs(b3 - 1) < tol:
        b3 = 1

    b1 = 1 - b2 - b3
    if abs(b1) < tol:
        b1 = 0
    elif abs(b1 - 1) < tol:
        b1 = 1

    return np.array([b1, b2, b3])


def directional_coordinates(vertices, u):
    """
    Returns the directional coordinates of the directional vector u with
    respect to the triangle delineated by supplied vertices.
    :param np.ndarray vertices: (3x2) matrix containing the three vertices
    :param np.ndarray u: array of length two representing a vector
    :return: np.ndarray (a0, a1, a2)
    """
    # u = x1 - x2
    x1 = np.array([u[0], 0])
    x2 = np.array([0, -u[1]])

    b1 = barycentric_coordinates(vertices, x1)
    b2 = barycentric_coordinates(vertices, x2)

    a = b1 - b2

    return a


def signed_area(triangle):
    """
    Computes the signed area of the given triangle.
    :param np.ndarray, list triangle: vertices of triangle
    :return float: signed area of triangle
    """

    p1, p2, p3 = triangle
    s2 = p2 - p1
    s3 = p3 - p1

    return 0.5 * (s2[0] * s3[1] - s2[1] * s3[0])


def area(triangle):
    """
    Computes the unsigned area of the given triangle.
    :param np.ndarray triangle: vertices of triangle
    :return float: unsigned area of triangle
    """

    return abs(signed_area(triangle))


def determine_sub_triangle(triangle, x):
    """
    Determines the integer k such that the point x lies in sub-triangle k of the Powell-Sabin 12-split of the given
    triangle. :param np.ndarray triangle: :param np.ndarray x: :return int: sub-triangle number
    """

    b = barycentric_coordinates(triangle, x)
    index_lookup_table = {38: 0, 46: 0, 39: 1, 19: 2, 17: 3, 8: 4, 25: 4, 12: 5, 6: 6, 7: 7, 3: 8, 1: 9, 0: 10, 4: 11}

    # if any of the coordinates are negative, x lies outside the triangle
    if np.any(b[b < 0]):
        return -1
    else:
        b1, b2, b3 = b
        s = 32 * (b1 > 0.5) + 16 * (b2 >= 0.5) + 8 * (b3 >= 0.5) + 4 * (b1 > b2) + 2 * (b1 > b3) + (b2 >= b3)
        return index_lookup_table[s]


def sub_triangles(triangle):
    """
    Returns a list of the vertices corresponding to the twelve sub-triangles in the Powell-Sabin 12-split of the given
    triangle.
    :param np.ndarray triangle: vertices of triangle
    :return list: list of sets of vertices of sub-triangles
    """
    p = ps12_split_vertices(triangle)

    idx = [[0, 3, 6], [3, 1, 7], [1, 7, 4], [4, 2, 8],
           [2, 5, 8], [5, 6, 0], [6, 3, 9], [3, 9, 7],
           [7, 9, 4], [4, 8, 9], [5, 8, 9], [5, 6, 9]]

    sub_triangle_vertices = []
    for i in idx:
        sub_triangle_vertices.append(p[i])

    return sub_triangle_vertices


def sample_triangle(triangle, d, ret_number=False):
    """
    Returns a set of uniformly spaced points in the triangle. The number of points correspond to the dimension
    of the space of bi-variate polynomials of degree d.
    :param np.ndarray triangle: vertices of triangle
    :param int d: `degree`
    :param boolean ret_number: whether to return the number of points or not
    :return np.ndarray: sampled points
    """

    p1, p2, p3 = triangle
    n = int((1 / 2) * (d + 1) * (d + 2))  # total number of domain points
    points = np.zeros((n, 2), dtype=np.float64)

    m = 0
    for i in range(d + 1):
        for j in range(d - i + 1):
            k = (d - i - j)
            p = (i * p1 + j * p2 + k * p3) / d
            points[m] = p
            m += 1

    if ret_number:
        return points, n

    return points


def evaluate_non_zero_basis_splines(triangle, d, x):
    """
    evaluates the non-zero basis splines of degree d at the point x over
    the Powell-Sabin 12-split of the triangle delineated by vertices.
    :param np.ndarray triangle: vertices of triangle
    :param int d: spline degree
    :param np.ndarray x: point of evaluation
    :return: array of non-zero basis splines evaluated at x.
    """

    k = determine_sub_triangle(triangle, x)
    s = np.array([1])
    R_mat = [r1, r2]
    R = [R_mat[i](triangle, x) for i in range(d)]
    for i in range(d):
        R_sub = sub_matrix(R[i], i + 1, k)
        s = s.dot(R_sub)
    return s


def evaluate_non_zero_basis_derivatives(triangle, d, r, x, u):
    """
    Evaluates the r'th directional derivative of the non-zero basis splines of degree d at point x
    over the Powell-Sabin 12 split of the given triangle.
    :param np.ndarray triangle: vertices of triangle
    :param int d: spline degree
    :param int r: order of derivative
    :param np.ndarray x: point of evaluation
    :param np.ndarray u: direction of differentiation
    :return: array of non-zero directional derivatives evaluated at x
    """
    k = determine_sub_triangle(triangle, x)
    s = np.array([1])
    R_mat = [r1, r2]
    U_mat = [u1, u2]
    R = [R_mat[i](triangle, x) for i in range(d)]
    U = [U_mat[i](triangle, u) for i in range(d)]

    for i in range(d - r):
        R_sub = sub_matrix(R[i], i + 1, k)
        s = s.dot(R_sub)

    for j, i in enumerate(range(d - r, d)):
        U_sub = sub_matrix(U[i], i + 1, k)
        s = (i + 1) * s.dot(U_sub)

    return s


def coefficients_linear(k):
    """
    Returns the indices of coefficients corresponding to non-zero S-splines on
    sub-triangle k
    """
    c1 = {
        0: [0, 5, 6], 1: [0, 3, 6], 2: [1, 3, 7],
        3: [1, 4, 7], 4: [2, 4, 8], 5: [2, 5, 8],
        6: [5, 6, 9], 7: [3, 6, 9], 8: [3, 7, 9],
        9: [4, 7, 9], 10: [4, 8, 9], 11: [5, 8, 9]
    }

    return np.array(c1[k])


def coefficients_quadratic(k):
    """
    Returns the indices of coefficients corresponding to non-zero S-splines on
    sub-triangle k
    """
    c2 = {
        0: [0, 1, 2, 9, 10, 11], 1: [0, 1, 2, 3, 10, 11], 2: [1, 2, 3, 4, 5, 6],
        3: [2, 3, 4, 5, 6, 7], 4: [5, 6, 7, 8, 9, 10], 5: [6, 7, 8, 9, 10, 11],
        6: [1, 2, 6, 9, 10, 11], 7: [1, 2, 3, 6, 10, 11], 8: [1, 2, 3, 5, 6, 10],
        9: [2, 3, 5, 6, 7, 10], 10: [2, 5, 6, 7, 9, 10], 11: [2, 6, 7, 9, 10, 11]
    }
    return np.array(c2[k])


def sub_matrix(matrix, d, k):
    """
    Gets the sub-matrix used in evaluation over sub-triangle k for the S-spline matrix of degree d.
    :param np.ndarray matrix: S-spline matrix of degree 1 or 2
    :param int d: degree 1 or 2
    :param int k: sub triangle
    :return: (1x3) or (3x6) sub-matrix for d = 1, d = 2 respectively.
    """

    c1, c2 = coefficients_linear, coefficients_quadratic

    if d == 1:
        s = matrix[k, c1(k)]
        s = np.reshape(s, (1, 3))
    elif d == 2:
        s = matrix[np.ix_(c1(k), c2(k))]
        s = np.reshape(s, (3, 6))

    return s


def r1(vertices, x):
    """
    Computes the linear evaluation matrix for Splines on the Powell-Sabin
    12-split of the triangle delineated by given vertices, evaluated at x.
    :param vertices: (3x2) matrix of points
    :param x: point of evaluation
    :return: (12x10) linear evaluation matrix.
    """

    B = barycentric_coordinates(vertices, x)
    R = np.zeros((12, 10))
    b = np.zeros((3, 3))  # beta
    g = np.zeros(3)  # gamma

    for i in range(3):
        g[i] = 2 * B[i] - 1
        for j in range(3):
            b[i, j] = B[i] - B[j]

    R[[0, 1], 0] = g[0]
    R[[2, 3], 1] = g[1]
    R[[4, 5], 2] = g[2]

    R[[1, 2, 7, 8], 3] = [2 * b[1, 2], 2 * b[0, 2], 2 * b[1, 2], 2 * b[0, 2]]
    R[[3, 4, 9, 10], 4] = [2 * b[2, 0], 2 * b[1, 0], 2 * b[2, 0], 2 * b[1, 0]]
    R[[0, 5, 6, 11], 5] = [2 * b[2, 1], 2 * b[0, 1], 2 * b[2, 1], 2 * b[0, 1]]
    R[[0, 1, 6, 7], 6] = [4 * B[1], 4 * B[2], 4 * b[0, 2], 4 * b[0, 1]]
    R[[2, 3, 8, 9], 7] = [4 * B[2], 4 * B[0], 4 * b[1, 0], 4 * b[1, 2]]
    R[[4, 5, 10, 11], 8] = [4 * B[0], 4 * B[1], 4 * b[2, 1], 4 * b[2, 0]]
    R[6:, 9] = -3 * np.array([g[0], g[0], g[1], g[1], g[2], g[2]])

    return R


def r2(vertices, x):
    """
    Computes the quadratic evaluation matrix for Splines on the Powell-Sabin
    12-split of the triangle delineated by given vertices, evaluated at x.
    :param vertices: (3x2) matrix of points
    :param x: point of evaluation
    :return: (10x12) quadratic evaluation matrix.
    """

    B = barycentric_coordinates(vertices, x)
    R = np.zeros((10, 12))
    b = np.zeros((3, 3))  # beta
    g = np.zeros(3)  # gamma

    for i in range(3):
        g[i] = 2 * B[i] - 1
        for j in range(3):
            b[i, j] = B[i] - B[j]

    R[0, [0, 1, 11]] = [g[0], 2 * B[1], 2 * B[2]]
    R[1, [3, 4, 5]] = [2 * B[0], g[1], 2 * B[2]]
    R[2, [7, 8, 9]] = [2 * B[1], g[2], 2 * B[0]]
    R[3, [1, 2, 3]] = [b[0, 2], 3 * B[2], b[1, 2]]
    R[4, [5, 6, 7]] = [b[1, 0], 3 * B[0], b[2, 0]]
    R[5, [9, 10, 11]] = [b[2, 1], 3 * B[1], b[0, 1]]
    R[6, [1, 2, 10, 11]] = 0.5 * np.array([b[0, 2], 3 * B[1], 3 * B[2], b[0, 1]])
    R[7, [2, 3, 5, 6]] = 0.5 * np.array([3 * B[0], b[1, 2], b[1, 0], 3 * B[2]])
    R[8, [6, 7, 9, 10]] = 0.5 * np.array([3 * B[1], b[2, 0], b[2, 1], 3 * B[0]])
    R[9, [2, 6, 10]] = [-g[2], -g[0], -g[1]]

    return R


def u1(vertices, u):
    """
    Computes the linear derivative matrix for Splines on the Powell-Sabin
    12-split of the triangle delineated by given vertices in the direction u.
    :param vertices: (3x2) matrix of points
    :param u: directional vector
    :return: (12x10) linear derivative matrix.
    """

    A = directional_coordinates(vertices, u)
    U = np.zeros((12, 10))
    a = np.zeros((3, 3))

    for i in range(3):
        for j in range(3):
            a[i, j] = A[i] - A[j]

    U[[0, 1], 0] = [2 * A[0], 2 * A[0]]
    U[[2, 3], 1] = [2 * A[1], 2 * A[1]]
    U[[4, 5], 2] = [2 * A[2], 2 * A[2]]
    U[[1, 2, 7, 8], 3] = [2 * a[1, 2], 2 * a[0, 2], 2 * a[1, 2], 2 * a[0, 2]]
    U[[3, 4, 9, 10], 4] = [2 * a[2, 0], 2 * a[1, 0], 2 * a[2, 0], 2 * a[1, 0]]
    U[[0, 5, 6, 11], 5] = [2 * a[2, 1], 2 * a[0, 1], 2 * a[2, 1], 2 * a[0, 1]]
    U[[0, 1, 6, 7], 6] = [4 * A[1], 4 * A[2], 4 * a[0, 2], 4 * a[0, 1]]
    U[[2, 3, 8, 9], 7] = [4 * A[2], 4 * A[0], 4 * a[1, 0], 4 * a[1, 2]]
    U[[4, 5, 10, 11], 8] = [4 * A[0], 4 * A[1], 4 * a[2, 1], 4 * a[2, 0]]
    U[[6, 7, 8, 9, 10, 11], 9] = [-6 * A[0], -6 * A[0], -6 * A[1], -6 * A[1], -6 * A[2], -6 * A[2]]

    return U


def u2(vertices, u):
    """
    Computes the quadratic derivative matrix for Splines on the Powell-Sabin
    12-split of the triangle delineated by given vertices in the direction u.
    :param vertices: (3x2) matrix of points
    :param u: directional vector
    :return: (12x10) quadratic derivative matrix.
    """

    A = directional_coordinates(vertices, u)
    U = np.zeros((10, 12))
    a = np.zeros((3, 3))

    for i in range(3):
        for j in range(3):
            a[i, j] = A[i] - A[j]

    U[0, [0, 1, 11]] = [2 * A[0], 2 * A[1], 2 * A[2]]
    U[1, [3, 4, 5]] = [2 * A[0], 2 * A[1], 2 * A[2]]
    U[2, [7, 8, 9]] = [2 * A[1], 2 * A[2], 2 * A[0]]
    U[3, [1, 2, 3]] = [a[0, 2], 3 * A[2], a[1, 2]]
    U[4, [5, 6, 7]] = [a[1, 0], 3 * A[0], a[2, 0]]
    U[5, [9, 10, 11]] = [a[2, 1], 3 * A[1], a[0, 1]]
    U[6, [1, 2, 10, 11]] = 0.5 * np.array([a[0, 2], 3 * A[1], 3 * A[2], a[0, 1]])
    U[7, [2, 3, 5, 6]] = 0.5 * np.array([3 * A[0], a[1, 2], a[1, 0], 3 * A[2]])
    U[8, [6, 7, 9, 10]] = 0.5 * np.array([3 * A[1], a[2, 0], a[2, 1], 3 * A[0]])
    U[9, [2, 6, 10]] = [-2 * A[2], -2 * A[0], -2 * A[1]]

    return U


def ps12_split_vertices(vertices):
    """
    Returns the set of 10 vertices in the PS12-split of triangle.
    :param np.ndarray vertices:
    :return:
    """
    p0, p1, p2 = vertices

    p = np.zeros(shape=(10, 2))
    # corners
    p[0, :] = p0
    p[1, :] = p1
    p[2, :] = p2

    # midpoints
    p[3, :] = 0.5 * (p0 + p1)
    p[4, :] = 0.5 * (p1 + p2)
    p[5, :] = 0.5 * (p2 + p0)

    # interior
    p[6, :] = 0.5 * (p[3] + p[5])
    p[7, :] = 0.5 * (p[3] + p[4])
    p[8, :] = 0.5 * (p[4] + p[5])

    # center
    p[9, :] = (1.0 / 3.0) * (p0 + p1 + p2)

    return p


def sspline_to_hermite(vertices):
    """
    Returns the change of basis matrix from quadratic S-basis to quadratic Hermite basis.
    :param np.ndarray vertices: vertices of triangle.
    :return: change of basis matrix.
    """

    def projection(i, j, k):
        """
        Returns the projection of p_j - p_k in the direction of p_i - p_j.
        :param i: p_i
        :param j: p_j
        :param k: p_k
        :returns:
        """

        return (i - j).T.dot(j - k) / (i - j).T.dot(i - j)

    A = np.zeros((12, 12))
    d = 2 * signed_area(vertices)

    [x1, y1], [x2, y2], [x3, y3] = vertices
    p1, p2, p3, p4, p5, p6, *_ = ps12_split_vertices(vertices)

    A[[0, 1, 2, 10, 11], 0] = [1, 1, -2 / 3 * projection(p1, p2, p6), -2 / 3 * projection(p1, p3, p4), 1]
    A[[1, 2, 10, 11], 1] = [1 / 4 * (x2 - x1), 1 / 6 * (x1 - x2) * projection(p1, p2, p6),
                            1 / 6 * (x1 - x3) * projection(p1, p3, p4), 1 / 4 * (x3 - x1)]
    A[[1, 2, 10, 11], 2] = [1 / 4 * (y2 - y1), 1 / 6 * (y1 - y2) * projection(p1, p2, p6),
                            1 / 6 * (y1 - y3) * projection(p1, p3, p4), 1 / 4 * (y3 - y1)]
    A[2, 3] = d / (6 * np.linalg.norm(p1 - p2))
    A[[2, 3, 4, 5, 6], 4] = [-2 / 3 * projection(p2, p1, p5), 1, 1, 1, -2 / 3 * projection(p2, p3, p4)]
    A[[2, 3, 5, 6], 5] = [1 / 6 * (x2 - x1) * projection(p2, p1, p5), 1 / 4 * (x1 - x2), 1 / 4 * (x3 - x2),
                          1 / 6 * (x2 - x3) * projection(p2, p3, p4)]
    A[[2, 3, 5, 6], 6] = [1 / 6 * (y2 - y1) * projection(p2, p1, p5), 1 / 4 * (y1 - y2), 1 / 4 * (y3 - y2),
                          1 / 6 * (y2 - y3) * projection(p2, p3, p4)]
    A[6, 7] = d / (6 * np.linalg.norm(p2 - p3))
    A[[6, 7, 8, 9, 10], 8] = [-2 / 3 * projection(p3, p2, p6), 1, 1, 1, -2 / 3 * projection(p3, p1, p5)]
    A[[6, 7, 9, 10], 9] = [1 / 6 * (x3 - x2) * projection(p3, p2, p6), 1 / 4 * (x2 - x3), 1 / 4 * (x1 - x3),
                           1 / 6 * (x3 - x1) * projection(p3, p1, p5)]
    A[[6, 7, 9, 10], 10] = [1 / 6 * (y3 - y2) * projection(p3, p2, p6), 1 / 4 * (y2 - y3), 1 / 4 * (y1 - y3),
                            1 / 6 * (y3 - y1) * projection(p3, p1, p5)]
    A[10, 11] = d / (6 * np.linalg.norm(p3 - p1))

    return A
