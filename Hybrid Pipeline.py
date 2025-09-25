# Nama: Matin Rusydan
# NPM: 237006030

import threading
import queue
import time
import os
from concurrent.futures import ProcessPoolExecutor

# --- FUNGSI-FUNGSI PIPELINE ---

# Stage 1: Loader (I/O-bound)
# Thread ini bertugas membaca path file dan memasukkannya ke queue.
def loader(file_paths, q):
    print("Loader: Memulai...")
    for file_path in file_paths:
        # Mensimulasikan I/O saat membaca direktori
        time.sleep(0.05)
        q.put(file_path)
    # Menandakan tidak ada lagi file yang akan dimasukkan
    q.put(None)
    print("Loader: Selesai.")

# Stage 2: Worker (CPU-bound)
# Fungsi ini dijalankan oleh process pool untuk mengolah data.
def process_file(file_path):
    # Mensimulasikan pembacaan file dan komputasi berat
    # time.sleep(0.1) # Simulasi baca file
    s = 0
    # Simulasi komputasi berat
    for i in range(10**6):
        s += (i * hash(file_path)) % 17
    return f"Hasil dari {os.path.basename(file_path)}"

# Stage 3: Aggregator
# Mengumpulkan hasil dari para worker.
def aggregator(q_out):
    print("Aggregator: Memulai...")
    results = []
    while True:
        result = q_out.get()
        if result is None:
            break
        results.append(result)
    print(f"Aggregator: Selesai. Total hasil: {len(results)}")
    return results


# --- FUNGSI UTAMA UNTUK MENJALANKAN PIPELINE ---
def run_pipeline(num_files, num_workers):
    # Membuat "file" dummy
    DUMMY_FILES = [f"data/file_{i}.txt" for i in range(num_files)]
    if not os.path.exists('data'):
        os.makedirs('data')
    for f in DUMMY_FILES:
        with open(f, 'w') as file:
            file.write("dummy content")

    # Membuat queue untuk komunikasi antar stage
    q_in = queue.Queue(maxsize=10) # maxsize untuk backpressure 
    q_out = queue.Queue()

    start_time = time.time()
    
    # 1. Mulai Loader Thread
    loader_thread = threading.Thread(target=loader, args=(DUMMY_FILES, q_in))
    loader_thread.start()

    # 2. Mulai Aggregator Thread (menunggu hasil)
    aggregator_thread = threading.Thread(target=aggregator, args=(q_out,))
    aggregator_thread.start()
    
    # 3. Mulai Process Pool untuk Worker
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        while True:
            file_path = q_in.get()
            if file_path is None: # Sinyal selesai dari loader
                break
            future = executor.submit(process_file, file_path)
            future.add_done_callback(lambda f: q_out.put(f.result()))

    # Sinyal selesai untuk aggregator
    q_out.put(None)

    # Menunggu semua thread selesai
    loader_thread.join()
    aggregator_thread.join()
    
    end_time = time.time()
    total_time = end_time - start_time

    return total_time

# --- EKSEKUSI DAN PENGUKURAN ---
if __name__ == '__main__':
    NUM_FILES = 50

    results = []
    for workers in [1, 2, 4, 8]:
        print(f"=== Menjalankan pipeline dengan {workers} workers ===")
        total_time = run_pipeline(NUM_FILES, workers)
        throughput = NUM_FILES / total_time
        avg_latency = total_time / NUM_FILES
        results.append((workers, total_time, throughput, avg_latency))

    # Cetak tabel setelah semua eksekusi selesai
    print(f"{'Threads Loader':<15} | {'Workers CPU':<12} | {'Jumlah File':<12} | {'Waktu (s)':<12} | {'Throughput (file/s)':<18} | {'Avg Latency (s)':<18}")
    print("-" * 100)

    for workers, total_time, throughput, avg_latency in results:
        print(f"{1:<15} | {workers:<12} | {NUM_FILES:<12} | {total_time:<12.4f} | {f'{throughput:.2f} file/s':<18} | {f'{avg_latency:.4f}':<18}")