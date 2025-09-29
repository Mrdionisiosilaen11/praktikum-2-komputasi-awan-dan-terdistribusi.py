# Nama Lengkap: [Dionisio Silaen]
# NPM         : [237006011]
# Kelas       : [A]

import time
from concurrent.futures import ProcessPoolExecutor


def heavy(n, iters=10**6):
    """Fungsi yang melakukan komputasi berat."""
    s = 0
    for i in range(iters):
        s += (i * n) % 7
    return s

def run_serial(data_range):
    """Menjalankan komputasi secara serial."""
    results = []
    for item in data_range:
        results.append(heavy(item))
    return results

def run_parallel(data_range, max_workers):
    """Menjalankan komputasi secara paralel menggunakan proses."""
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(heavy, data_range))
    return results

if __name__ == "__main__":
    data = range(1, 21)

    print("--- Menjalankan Mode Serial ---")
    start_time_serial = time.time()
    run_serial(data)
    end_time_serial = time.time()
    waktu_serial = end_time_serial - start_time_serial
    print(f"Waktu eksekusi serial: {waktu_serial:.4f} detik.")

    print("\n--- Tabel Hasil ---")
    print(f"| {'Proses':<8} | {'Waktu (s)':<10} | {'Speedup':<10} | {'Efisiensi':<10} |")
    print(f"| {'-'*8} | {'-'*10} | {'-'*10} | {'-'*10} |")
    print(f"| {'1 (Serial)':<8} | {waktu_serial:<10.4f} | {'1.00x':<10} | {'100.00%':<10} |")

    for num_processes in [2, 4, 8]:
        print(f"\n--- Menjalankan Mode Paralel ({num_processes} proses) ---")
        start_time_parallel = time.time()
        run_parallel(data, num_processes)
        end_time_parallel = time.time()
        waktu_paralel = end_time_parallel - start_time_parallel
        print(f"Waktu eksekusi paralel: {waktu_paralel:.4f} detik.")

        speedup = waktu_serial / waktu_paralel
        efisiensi = (speedup / num_processes) * 100

        print(f"| {num_processes:<8} | {waktu_paralel:<10.4f} | {f'{speedup:.2f}x':<10} | {f'{efisiensi:.2f}%':<10} |")