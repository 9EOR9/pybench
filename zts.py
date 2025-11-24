import timeit

# --- Test Packets ---
packet_short = bytearray(b'Hello\x00World')
packet_medium = bytearray(b'A' * 1000 + b'\x00')
packet_long = bytearray(b'A' * 50000 + b'\x00')

pos = 0

# --- Original Implementation ---
def read_null_terminated_original(packet, pos, encoding='utf-8'):
    for i in range(pos, len(packet)):
        if packet[i] == 0x00:
            string_data = bytes(packet[pos:i]).decode(encoding)
            return string_data, i + 1
    string_data = bytes(packet[pos:]).decode(encoding)
    return string_data, len(packet)

# --- Optimized Implementation ---
def read_null_terminated_optimized(packet, pos, encoding='utf-8'):
    null_pos = packet.find(0x00, pos)
    if null_pos == -1:
        string_data = packet[pos:].decode(encoding)
        return string_data, len(packet)
    string_data = packet[pos:null_pos].decode(encoding)
    return string_data, null_pos + 1


# --- Benchmark Runner ---
def run_benchmark():
    iterations = 10_000

    results = {
        "short_original": timeit.timeit(
            lambda: read_null_terminated_original(packet_short, pos),
            number=iterations),
        "short_optimized": timeit.timeit(
            lambda: read_null_terminated_optimized(packet_short, pos),
            number=iterations),

        "medium_original": timeit.timeit(
            lambda: read_null_terminated_original(packet_medium, pos),
            number=iterations),
        "medium_optimized": timeit.timeit(
            lambda: read_null_terminated_optimized(packet_medium, pos),
            number=iterations),

        "long_original": timeit.timeit(
            lambda: read_null_terminated_original(packet_long, pos),
            number=iterations),
        "long_optimized": timeit.timeit(
            lambda: read_null_terminated_optimized(packet_long, pos),
            number=iterations),
    }

    print("\n=== Parse zero terminated string benchmark results (10,000 runs) ===")
    for key, value in results.items():
        print(f"{key:20} : {value:.6f} s")


if __name__ == "__main__":
    run_benchmark()

