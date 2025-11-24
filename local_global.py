from timeit import timeit

class test():

    glen= b'123'

    def fglobal(self):
        """
        Access global variable glen
        """
        for i in range(250):
            x= self.glen

    def flocal(self):
        """
        Store global variable in local variable
        """
        y= self.glen
        for i in range(250):
            x= y

    def fparam(self, y):
        """
        Pass variable
        """
        for i in range(250):
            x= y


setup = """from __main__ import test
x= test()"""

t1= timeit("x.fglobal()", setup=setup)
t2= timeit("x.flocal()", setup=setup)
t3= timeit("x.fparam(b'123')", setup=setup)

print(f"Global: {t1}")
print(f"Local:  {t2}")
print(f"Param:  {t3}")

