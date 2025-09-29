# Laporan Praktikum: Thread & Task Parallelism

Repositori ini berisi kode sumber dan laporan hasil untuk tugas praktikum mata kuliah Komputasi Paralel dan Terdistribusi. Praktikum ini bertujuan untuk memahami dan membandingkan implementasi **Thread Parallelism** dan **Task Parallelism** di Python.

### Informasi Mahasiswa

- **Nama**: Dionisio Silaen
- **NPM**: 237006011
- **Kelas**: A

### Deskripsi Singkat

Praktikum ini terbagi menjadi empat bagian utama yang mengeksplorasi penggunaan *threads* dan *processes* untuk menangani dua jenis beban kerja yang berbeda:
1.  **I/O-Bound**: Tugas yang didominasi oleh waktu tunggu operasi Input/Output.
2.  **CPU-Bound**: Tugas yang didominasi oleh waktu komputasi intensif di CPU.

### Struktur Proyek

```
.
├── prak1.py            # Tugas 1: Simulasi I/O-Bound dengan Serial vs Threading
├── prak2.py            # Tugas 2: Simulasi CPU-Bound dengan Serial vs Multiprocessing
├── prak3.py            # Tugas 3: Perbandingan performa Threads vs Processes
├── prak4.py            # Tugas 4: Implementasi pipeline hibrid (Threads + Processes)
└── README.md           # Laporan hasil dan analisis praktikum
```

### Cara Menjalankan

Setiap file praktikum dapat dijalankan secara mandiri menggunakan interpreter Python 3.

```sh
# Menjalankan Tugas 1
python prak1.py

# Menjalankan Tugas 2
python prak2.py

# Menjalankan Tugas 3
python prak3.py

# Menjalankan Tugas 4
python prak4.py
```

---

## Hasil dan Analisis

### Tugas 1: Thread Parallelism (I/O-Bound Download Simulator)

#### Tabel Hasil

| Mode     | Jumlah File | Waktu (s) | Speedup |
| :------- | :---------- | :-------- | :------ |
| Serial   | 10          | 11.26     | 1.00x   |
| Threaded | 10          | 1.85      | 5.55x   |

#### Jawaban Diskusi

*   **Mengapa threads lebih efektif untuk aplikasi I/O dibanding serial?**
    Pada eksekusi serial, program harus menunggu satu tugas I/O (seperti `time.sleep` yang menyimulasikan unduhan) selesai sebelum melanjutkan ke tugas berikutnya. Selama waktu tunggu ini, CPU tidak melakukan pekerjaan apa pun (menganggur). Pada eksekusi *threaded*, ketika satu *thread* sedang menunggu (misalnya, menunggu data dari jaringan), sistem operasi dapat dengan cerdas mengalihkan eksekusi ke *thread* lain yang siap berjalan. Hal ini memungkinkan banyak tugas yang bersifat "menunggu" dapat dieksekusi secara bersamaan, sehingga total waktu eksekusi menjadi jauh lebih singkat dan mendekati waktu tugas terlama, bukan total waktu dari semua tugas.

*   **Apa potensi masalah jika terlalu banyak threads dibuat?**
    -   **Overhead**: Setiap *thread* yang dibuat memerlukan sumber daya sistem seperti memori dan waktu CPU untuk manajemen (dikenal sebagai *context switching*). Membuat ribuan *thread* dapat menghabiskan memori dan membuat sistem operasi lebih sibuk beralih antar-*thread* daripada mengerjakan tugas utamanya, yang justru dapat memperlambat kinerja.
    -   **Resource Limitation**: Sistem operasi memiliki batasan jumlah *thread* yang dapat dibuat oleh sebuah proses. Jika batas ini terlampaui, aplikasi bisa mengalami *crash* atau gagal membuat *thread* baru.
    -   **Race Conditions**: Jika beberapa *thread* mencoba untuk mengakses atau memodifikasi data yang sama secara bersamaan tanpa mekanisme penguncian yang tepat, hasilnya bisa tidak terduga dan menyebabkan *bug* yang sulit dilacak.

### Tugas 2: Task Parallelism (CPU-Bound Heavy Computation)

#### Tabel Hasil

--- Menjalankan Mode Serial ---
Waktu eksekusi serial: 1.5138 detik.
| Threaded   | 10           | 1.85       | 5.55x      |
| Threaded   | 10           | 1.85       | 5.55x      |
| Threaded   | 10           | 1.85       | 5.55x      |


| Proses   | Waktu (s)  | Speedup    | Efisiensi  |
| -------- | ---------- | ---------- | ---------- |
| 1 (Serial) | 1.5138     | 1.00x      | 100.00%    |
| -------- | ---------- | ---------- | ---------- |
| 1 (Serial) | 1.5138     | 1.00x      | 100.00%    |
| 2        | 1.0504     | 1.44x      | 72.05%     |
| 1 (Serial) | 1.5138     | 1.00x      | 100.00%    |
| 2        | 1.0504     | 1.44x      | 72.05%     |
| 2        | 1.0504     | 1.44x      | 72.05%     |
| 2        | 1.0504     | 1.44x      | 72.05%     |
| 2        | 1.0504     | 1.44x      | 72.05%     |
| 4        | 0.6139     | 2.47x      | 61.65%     |
| 8        | 0.7415     | 2.04x      | 25.52%     |


#### Jawaban Diskusi

