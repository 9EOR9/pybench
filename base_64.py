import base64
import timeit
import os

def escape_base64(value: bytes | bytearray) -> str:
    b64 = base64.b64encode(value).decode('ascii')
    return "FROM_BASE64('" + b64 + "')"

def escape_hex(value: bytes | bytearray) -> str:
    hex= value.hex()
    return "X'" + hex + "'"

def run_benchmark():
    sizes = [1, 16, 64, 256, 1024, 4096, 8192, 16384, 32768, 65536, 131072]

    header = f"{'Size (bytes)':>12} | {'Method':>8} | {'Time (s)':>10} | {'Output size':>12} | Ratio"
    print(header)
    print("-" * len(header))

    for size in sizes:
        data = os.urandom(size)

        # Base64
        b64_sample = escape_base64(data)
        b64_size = len(b64_sample.encode("ascii"))
        b64_time = timeit.timeit(lambda: escape_base64(data), number=20000)

        # HEX
        hex_sample = escape_hex(data)
        hex_size = len(hex_sample.encode("ascii"))
        hex_time = timeit.timeit(lambda: escape_hex(data), number=20000)

        print(f"{size:>12} | {'Base64':>8} | {b64_time:>10.4f} | {b64_size:>12} | x{b64_size/size:0.2f}")
        print(f"{size:>12} | {'HEX':>8} | {hex_time:>10.4f} | {hex_size:>12} | x{hex_size/size:0.2f}")
        print("-" * len(header))

if __name__ == "__main__":
    run_benchmark()

