# Cara Menjalankan Program Praktikum Komputasi Distribusi Paralel

## Persyaratan
- Python 3.13 atau lebih baru
- Modul yang diperlukan: `concurrent.futures`, `threading`, `queue`, `time`, `os`, `random`

## Cara Menjalankan

### 1. Thread Parallelism.py
Simulasi unduhan file menggunakan threads.
```bash
python "Thread Parallelism.py"
```
Program akan menjalankan simulasi unduhan 10 file dengan 1, 2, 4, dan 8 threads, menampilkan waktu eksekusi dan speedup.

### 2. Task Parallelism.py
Simulasi komputasi CPU-bound menggunakan ProcessPoolExecutor.
```bash
python "Task Parallelism.py"
```
Program akan menjalankan komputasi paralel dengan 2, 4, dan 8 proses, menampilkan waktu eksekusi, speedup, dan efisiensi.

### 3. Perbandingan Threads vs Tasks.py
Perbandingan performa threads vs processes untuk I/O-bound dan CPU-bound.
```bash
python "Perbandingan Threads vs Tasks.py"
```
Program akan menjalankan pengujian untuk aplikasi I/O-bound (unduhan) dan CPU-bound (komputasi), menggunakan 10 workers untuk threads dan processes.

### 4. Hybrid Pipeline.py
Pipeline hibrid dengan threads dan processes.
```bash
python "Hybrid Pipeline.py"
```
Program akan menjalankan pipeline dengan 1, 2, 4, dan 8 CPU workers, menampilkan waktu, throughput, dan latency untuk 50 file.

### Menjalankan Semua Sekaligus
Untuk menjalankan semua program dan menyimpan output ke file:
```bash
python run_all.py
```
Output akan disimpan di `output.txt`.

## Catatan
- Pastikan tidak ada file `data/file_*.txt` yang mengganggu, karena program Hybrid Pipeline akan membuat dan menghapusnya.
- Semua program menggunakan `if __name__ == '__main__':` untuk kompatibilitas multiprocessing di Windows.