import numpy as np


def rk4N(a, b, h, nfX0, dnfX):
    x = np.arange(a, b, h)
    n = len(x)
    order = len(nfX0)
    fnX = np.empty([order, n])
    fnX[:, 0] = nfX0.T
    k1, k2, k3, k4 = np.empty((1, order)), np.empty((1, order)), np.empty((1, order)), np.empty((1, order))
    for it in range(1, n):
        # k1
        for itOrder in range(order - 1):
            k1[0, itOrder] = fnX[itOrder + 1, it - 1]

        args = [x[it - 1]]

        for i in range(len(fnX)):
            args.append(fnX[i, it - 1])

        k1[0, order - 1] = dnfX(*args)

        # k2
        for itOrder in range(order - 1):
            k2[0, itOrder] = fnX[itOrder + 1, it - 1] + h / 2 * k1[0, itOrder + 1]

        args = [x[it - 1] + h / 2]

        for i in range(len(fnX)):
            for j in range(len(k1)):
                args.append(fnX[i, it - 1] + h / 2 * k1[j][0])

        k2[0, order - 1] = dnfX(*args)

        # k3
        for itOrder in range(order - 1):
            k3[0, itOrder] = fnX[itOrder + 1, it - 1] + h / 2 * k2[0, itOrder + 1]

        args = [x[it - 1] + h / 2]
        for i in range(len(fnX)):
            for j in range(len(k1)):
                args.append(fnX[i, it - 1] + h / 2 * k2[j][0])
        k3[0, order - 1] = dnfX(*args)

        # k4
        for itOrder in range(order - 1):
            k4[0, itOrder] = fnX[itOrder + 1, it - 1] + h * k3[0, itOrder + 1]

        args = [x[it - 1] + h]
        for i in range(len(fnX)):
            for j in range(len(k1)):
                args.append(fnX[i, it - 1] + h * k3[j][0])

        k4[0, order - 1] = dnfX(*args)

        for itOrder in range(order):
            fnX[itOrder, it] = fnX[itOrder, it - 1] + h / 6 * (
                        k1[0, itOrder] + 2 * k2[0, itOrder] + 2 * k3[0, itOrder] + k4[0, itOrder])

    fX = fnX[0, :]
    return fX, fnX.T


def zeroBisection(f, a, b, errMax=0.0001, itMax=100):
    '''
    Finds the zero of a function using the Bisection method

            Parameters:
                    f(function): Target function
                    a(np.array, 1d): Left boundry
                    b(np.array, 1d): Right boundry
                    errMax(float): Maximum allowed error
                    itMax(int): Maximum number of iterations

            Returns:
                    x(np.array, 1d): x where f(x)==0
                    it: number of performed iterations
    '''
    for it in range(itMax):
        zero = (a + b) / 2
        fZero = f(zero)

        if abs(fZero) < errMax or abs(b - a) < errMax:
            return zero, it + 1

        if f(a) * fZero < 0:
            b = zero
        else:
            a = zero

    return zero, it + 1


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
