import subprocess
import sys

# Daftar script yang akan dijalankan satu per satu
scripts = [
    'Thread Parallelism.py',
    'Task Parallelism.py',
    'Perbandingan Threads vs Tasks.py',
    'Hybrid Pipeline.py'
]

# Buka file output.txt untuk output
with open('output.txt', 'w') as output_file:
    for script in scripts:
        print(f"\n=== Menjalankan {script} ===\n", file=output_file)
        try:
            # Jalankan script dan mengambil outputnya
            result = subprocess.run([sys.executable, script], capture_output=True, text=True, cwd='.')
            # Tulis output dan error ke file
            output_file.write(result.stdout)
            if result.stderr:
                output_file.write(f"Kesalahan:\n{result.stderr}\n")
        except Exception as e:
            output_file.write(f"Kesalahan saat menjalankan {script}: {str(e)}\n")

print("Semua script telah dijalankan. Output disimpan di output.txt")
