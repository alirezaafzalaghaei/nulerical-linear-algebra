from __future__ import division

import copy
import time

import numpy as np


def timeit(method):
    def timed(*args, **kw):
        ts = time.perf_counter()
        result = method(*args, **kw)
        te = time.perf_counter()
        print('%-20r %7.5f sec' % (method.__name__, te - ts))
        return result

    return timed


@timeit
def lu_solvable(A):
    return all(np.linalg.det(np.array(A)[0:k, 0:k]) != 0 for k in range(1, len(A) + 1))


@timeit
def upper_tri_solver(a, b):
    n = len(b)
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(a[i][j] * x[j] for j in range(n))) / a[i][i]
    return x


@timeit
def lower_tri_solver(a, b):
    n = len(b)
    x = [0] * n
    for i in range(n):
        x[i] = (b[i] - sum(a[i][j] * x[j] for j in range(n))) / a[i][i]
    return x


@timeit
def LU_partial_pivoting(A):
    n = len(A)
    # P = [[1 if j == i else 0 for j in range(n)] for i in range(n)]
    # L = [[1 if j == i else 0 for j in range(n)] for i in range(n)]
    P = np.eye(n).tolist()
    L = np.eye(n).tolist()

    for k in range(n - 1):
        r = np.abs(A[k][k:]).T.argmax() + k
        A[k], A[r] = A[r], A[k]
        L[k][:k], L[r][:k] = L[r][:k], L[k][:k]
        P[r], P[k] = P[k], P[r]

        for i in range(k + 1, n):
            L[i][k] = A[i][k] / A[k][k]
            for j in range(k, n):
                A[i][j] -= L[i][k] * A[k][j]

    return L, A, P


# A = input("Enter Matrix A(n,n): ")
# B = input("Enter matrix B(1,n): ")

n = 3
A = np.random.uniform(-100, 100, (n, n))
B = np.random.uniform(-10, 10, n)

# A = [[1, -1, 3], [-1, 1, 2], [1, 0, 1]]
# B = [2, 3, 4]


# check if LU Decomposition method can solve the equation
# A = [[1, 3, -1], [7, 1, 0], [2, 5, 1]]
# A = [[2, 1, 1, 0], [4, 3, 3, 1], [8, 7, 9, 5], [6, 7, 9, 8]]
# B = [1, 2, 3, 4]
A = [[10, 7, 0], [-3, 2, 6], [5, -1, 5]]
B = [1, 2, 3]
if not lu_solvable(A):
    raise ValueError("Determinant must be greater than zero!")

# find exact solution of AX = B
real = np.dot(np.linalg.inv(A), B)

# find L and U
L, U, P = LU_partial_pivoting(copy.deepcopy(A))

B = np.dot(P, B)

# round L and U elements to 5 digits
L, U = np.around([L, U], 5)

# solve LY = B equation
Y = lower_tri_solver(L, B)

# solve UX = Y equation
X = upper_tri_solver(U, Y)

# round results to 5 digits
real, X = np.around([real, X], 5)

assert np.allclose(X, real, rtol=0, atol=1e-1)

print(
    """
    LU Decomposition: {0}

    Matrix Solution : {1}
    """.format(X, real))
