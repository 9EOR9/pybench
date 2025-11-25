import struct
import timeit

class PacketBuffer:
    def __init__(self, data):
        self._data = data

    def __getitem__(self, key):
        return self._data[key]

packet_data = b'abcdefgh'  # 8-byte "packet"
packet = PacketBuffer(packet_data)
mv = memoryview(packet._data)
N = 1_000_000_0

# Slice + unpack
t_slice = timeit.timeit(
    'struct.unpack("<d", packet[:8])[0]',
    globals=globals(),
    number=N
)

# Direct _data + unpack_from
t_direct = timeit.timeit(
    'struct.unpack("<d", packet._data[0:])[0]',
    globals=globals(),
    number=N
)
# Direct _data + unpack_from
t_direct2 = timeit.timeit(
    'struct.unpack_from("<d", packet._data,0)[0]',
    globals=globals(),
    number=N
)

# Memoryview + unpack_from
t_mv = timeit.timeit(
    'struct.unpack("<d", mv[0:])[0]',
    globals=globals(),
    number=N
)

# Memoryview + unpack_from
t_mv2 = timeit.timeit(
    'struct.unpack_from("<d", mv,0)[0]',
    globals=globals(),
    number=N
)

print(f"__get_item__ + unpack: {t_slice:.6f} s")
print(f"packet._data + unpack: {t_direct:.6f} s")
print(f"view + unpack: {t_mv:.6f} s")
print(f"packet._data + unpack_from: {t_direct2:.6f} s")
print(f"view + unpack_from: {t_mv:.6f} s")

