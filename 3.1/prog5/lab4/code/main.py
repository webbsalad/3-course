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



