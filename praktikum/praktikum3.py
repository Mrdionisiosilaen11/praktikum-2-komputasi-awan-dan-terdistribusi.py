# Nama Lengkap: [Dionisio Silaen]
# NPM         : [237006011]
# Kelas       : [A]

import time
import random
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def download_file(duration):
    time.sleep(duration)

def heavy(n, iters=10**6):
    s = 0
    for i in range(iters):
        s += (i * n) % 7
    return s

def run_serial(func, data):
    for d in data:
        func(d)

def run_threads(func, data, max_workers):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(func, data)

def run_processes(func, data, max_workers):
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        executor.map(func, data)

if __name__ == "__main__":
    NUM_JOBS = 10
    NUM_WORKERS = 4 

    io_data = [random.uniform(0.1, 0.5) for _ in range(NUM_JOBS)]
    cpu_data = range(1, NUM_JOBS + 1)

    results = {}

    start = time.time()
    run_serial(download_file, io_data)
    results['io_serial'] = time.time() - start

    start = time.time()
    run_threads(download_file, io_data, NUM_WORKERS)
    results['io_threads'] = time.time() - start

    start = time.time()
    run_processes(download_file, io_data, NUM_WORKERS)
    results['io_processes'] = time.time() - start

    start = time.time()
    run_serial(heavy, cpu_data)
    results['cpu_serial'] = time.time() - start

    start = time.time()
    run_threads(heavy, cpu_data, NUM_WORKERS)
    results['cpu_threads'] = time.time() - start

    start = time.time()
    run_processes(heavy, cpu_data, NUM_WORKERS)
    results['cpu_processes'] = time.time() - start

    sp_threads_io = results['io_serial'] / results['io_threads']
    sp_processes_io = results['io_serial'] / results['io_processes']
    sp_threads_cpu = results['cpu_serial'] / results['cpu_threads']
    sp_processes_cpu = results['cpu_serial'] / results['cpu_processes']

    print("\n--- Tabel Hasil Perbandingan ---")
    print(f"| {'Jenis Aplikasi':<15} | {'Serial (s)':<12} | {'Threads (s)':<12} | {'Processes (s)':<14} | {'Speedup Threads':<18} | {'Speedup Processes':<18} |")
    print(f"| {'-'*15} | {'-'*12} | {'-'*12} | {'-'*14} | {'-'*18} | {'-'*18} |")
    print(f"| {'I/O-Bound':<15} | {results['io_serial']:<12.4f} | {results['io_threads']:<12.4f} | {results['io_processes']:<14.4f} | {f'{sp_threads_io:.2f}x':<18} | {f'{sp_processes_io:.2f}x':<18} |")
    print(f"| {'CPU-Bound':<15} | {results['cpu_serial']:<12.4f} | {results['cpu_threads']:<12.4f} | {results['cpu_processes']:<14.4f} | {f'{sp_threads_cpu:.2f}x':<18} | {f'{sp_processes_cpu:.2f}x':<18} |")