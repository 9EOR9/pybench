import timeit

ITERATIONS=100000
COLUMNS=1000

def prealloc_list():
    result = [None] * COLUMNS
    for i in range(COLUMNS):
        result[i]= "this is the value for"


def append_list():
    result = []
    for i in range(COLUMNS):
        result.append("This is the value for")


n = 100
t1 = timeit.timeit("prealloc_list()", globals=globals(), number=ITERATIONS)
t2 = timeit.timeit("append_list()", globals=globals(), number=ITERATIONS)

print(f"prealloc: {t1:.4f} s")
print(f"append: {t2:.4f} s")

