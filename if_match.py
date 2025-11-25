from timeit import timeit
import datetime
import decimal
from array import array

# Test value (most common type)
test_value = 42

# ---- Method A: optimized if/elif chain (most common first) ----
def detect_if(v):
    if isinstance(v, int):                          # Expected hit
        return "int"
    elif isinstance(v, str):
        return "str"
    elif isinstance(v, datetime.datetime):
        return "datetime"
    elif isinstance(v, float):
        return "float"
    elif isinstance(v, decimal.Decimal):
        return "decimal"
    elif isinstance(v, bytes):
        return "bytes"
    elif isinstance(v, bytearray):
        return "bytearray"
    elif isinstance(v, datetime.date):
        return "date"
    elif isinstance(v, datetime.timedelta):
        return "timedelta"
    elif isinstance(v, array):
        return "array"
    else:
        return "unknown"

# ---- Method A: optimized if/elif chain (most common first) ----
def detect_match_last(v):
    match v:
        case str():
            return "str"
        case datetime.datetime():
            return "datetime"
        case float():
            return "float"
        case decimal.Decimal():
            return "decimal"
        case bytes():
            return "bytes"
        case bytearray():
            return "bytearray"
        case datetime.date():
            return "date"
        case datetime.timedelta():
            return "timedelta"
        case array():
            return "array"
        case int():
            return "int"
        case _:
            return "unknown"



# ---- Method B: match/case dispatch ----
def detect_match(v):
    match v:
        case int():
            return "int"
        case str():
            return "str"
        case datetime.datetime():
            return "datetime"
        case float():
            return "float"
        case decimal.Decimal():
            return "decimal"
        case bytes():
            return "bytes"
        case bytearray():
            return "bytearray"
        case datetime.date():
            return "date"
        case datetime.timedelta():
            return "timedelta"
        case array():
            return "array"
        case _:
            return "unknown"


# ---- Method C: dispatch dict on type ----
dispatch_table = {
    int: "int",
    str: "str",
    datetime.datetime: "datetime",
    float: "float",
    decimal.Decimal: "decimal",
    bytes: "bytes",
    bytearray: "bytearray",
    datetime.date: "date",
    datetime.timedelta: "timedelta",
    array: "array",
}

def detect_table(v):
    return dispatch_table.get(type(v), "unknown")


# ---- RUN BENCHMARK ----
N = 2_000_000

t_if     = timeit("detect_if(test_value)", globals=globals(), number=N)
t_match_last = timeit("detect_match_last(test_value)", globals=globals(), number=N)
t_match  = timeit("detect_match(test_value)", globals=globals(), number=N)
t_table  = timeit("detect_table(test_value)", globals=globals(), number=N)

print(f"Iterations: {N:,}")
print(f"if / elif chain       → {t_if:.5f} sec")
print(f"match-case (1st)      → {t_match:.5f} sec")
print(f"match-case (last)     → {t_match_last:.5f} sec")
print(f"type() dispatch table → {t_table:.5f} sec")

