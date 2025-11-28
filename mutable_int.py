import timeit
import struct
from ctypes import c_size_t

# -------------------------
# Setup: small memoryview packet
packet = memoryview(b"\x01\x02" * 10)
PACKET_LIMIT = len(packet) - 2  # prevent out-of-bounds

# -------------------------
# Method 1: tuple return (value, new_pos)
def read_uint16_return(packet, pos):
    value = struct.unpack_from('<H', packet, pos)[0]
    return value, pos + 2

# -------------------------
# Method 2: mutable list cursor
def read_uint16_list(packet, cursor):
    pos = cursor[0]
    value = struct.unpack_from('<H', packet, pos)[0]
    pos += 2
    if pos > PACKET_LIMIT:
        pos = 0
    cursor[0] = pos
    return value

# -------------------------
# Method 3: ctypes cursor
def read_uint16_ctypes(packet, cursor: c_size_t):
    pos = cursor.value
    value = struct.unpack_from('<H', packet, pos)[0]
    pos += 2
    if pos > PACKET_LIMIT:
        pos = 0
    cursor.value = pos
    return value

# -------------------------
# Method 4: parser-style function (emulates PayloadParser)
def parser_read_uint16(state):
    pos = state['pos']
    value = struct.unpack_from('<H', state['packet'], pos)[0]
    pos += 2
    if pos > PACKET_LIMIT:
        pos = 0
    state['pos'] = pos
    return value

# -------------------------
# Benchmark
def benchmark():
    iterations = 10_000_000  # 10 million

    # Tuple-return
    t1 = timeit.timeit(
        stmt="""
v, pos = read_uint16_return(packet, pos)
if pos > PACKET_LIMIT: pos = 0
        """,
        setup="from __main__ import read_uint16_return, packet, PACKET_LIMIT; pos=0",
        number=iterations,
    )

    # Mutable list cursor
    t2 = timeit.timeit(
        stmt="v = read_uint16_list(packet, cursor)",
        setup="from __main__ import read_uint16_list, packet, PACKET_LIMIT; cursor=[0]",
        number=iterations,
    )

    # ctypes cursor
    t3 = timeit.timeit(
        stmt="v = read_uint16_ctypes(packet, cursor)",
        setup="from __main__ import read_uint16_ctypes, packet, PACKET_LIMIT, c_size_t; cursor=c_size_t(0)",
        number=iterations,
    )

    # Parser-style state dict
    t4 = timeit.timeit(
        stmt="v = parser_read_uint16(state)",
        setup="from __main__ import parser_read_uint16, packet, PACKET_LIMIT; state={'packet': packet, 'pos':0}",
        number=iterations,
    )

    print(f"Iterations: {iterations:,}")
    print(f"return (value, pos):           {t1:.4f}s")
    print(f"return value, pos=mutable int: {t2:.4f}s")
    print(f"return value, pos=ctypes:      {t3:.4f}s")
    print(f"existing (PayloadParser):      {t4:.4f}s")


if __name__ == "__main__":
    benchmark()

