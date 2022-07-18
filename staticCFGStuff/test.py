def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib_gen = fib()
for _ in range(10):
    next(fib_gen)
a = 1
if(a > 2):
    print("sth")
else:
    exit()

#constant propagation can be done with semgrp


def something():
    c=0
    d=0
    c+d