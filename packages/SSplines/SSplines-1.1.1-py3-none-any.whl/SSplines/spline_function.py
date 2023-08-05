import numpy as np

from SSplines.helper_functions import coefficients_linear, \
    coefficients_quadratic, evaluate_non_zero_basis_splines, determine_sub_triangle, evaluate_non_zero_basis_derivatives


class SplineFunction(object):
    """
    Represents a single callable spline function of degree 0/1/2 over the PS12-split of given triangle.
    """

    def __init__(self, vertices, degree, coefficients):
        self.vertices = np.array(vertices)
        self.degree = int(degree)
        self.coefficients = np.array(coefficients)

    def __add__(self, other):
        """
        Addition of two SplineFunctions.
        :param SplineFunction other:
        :return: SplineFunction
        """
        return SplineFunction(self.vertices, self.degree, self.coefficients + other.coefficients)

    def __radd__(self, other):
        """
        Right addition of two SplineFunctions. Used for 'summing' over a list of SplineFunctions.
        :param SplineFunction other:
        :return: SplineFunction
        """
        if other == 0:  # 'sum' starts with 0 and radds elements one by one.
            return self
        else:
            return self.__add__(other)

    def __mul__(self, scalar):
        """
        Scalar multiplication of SplineFunction.
        :param float scalar:
        :return: SplineFunction
        """
        return SplineFunction(self.vertices, self.degree, scalar * self.coefficients)

    def __rmul__(self, scalar):
        """
        Right scalar multiplication of SplineFunction
        :param float scalar:
        :return: SplineFunction
        """
        return self.__mul__(scalar)

    def _non_zero_coefficients(self, k):
        """
        Returns the indices of the non-zero coefficients at sub-triangle k.
        :param int k: sub-triangle number
        :return np.ndarray: indices
        """
        if self.degree == 0:
            return self.coefficients[k]
        elif self.degree == 1:
            return self.coefficients[coefficients_linear(k)]
        elif self.degree == 2:
            return self.coefficients[coefficients_quadratic(k)]

    def _D_once(self, x, k, u, r):
        """
        Evaluates the r'th directional derivative of the function at the point x.
        :param np.ndarray x: point of evaluation
        :param int k: sub-triangle of x
        :param np.ndarray u: direction vector
        :param int r: order of derivative
        :return: r'th directional derivative of f in direction u
        """

        if k == -1:
            return 0

        z = evaluate_non_zero_basis_derivatives(triangle=self.vertices, d=self.degree, r=r, x=x, u=u)
        c = self._non_zero_coefficients(k)

        return z.dot(c)

    def D(self, x, u, r):
        """
        Evaluates the r'th directional derivative of the function at the point x.
        :param np.ndarray x: point of evaluation
        :param np.ndarray u: direction vector
        :param int r: order of derivative
        :return: r'th directional derivative of f in direction u
        """

        if len(x.shape) == 2:
            m, _ = x.shape
        else:
            m = 1

        if m == 1:
            k = determine_sub_triangle(self.vertices, x)
            return self._D_once(x=x, k=k, r=r, u=u)
        else:
            z = np.zeros(m)
            for i, p in enumerate(x):
                k = determine_sub_triangle(self.vertices, p)
                z[i] = self._D_once(x=p, k=k, r=r, u=u)
            return z

    def _evaluate_once(self, x, k):
        """
        Evaluates the spline function or its r'th directional derivative.
        :param np.ndarray x: point of evaluation
        :param int k: sub-triangle x lies in
        :return:
        """

        if k == -1:
            return 0

        z = evaluate_non_zero_basis_splines(triangle=self.vertices, d=self.degree, x=x)
        c = self._non_zero_coefficients(k)

        return z.dot(c)

    def __call__(self, x):
        """
        Evaluates the spline function at the point x.
        :param np.ndarray x: point of evaluation
        :return: f(x)
        """
        if len(x.shape) == 2:
            m, _ = x.shape
        else:
            m = 1

        if m == 1:
            k = determine_sub_triangle(self.vertices, x)
            return self._evaluate_once(x=x, k=k)
        else:
            z = np.zeros(m)
            for i, p in enumerate(x):
                k = determine_sub_triangle(self.vertices, p)
                z[i] = self._evaluate_once(p, k)
            return z

    def dx(self, x):
        """
        Shorthand for derivative in x-direction.
        :param np.ndarray x: point of evaluation
        :return: df/dx
        """

        return self.D(x, np.array([1, 0]), 1)

    def dy(self, x):
        """
        Shorthand for derivative in y-direction.
        :param np.ndarray x: point of evaluation
        :return: df/dy
        """
        return self.D(x, np.array([0, 1]), 1)

    def div(self, x):
        """
        Computes the divergence of the spline function at the point(s) x.
        :param np.ndarray x:
        :return: divergence evaluated at x
        """

        return self.dx(x) + self.dy(x)

    def grad(self, x):
        """
        Computes the gradient of the spline function at the point(s) x.
        :param np.ndarray x: points of evaluation
        :return: gradient evaluated at x
        """

        return np.array([self.dx(x), self.dy(x)]).T

    def lapl(self, x):
        """
        Computes the laplacian of the spline function at the point(s) x.
        :param np.ndarray x: points of evaluation
        :return: laplacian evaluated at x
        """

        r = 2
        ux = np.array([1, 0])
        uy = np.array([0, 1])

        return self.D(x, ux, r) + self.D(x, uy, r)
