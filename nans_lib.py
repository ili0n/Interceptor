import numpy as np


def lagrange_interpolation(x, fX):
    '''
    Finds the Lagrange polynomial for given points

            Parameters:
                    x(np.array, 1d): Points on x axis
                    fX(np.array, 1d): Points on y axis

            Returns:
                    p(np.array, 1d): Lagrange polynomial coefficients such that
                                     L = p[0]*x**(N-1) + p[1]*x**(N-2) + ... + p[N-2]*x + p[N-1]
    '''
    order = x.size

    p = 0

    for itFX in range(order):
        lNumer = 1
        lDenom = 1

        for itX in range(itFX):
            lNumer = np.convolve(lNumer, np.array([1, -x[itX]]))
            lDenom = lDenom * (x[itFX] - x[itX])

        for itX in range(itFX + 1, order):
            lNumer = np.convolve(lNumer, np.array([1, -x[itX]]))
            lDenom = lDenom * (x[itFX] - x[itX])

        p = p + lNumer / lDenom * fX[itFX]

    return p


def least_squares_regression(x, fX, order):
    '''
    Performs least-squares regression with polynomial of given order

            Parameters:
                    x(np.array, 1d): Points on x axis
                    fX(np.array, 1d): Points on y axis
                    order(int): Polynomial order

            Returns:
                    p(np.array, 1d): Polynomial coefficients of the least-squares solution such that
                                     R = p[0]*x**(N-1) + p[1]*x**(N-2) + ... + p[N-2]*x + p[N-1]
    '''
    n = x.size
    m = min(order + 1, n)
    A = np.zeros((n, m))

    for it in range(m):
        A[:, it] = x ** (it)

    a = np.linalg.solve(np.matmul(A.T, A), np.matmul(A.T, fX))

    p = a[::-1]
    return p
