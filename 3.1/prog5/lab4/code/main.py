# import itertools

# def fibonacci():
#     a, b = 0, 1
#     while True:
#         yield a
#         a, b = b, a + b

# def my_gen(n):
#     fib_gen = fibonacci()
#     return list(itertools.islice(fib_gen, n))
    
# print(my_gen(10))
""""""

# def fibonacci_gen():
#     a, b = 0, 1
#     while True:
#         yield a
#         a, b = b, a + b

# def my_gen(n):
#     while True:
#         yield from (next(fibonacci_gen()) for _ in range(n))

# gen = my_gen(10)
# print(next(gen))

""""""

import functools

def fibonacci_gen():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def coroutine(g):
    @functools.wraps(g)
    def wrapper(*args, **kwargs):
        gen = g(*args, **kwargs)
        next(gen) 
        return gen
    return wrapper

@coroutine
def my_gen():
    gen = fibonacci_gen()
    n = yield  
    while True:
        yield [next(gen) for _ in range(n)]
        n = yield  

gen = my_gen()
print(gen.send(10))