*   **Mengapa task parallelism (proses) lebih efektif untuk CPU-bound dibanding thread?**
    Ini disebabkan oleh adanya **Global Interpreter Lock (GIL)** di Python. GIL adalah sebuah mekanisme yang hanya mengizinkan satu *thread* untuk mengeksekusi *bytecode* Python pada satu waktu dalam satu proses. Akibatnya, meskipun kita membuat banyak *thread* untuk tugas CPU-bound, hanya satu *thread* yang benar-benar bekerja pada satu inti CPU pada satu waktu. Sebaliknya, setiap **proses** memiliki interpreter dan GIL-nya sendiri, memungkinkan beberapa proses berjalan secara paralel sejati pada beberapa inti CPU yang berbeda, sehingga sangat efektif untuk mempercepat tugas-tugas CPU-bound.

*   **Apa peran GIL (Global Interpreter Lock) dalam Python?**
    Peran utama GIL adalah untuk menyederhanakan manajemen memori di Python dengan melindunginya dari akses serentak. Ini mencegah *race condition* pada level internal CPython. Namun, efek sampingnya adalah ia membatasi eksekusi paralel dari *thread* pada tugas-tugas yang terikat CPU. Untuk tugas I/O-bound, GIL tidak menjadi masalah karena *thread* akan melepaskan GIL saat menunggu operasi I/O, memungkinkan *thread* lain berjalan.

### Tugas 3: Perbandingan Threads vs Processes

#### Tabel Hasil

| Jenis Aplikasi | Serial (s) | Threads (s) | Processes (s) | Speedup Threads | Speedup Processes |
| :------------- | :--------- | :---------- | :------------ | :-------------- | :---------------- |
| I/O-Bound      | 2.6619     | 0.7056      | 0.8855        | 3.77x           | 3.01x             |
| CPU-Bound      | 0.7246     | 0.7592      | 0.4144        | 0.95x           | 1.75x             |

#### Jawaban Diskusi

*   **Jelaskan perbedaan hasil antara aplikasi I/O-bound dan CPU-bound.**
    -   **I/O-bound**: *Threads* menunjukkan performa yang sangat baik karena saat satu *thread* menunggu I/O, *thread* lain bisa berjalan. *Processes* juga memberikan percepatan, tetapi *overhead* untuk membuat proses lebih besar daripada *thread*, sehingga *threads* cenderung lebih efisien di sini.
    -   **CPU-bound**: *Threads* menunjukkan *speedup* yang buruk (bahkan bisa lebih lambat) karena batasan GIL. Sebaliknya, *processes* menunjukkan *speedup* yang signifikan karena setiap proses berjalan pada intinya sendiri tanpa terhalang GIL.

*   **Apa implikasi pemilihan threads vs processes pada desain sistem nyata?**
    -   **Gunakan Threads** ketika aplikasi melakukan banyak operasi yang melibatkan penungguan, seperti mengakses API web, *database*, atau membaca/menulis file.
    -   **Gunakan Processes** ketika aplikasi perlu melakukan komputasi berat dan paralel, seperti pemrosesan gambar/video, simulasi ilmiah, atau analisis data besar.

### Tugas 4: Hybrid Pipeline (Threads + Processes)

#### Tabel Hasil

--- Hasil Pipeline ---
Total file diproses : 20
--- Hasil Pipeline ---
Total file diproses : 20
Total kata dihitung : 12600
Waktu total         : 0.2393 s
Total kata dihitung : 12600
Waktu total         : 0.2393 s
Throughput          : 83.57 file/s
Avg Latency         : 0.0120 s/file
Avg Latency         : 0.0120 s/file
Avg Latency         : 0.0120 s/file
Avg Latency         : 0.0120 s/file
Avg Latency         : 0.0120 s/file
Avg Latency         : 0.0120 s/file
Avg Latency         : 0.0120 s/file
Avg Latency         : 0.0120 s/file

#### Jawaban Diskusi

*   **Dimana bottleneck pipeline terjadi?**
    *Bottleneck* (kemacetan) kemungkinan besar terjadi di **Stage-2 (process pool)**. Membaca path file (Stage 1) sangat cepat (I/O ringan). Namun, pemrosesan file yang intensif secara CPU akan memakan waktu paling lama. Jika *worker* CPU tidak dapat mengimbangi kecepatan *loader*, maka `task_queue` akan menumpuk.

*   **Bagaimana peran backpressure (queue maxsize) dalam pipeline ini?**
    Dengan menyetel `queue.Queue(maxsize=...)`, kita bisa menerapkan *backpressure* (tekanan balik) untuk membatasi ukuran antrian. Jika antrian penuh, *loader thread* akan berhenti sejenak saat mencoba memasukkan item baru. Ini secara otomatis menyinkronkan kecepatan tahap yang cepat (loader) dengan tahap yang lambat (worker), mencegah penggunaan memori yang berlebihan.

*   **Bagaimana menyesuaikan jumlah thread vs proses untuk optimasi?**
    -   **Jumlah Threads Loader (Stage 1)**: Biasanya **satu *thread*** sudah cukup, karena ini adalah tugas I/O yang sangat ringan.
    -   **Jumlah Proses Workers (Stage 2)**: Ini adalah parameter paling penting. Jumlah ideal biasanya **sama dengan jumlah inti CPU** yang tersedia. Terlalu sedikit akan membuat inti CPU menganggur; terlalu banyak akan menyebabkan *overhead* dari *context switching* yang justru menurunkan performa.
