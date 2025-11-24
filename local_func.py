import timeit

import math

class MyTest():

    def test_func(self):
        return 0

def test_func():
    return 0

def test_class():
    a= MyTest()
    for i in range(1_000_000_00):
        a.test_func()

def test_local():
    a= MyTest()
    for i in range(1_000_000_00):
        test_func() 

print(timeit.timeit(test_class, number=5))
print(timeit.timeit(test_local, number=5))

