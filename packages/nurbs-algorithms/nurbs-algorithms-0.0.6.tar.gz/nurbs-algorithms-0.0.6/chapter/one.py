from numpy import zeros, asarray


def Horner1(a, n, u0):
    '''Horner algorithm for computing a power basis curve'''
    #
    # Get degree
    degree = n
    #
    # Initialize curve evaluation
    C = a[degree]
    #
    # Iterate over lower exponents
    for i in range(degree - 1, -1, -1):
        C = C * u0 + a[i]
    #
    return C


def Bernstein(i, n, u):
    '''Calculate the Bernstein polynomial, B_i,n(u), at u'''
    #
    # Initialize temp array
    temp = zeros((1, n + 1))
    temp[n - i] = 1.0
    #
    # Compute 1 less u
    u0 = 1 - u
    #
    # Compute the columns of Table 1.1, p. 20
    # Outer loop iterates over all degrees < n
    # families of Bernstein polynomials
    for k in range(1, n + 1):
        #
        # Inner loop computes current value of
        # Bernstein polynomial family based on
        # previous family's evaluation.
        for j in range(n, k - 1, -1):
            temp[j] = u0 * temp[j] + u * temp[j - 1]
        #
    #
    # Last entry is value of polynomial at u
    B = temp[n]
    #
    return B


def AllBernstein(n, u):
    #
    B_list = zeros((1, n + 1))
    B_list[0] = 1.0
    u0 = 1.0 - u
    for j in range(1, n + 1):
        saved = 0
        for k in range(0, j):
            temp = B_list[k]
            B_list[k] = saved + u0 * temp
            saved = u * temp
        #
        B_list[j] = saved
        #
    #
    return B_list


def PointOnBezierCurve(P, n, u):
    #
    B_list = AllBernstein(n, u)
    C = asarray([0.0, 0.0])
    for k in range(0, n + 1):
        C += (B_list[k] * P[k])
    #
    return C


def deCasteljau1(P, n, u):
    #
    Q = tuple(point.copy() for point in P)
    u0 = 1.0 - u
    #
    for k in range(1, n + 1):
        for i in range(0, n - k + 1):
            Q[i] = u0 * Q[i] + u * Q[i + 1]
        #
    #
    C = Q[0]
    #
    return C


def Horner2(a, n, m, u0, v0):
    #
    C1 = tuple(Horner1(a[i], m, u0) for i in range(0, n + 1))
    S = Horner1(C1, n, v0)
    #
    return S


def deCasteljau2(P, n, m, u0, v0):
    #
    # Although it's more efficient to compute this
    # on the smaller of n or m, the data structure I'm using
    # is overly simple and doesn't naturally support 2D indexing
    Q = tuple(deCasteljau1(P[j], n, u0) for j in range(0, m + 1))
    S = deCasteljau1(Q, m, v0)
    #
    return S
