class FibonacciLst:
    def __init__(self, lst):
        self.lst = lst
        self.fib_set = set()
        self.generate_fib_up_to(max(lst))
        self.iter_lst = iter([x for x in lst if x in self.fib_set])
    
    def generate_fib_up_to(self, limit):
        a, b = 0, 1
        self.fib_set.add(a)
        self.fib_set.add(b)
        while b <= limit:
            a, b = b, a + b
            self.fib_set.add(b)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return next(self.iter_lst)

lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
fib_lst = FibonacciLst(lst)
print([x for x in fib_lst])
