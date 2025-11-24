import time
import cProfile
import pstats
import os
import psutil
import time
import threading
import importlib
import argparse


# Global variable to store the maximum usage
MAX_MEMORY_MB = 0.0

def monitor_memory():
    """A function run in a separate thread to monitor memory usage."""
    global MAX_MEMORY_MB
    process = psutil.Process(os.getpid())

    # Monitor until the main thread signals it's done
    while threading.main_thread().is_alive():
        try:
            # Get the Resident Set Size (RSS) in bytes
            memory_bytes = process.memory_info().rss
            memory_mib = memory_bytes / (1024 * 1024)

            # Update the maximum usage
            if memory_mib > MAX_MEMORY_MB:
                MAX_MEMORY_MB = memory_mib

            time.sleep(0.1)  # Check every 100 milliseconds
        except psutil.NoSuchProcess:
            # Handle case where the process might have ended
            break
    print(f"\n--- Monitoring Thread Exited ---")

# --- Start Monitoring ---
memory_thread = threading.Thread(target=monitor_memory)
memory_thread.daemon = True # Allows the script to exit even if this thread is running
memory_thread.start()

# === CONFIG ===
HOST = "localhost"
USER = "georg"
PASSWORD = None
DATABASE = "test"

# Dramatically increase iterations and rows
SELECT_ITERATIONS = 200_000
INSERT_ROWS = 200_000
FETCH_CHUNK = 1000

def benchmark(conn):
    cursor = conn.cursor()

    print("=== Warm-up ===")
    cursor.execute("SELECT 1")
    cursor.fetchone()

    # --- Long-running SELECT benchmark ---
    print("=== Running long SELECT benchmark ===")
    select_times = []
    for i in range(SELECT_ITERATIONS):
        start = time.perf_counter()
        cursor.execute("SELECT 0xF as first, 0xFFFF as second, 0xFFFFFF as third, 0xFFFFFFFF as fourth")
        cursor.fetchone()
        end = time.perf_counter()
        select_times.append(end - start)
        if (i+1) % 50_000 == 0:
            print(f"Completed {i+1}/{SELECT_ITERATIONS} SELECTs")

    print(f"SELECT 1 avg time: {sum(select_times)/SELECT_ITERATIONS*1000:.3f} ms")

    # --- Long-running INSERT benchmark ---
    print("=== Running long INSERT benchmark ===")
    if dbmod.__name__ == "psycopg":
        cursor.execute("CREATE TEMPORARY TABLE IF NOT EXISTS bench (id SERIAL PRIMARY KEY, val INT)")
    else:
        cursor.execute("CREATE TEMPORARY TABLE IF NOT EXISTS bench (id INT PRIMARY KEY AUTO_INCREMENT, val INT)")
    insert_times = []
    for i in range(INSERT_ROWS):
        start = time.perf_counter()
        if dbmod.__name__ == "mariadb":
            cursor.execute("INSERT INTO bench (val) VALUES (?)", (i,))
        else:
            cursor.execute("INSERT INTO bench (val) VALUES (%s)", (i,))
        end = time.perf_counter()
        insert_times.append(end - start)
        if (i+1) % 50_000 == 0:
            print(f"Inserted {i+1}/{INSERT_ROWS} rows")
    conn.commit()
    print(f"INSERT {INSERT_ROWS} rows avg time: {sum(insert_times)/INSERT_ROWS*1000:.3f} ms")

    # --- Benchmark: fetchall ---
    print("=== Running fetchall benchmark ===")
    start = time.perf_counter()
    cursor.execute("SELECT *,1,2,3 FROM bench")
    rows= cursor.fetchall()
    end = time.perf_counter()
    print(f"Fetched {len(rows)} rows (fetchall) in {end-start:.3f} s")

    # --- Benchmark: fetchmany ---
    print("=== Running fetchmany benchmark ===")
    start = time.perf_counter()
    cursor.execute("SELECT *,1,2,3 FROM bench")
    total = 0
    while True:
        chunk = cursor.fetchmany(FETCH_CHUNK)
        if not chunk:
            break
        total += len(chunk)
    end = time.perf_counter()
    print(f"Fetched {total} rows (fetchmany {FETCH_CHUNK}) in {end-start:.3f} s")

    cursor.close()

def profile_module():
    print("=== Profiling long-running benchmark ===")
    if dbmod.__name__ == "psycopg":
        conn = dbmod.connect(
            user=USER,
            dbname=DATABASE,
            password=PASSWORD,
       )
    else:
        conn = dbmod.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
       )
    profiler = cProfile.Profile()
    profiler.enable()
    benchmark(conn)
    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats("cumulative")
    stats.print_stats(50)

    stats.sort_stats("calls").print_stats(20)

    conn.close()

    time.sleep(1.5) 

    print("\n" + "="*40)
    print(f"** Peak Memory Usage: {MAX_MEMORY_MB:.2f} MiB **")
    print("="*40)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dbmodule",
        nargs="?",
        choices=["mariadb", "psycopg", "pymysql"],
        default="mariadb",
        help="Database module to use (default=mariadb)"
    )
    args = parser.parse_args()

    dbmod = importlib.import_module(args.dbmodule)
    profile_module()


