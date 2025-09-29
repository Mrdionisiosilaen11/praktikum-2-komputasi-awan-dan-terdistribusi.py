# Nama Lengkap: [Dionisio Silaen]
# NPM         : [237006011]
# Kelas       : [A]

import threading
import time
import queue
import os
from concurrent.futures import ProcessPoolExecutor


def loader(file_paths, task_queue):
    """Stage-1: Membaca path file dan memasukkannya ke queue (I/O)."""
    print("Loader: Memulai...")
    for path in file_paths:
        task_queue.put(path)
    print("Loader: Semua path file telah dimasukkan ke queue.")
    task_queue.put(None)

def worker_cpu_task(file_path):
    """Stage-2: Membaca file dan melakukan komputasi (CPU-Bound)."""
    if file_path is None:
        return None, 0
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            word_count = len(content.split())
            [i*i for i in range(500)]
            return os.path.basename(file_path), word_count
    except Exception as e:
        return os.path.basename(file_path), f"Error: {e}"

if __name__ == "__main__":
    if not os.path.exists("dataset"):
        os.makedirs("dataset")
    for i in range(20):
        with open(f"dataset/file_{i}.txt", "w") as f:
            f.write("Ini adalah contoh teks untuk praktikum. " * (i + 1) * 10)

    file_paths = [os.path.join("dataset", f) for f in os.listdir("dataset")]
    num_files = len(file_paths)
    num_workers_cpu = 4 

    task_queue = queue.Queue()

    print("--- Memulai Pipeline Hybrid ---")
    start_time = time.time()

    loader_thread = threading.Thread(target=loader, args=(file_paths, task_queue))
    loader_thread.start()

    total_word_count = 0
    files_processed = 0

    with ProcessPoolExecutor(max_workers=num_workers_cpu) as executor:
        futures = []
        while True:
            path = task_queue.get()
            if path is None: 
                break
            futures.append(executor.submit(worker_cpu_task, path))

        for future in futures:
            path, result = future.result()
            if isinstance(result, int):
                total_word_count += result
                files_processed += 1
                print(f"Aggregator: Hasil dari {path} -> {result} kata.")

    loader_thread.join() 
    end_time = time.time()

    total_time = end_time - start_time
    throughput = files_processed / total_time
    avg_latency = total_time / files_processed if files_processed > 0 else 0

    print("\n--- Hasil Pipeline ---")
    print(f"Total file diproses : {files_processed}")
    print(f"Total kata dihitung : {total_word_count}")
    print(f"Waktu total         : {total_time:.4f} s")
    print(f"Throughput          : {throughput:.2f} file/s")
    print(f"Avg Latency         : {avg_latency:.4f} s/file")