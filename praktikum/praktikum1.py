# Nama Lengkap: [Dionisio Silaen]
# NPM         : [237006011]
# Kelas       : [A]

import threading
import time
import random


def download_file(index, duration):
    """Fungsi untuk mensimulasikan unduhan file dengan sleep."""
    print(f"Mulai mengunduh file {index}...")
    time.sleep(duration)
    print(f"Selesai mengunduh file {index} dalam {duration:.2f} detik.")

def run_serial(jobs):
    """Menjalankan tugas secara serial."""
    for i, sec in jobs:
        download_file(i, sec)

def run_threads(jobs):
    """Menjalankan tugas menggunakan threads."""
    threads = []
    for i, sec in jobs:
        t = threading.Thread(target=download_file, args=(i, sec))
        threads.append(t)
        t.start() 

    for t in threads:
        t.join() 

if __name__ == "__main__":
    jumlah_file = 10
    jobs = [(i, random.uniform(0.5, 2)) for i in range(1, jumlah_file + 1)]
    print(f"Total {len(jobs)} file untuk diunduh.")

    print("\n--- Menjalankan Mode Serial ---")
    start_time_serial = time.time()
    run_serial(jobs)
    end_time_serial = time.time()
    waktu_serial = end_time_serial - start_time_serial
    print(f"Waktu eksekusi serial: {waktu_serial:.2f} detik.")

    print("\n--- Menjalankan Mode Threaded ---")
    start_time_threaded = time.time()
    run_threads(jobs)
    end_time_threaded = time.time()
    waktu_threaded = end_time_threaded - start_time_threaded
    print(f"Waktu eksekusi threaded: {waktu_threaded:.2f} detik.")

    speedup = waktu_serial / waktu_threaded
    print(f"\nSpeedup: {speedup:.2f}x")

    print("\n--- Tabel Hasil ---")
    print(f"| {'Mode':<10} | {'Jumlah File':<12} | {'Waktu (s)':<10} | {'Speedup':<10} |")
    print(f"| {'-'*10} | {'-'*12} | {'-'*10} | {'-'*10} |")
    print(f"| {'Serial':<10} | {jumlah_file:<12} | {waktu_serial:<10.2f} | {'1.00x':<10} |")
    print(f"| {'Threaded':<10} | {jumlah_file:<12} | {waktu_threaded:<10.2f} | {f'{speedup:.2f}x':<10} |")