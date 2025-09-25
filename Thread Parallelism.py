# Nama: Matin Rusydan
# NPM: 237006030

import time, random
from concurrent.futures import ThreadPoolExecutor

# 1. Menyiapkan 10 "file" untuk diunduh dengan durasi acak
# Durasi antara 0.5 hingga 2 detik
jobs = []
for i in range(1, 11):
    download_time = random.uniform(0.5, 2)
    jobs.append((i, download_time))

print(f"Daftar pekerjaan (file, durasi): {[(job[0], round(job[1], 2)) for job in jobs]}\n")

# Fungsi untuk mensimulasikan unduhan file
def download_file(file_number, sec):
    print(f"Mulai mengunduh file {file_number}...")
    time.sleep(sec) # Mensimulasikan waktu tunggu I/O
    print(f"Selesai mengunduh file {file_number}.")

def run_in_parallel(num_workers):
    """Menjalankan fungsi download_file secara paralel dengan jumlah thread tertentu."""
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        list(executor.map(download_file, [i for i, sec in jobs], [sec for i, sec in jobs]))  # list() untuk memastikan semua selesai

# --- EKSEKUSI DAN PENGUKURAN WAKTU ---

if __name__ == '__main__':
    # Eksekusi dengan berbagai jumlah thread
    results = {}
    for workers in [1, 2, 4, 8]:
        if workers == 1:
            mode = "Serial"
        else:
            mode = f"Thread ({workers})"
        print(f"--- Menjalankan {mode} ---")
        start = time.time()
        run_in_parallel(workers)
        end = time.time()
        t = end - start
        results[workers] = t
        print(f"Waktu eksekusi: {t:.4f} detik\n")

    # --- Menghitung Speedup ---
    print("--- Tabel Hasil ---")
    print(f"{'Mode':<15} | {'Jumlah Thread':<15} | {'Waktu (s)':<12} | {'Speedup':<10}")
    print("-" * 60)

    time_serial = results[1]
    for workers, t in results.items():
        if workers == 1:
            mode = "Serial"
            jumlah = 1
        else:
            mode = f"Thread ({workers})"
            jumlah = workers
        speedup = time_serial / t
        print(f"{mode:<15} | {jumlah:<15} | {t:<12.4f} | {f'{speedup:.2f}x':<10}")