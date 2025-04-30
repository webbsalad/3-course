import cython
from libc.math cimport sqrt, floor

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef bint is_perfect_square(long long n):
    """Проверяет, является ли число полным квадратом."""
    cdef long long root = <long long>floor(sqrt(n))
    return root * root == n

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef tuple fermat_factorization(long long N):
    """Разложение числа N на множители методом Ферма."""
    if N % 2 == 0:
        return 2, N // 2  # Если N четное, делим на 2
    
    cdef long long x = <long long>floor(sqrt(N)) + 1  # Начинаем с ближайшего целого числа к √N
    cdef long long y_squared
    cdef long long y
    
    while True:
        y_squared = x * x - N
        if is_perfect_square(y_squared):
            y = <long long>floor(sqrt(y_squared))
            return (x - y, x + y)  # Возвращаем найденные множители
        x += 1  # Увеличиваем x 