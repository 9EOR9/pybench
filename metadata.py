import timeit

# Simulated metadata bytes from MariaDB
data = (
    b"def\x00myschema\x00t_alias\x00table\x00c_alias\x00column\x00"
) * 30  # repeat to simulate many columns

def decode_once():
    decoded = data.decode("utf-8", "replace")
    parts = decoded.split("\x00")
    if parts and parts[-1] == "":
        parts.pop()
    for i in range(0, len(parts), 6):
        catalog, schema, t_alias, table, c_alias, column = parts[i:i+6]

def decode_each():
    parts = data.split(b"\x00")
    if parts and parts[-1] == b"":
        parts.pop()
    for i in range(0, len(parts), 6):
        catalog, schema, t_alias, table, c_alias, column = (
            p.decode("utf-8", "replace") for p in parts[i:i+6]
        )

# Run both benchmarks
n = 100000
t1 = timeit.timeit("decode_once()", globals=globals(), number=n)
t2 = timeit.timeit("decode_each()", globals=globals(), number=n)

print(f"decode_once: {t1:.4f} s")
print(f"decode_each: {t2:.4f} s")
print(f"Speedup: {t2/t1:.2f}x faster (single decode)")
