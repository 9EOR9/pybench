import timeit
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--size", type=int, default=128, help="Size value")

args = parser.parse_args()

slice_size = args.size  # each small chunk

# Large sample buffer (16 MB)
data = bytearray(b"x" * 0xFFFFF * 0x40)
mv = memoryview(data)

num_slices = len(data) // slice_size  # number of slices we’ll take


def slice_bytearray():
    result = []
    for i in range(0, 10000):
        result.append(data[:slice_size])  # this is a view, no copy
    return result


def slice_memoryview():
    result = []
    for i in range(0, 10000):
        result.append(mv[:slice_size])  # this is a view, no copy
    return result


n = 100
t1 = timeit.timeit("slice_bytearray()", globals=globals(), number=n)
t2 = timeit.timeit("slice_memoryview()", globals=globals(), number=n)

print(f"slice_size: {slice_size}")
print(f"bytearray slicing: {t1:.4f} s")
print(f"memoryview slicing: {t2:.4f} s")
print(f"Speedup: {t1/t2:.2f}× faster (memoryview)")

