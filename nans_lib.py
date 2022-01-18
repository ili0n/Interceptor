def zero_false_position(f, a, b, errMax=10**-6, itMax=100):
    '''
    Finds the zero of a function using the FalsePosition method

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
        fA = f(a)
        fB = f(b)
        zero = b - fB*(b - a)/(fB - fA)

        fZero = f(zero)

        if abs(fZero) < errMax or abs(b - a) < errMax:
            return zero, it

        if fA*fZero < 0:
            b = zero
        else:
            a = zero

    return zero, it
