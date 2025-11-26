import struct
import time

# ----- Config -----
ITERATIONS = 2_000_000
DATA = (bytes(range(256)) * 1024)  # 262,144 bytes
BUF_LEN = len(DATA)
SIZE = 3
# ------------------

# --- Readers ---
def unpack_from_3(offset):
    # Direct read from buffer
    return struct.unpack_from('<I', DATA, offset)[0] & 0xFFFFFF

def unpack_3(offset):
    # Slice + unpack
    return struct.unpack('<I', DATA[offset:offset+3] + b'\x00')[0] & 0xFFFFFF

def math_3(offset):
    # Manual unrolled math
    return DATA[offset] | (DATA[offset+1]<<8) | (DATA[offset+2]<<16)

def frombytes_3(offset):
    return int.from_bytes(DATA[offset:offset+3], 'little')

# --- Benchmark runner ---
def bench(reader):
    offset = 0
    max_off = BUF_LEN - SIZE
    total = 0
    start = time.perf_counter()
    for _ in range(ITERATIONS):
        if offset > max_off:
            offset = 0
        total += reader(offset)
        offset += SIZE
    return time.perf_counter() - start, total

# --- Run benchmark ---
def main():
    print(f"Buffer: {BUF_LEN:,} bytes | Iterations: {ITERATIONS:,}\n")

    t_unpack_from, _ = bench(unpack_from_3)
    t_unpack, _      = bench(unpack_3)
    t_math, _        = bench(math_3)
    t_from, _        = bench(frombytes_3)

    print("3-byte LE integer benchmark:\n")
    print(f"  struct.unpack_from : {t_unpack_from:.6f}s  ({ITERATIONS / t_unpack_from:,.0f} ops/sec)")
    print(f"  struct.unpack      : {t_unpack:.6f}s  ({ITERATIONS / t_unpack:,.0f} ops/sec)")
    print(f"  manual math        : {t_math:.6f}s  ({ITERATIONS / t_math:,.0f} ops/sec)")
    print(f"  int.from_bytes     : {t_from:.6f}s  ({ITERATIONS / t_from:,.0f} ops/sec)")

if __name__ == "__main__":
    main()

