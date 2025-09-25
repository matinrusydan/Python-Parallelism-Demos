# Nama: Matin Rusydan
# NPM: 237006030

import time
from concurrent.futures import ProcessPoolExecutor

# Fungsi komputasi berat (CPU-Bound)
def heavy(n, iters=10**6):
    s = 0
    for i in range(iters):
        s += (i * n) % 17 # Operasi matematika sederhana
    return s

# Jumlah tugas yang akan dijalankan
TASKS = range(1, 17) # Kita jalankan 16 tugas

def run_in_parallel(num_workers):
    """Menjalankan fungsi heavy secara paralel dengan jumlah proses tertentu."""
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        list(executor.map(heavy, TASKS)) # list() untuk memastikan semua selesai

# --- EKSEKUSI DAN PENGUKURAN WAKTU ---

if __name__ == '__main__':
    # 1. Eksekusi Serial (setara dengan 1 proses)
    print("--- Menjalankan Serial (1 Proses) ---")
    start_serial = time.time()
    for task in TASKS:
        heavy(task)
    end_serial = time.time()
    time_serial = end_serial - start_serial
    print(f"Waktu eksekusi: {time_serial:.4f} detik\n")


    # 2. Eksekusi Paralel
    results = {}
    for workers in [2, 4, 8]:
        print(f"--- Menjalankan Paralel ({workers} Proses) ---")
        start_parallel = time.time()
        run_in_parallel(workers)
        end_parallel = time.time()
        time_parallel = end_parallel - start_parallel
        results[workers] = time_parallel
        print(f"Waktu eksekusi: {time_parallel:.4f} detik\n")


    # --- Menghitung Speedup dan Efisiensi ---
    print("--- Tabel Hasil ---")
    print(f"{'Proses':<10} | {'Waktu (s)':<12} | {'Speedup':<10} | {'Efisiensi':<10}")
    print("-" * 50)

    # Hasil Serial
    print(f"{'1 (Serial)':<10} | {time_serial:<12.4f} | {'1.00x':<10} | {'100.00%':<10}")

    # Hasil Paralel
    for workers, t_parallel in results.items():
        speedup = time_serial / t_parallel
        efisiensi = (speedup / workers) * 100
        print(f"{workers:<10} | {t_parallel:<12.4f} | {f'{speedup:.2f}x':<10} | {f'{efisiensi:.2f}%':<10}")