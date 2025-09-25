# Nama: Matin Rusydan
# NPM: 237006030

import threading, time, random
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# --- FUNGSI DARI TUGAS 1 & 2 ---

# Fungsi I/O-Bound
def download_file(sec):
    time.sleep(sec)

# Fungsi CPU-Bound
def heavy(n, iters=10**6):
    s = 0
    for i in range(iters):
        s += (i * n) % 17
    return s

# --- SETUP TUGAS ---
NUM_TASKS = 10
IO_ARGS = [random.uniform(0.1, 0.3) for _ in range(NUM_TASKS)]
CPU_ARGS = range(NUM_TASKS)

# --- FUNGSI EKSEKUSI ---
def run_serial(func, args):
    for arg in args:
        func(arg)

def run_threads(func, args):
    with ThreadPoolExecutor(max_workers=NUM_TASKS) as executor:
        executor.map(func, args)

def run_processes(func, args):
    with ProcessPoolExecutor(max_workers=NUM_TASKS) as executor:
        executor.map(func, args)

# --- EKSEKUSI DAN PENGUKURAN ---

if __name__ == '__main__':
    # 1. Aplikasi I/O-Bound
    print("--- Menguji Aplikasi I/O-Bound ---")
    start = time.time()
    run_serial(download_file, IO_ARGS)
    t_serial_io = time.time() - start

    start = time.time()
    run_threads(download_file, IO_ARGS)
    t_threads_io = time.time() - start

    start = time.time()
    run_processes(download_file, IO_ARGS)
    t_processes_io = time.time() - start

    # 2. Aplikasi CPU-Bound
    print("--- Menguji Aplikasi CPU-Bound ---")
    start = time.time()
    run_serial(heavy, CPU_ARGS)
    t_serial_cpu = time.time() - start

    start = time.time()
    run_threads(heavy, CPU_ARGS)
    t_threads_cpu = time.time() - start

    start = time.time()
    run_processes(heavy, CPU_ARGS)
    t_processes_cpu = time.time() - start


    # --- Menampilkan Tabel Hasil ---
    print("\n--- Tabel Hasil Perbandingan ---")
    header = f"{'Jenis Aplikasi':<15} | {'Serial (s)':<12} | {'Threads (s)':<12} | {'Processes (s)':<14} | {'Speedup Threads':<18} | {'Speedup Processes':<18}"
    print(header)
    print("-" * len(header))

    # Data I/O
    sp_threads_io = t_serial_io / t_threads_io
    sp_proc_io = t_serial_io / t_processes_io
    print(f"{'I/O-Bound':<15} | {t_serial_io:<12.4f} | {t_threads_io:<12.4f} | {t_processes_io:<14.4f} | {f'{sp_threads_io:.2f}x':<18} | {f'{sp_proc_io:.2f}x':<18}")

    # Data CPU
    sp_threads_cpu = t_serial_cpu / t_threads_cpu
    sp_proc_cpu = t_serial_cpu / t_processes_cpu
    print(f"{'CPU-Bound':<15} | {t_serial_cpu:<12.4f} | {t_threads_cpu:<12.4f} | {t_processes_cpu:<14.4f} | {f'{sp_threads_cpu:.2f}x':<18} | {f'{sp_proc_cpu:.2f}x':<18}")