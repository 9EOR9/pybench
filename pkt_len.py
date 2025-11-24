import struct
import secrets
import timeit

a = secrets.token_bytes(4)


ITERATIONS=1000000

def struct_pktlen():
    packet_length = struct.unpack_from('<I', a[:3] + b'\x00')[0]

def native_pktlen():
    packet_length = a[0] + (a[1] << 8) + (a[2] << 16)


# warm up
timeit.timeit(struct_pktlen, number=ITERATIONS)
timeit.timeit(native_pktlen, number=ITERATIONS)

t1 = timeit.timeit(struct_pktlen, number=ITERATIONS)
t2 = timeit.timeit(native_pktlen, number=ITERATIONS)

print(f"struct_pktlen: {t1:.6f}")
print(f"native_pktlen: {t2:.6f}")

speedup = t1 / t2
percent = (t1 - t2) / t1 * 100

print(f"Speedup: {speedup:.1f}x faster ({percent:+.1f}%)")
