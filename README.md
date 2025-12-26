# **🕵️‍♀️ Alice's Modular Word Search Game**

Sebuah permainan **Cari Kata (Word Search)** tingkat lanjut yang dibangun menggunakan **Python** dan library **Pygame**.

Game ini tidak hanya sekadar mencari kata, tetapi juga dirancang dengan struktur kode **Modular** yang rapi, sistem **Multi-Level**, algoritma penempatan **Zig-Zag**, dan antarmuka **Menu Utama** yang interaktif.

## **✨ Fitur Unggulan**

### **🎮 Gameplay & Fitur**

- **Sistem Multi-Level:** Game terdiri dari berbagai level (Alice, Hewan, Coding) dengan transisi otomatis saat level selesai.
- **Menu Utama Interaktif:** Dilengkapi halaman Menu Utama, Halaman Petunjuk (How to Play), dan Pause Menu.
- **Grid Cerdas (Zig-Zag):** Algoritma generator memastikan variasi orientasi kata (Horizontal & Vertikal) seimbang.
- **Validasi 2 Arah:** Mendeteksi jawaban dari kiri-ke-kanan/atas-ke-bawah maupun sebaliknya (terbalik).
- **Visual Feedback:** Efek _Hover_ pada tombol, serta indikator warna saat seleksi huruf.

### **💻 Teknis & Struktur**

- **Modular Code:** Kode dipisah berdasarkan fungsinya (`main.py`, `ui.py`, `utils.py`, `levels.py`, `settings.py`) untuk kemudahan maintenance.
- **Safe Asset Loading:** Game memiliki mekanisme _fallback_. Jika gambar tidak ditemukan, game otomatis menggunakan grafis bawaan (kotak warna) tanpa error.

## **📂 Struktur Folder Proyek**

Berikut adalah susunan file dalam proyek ini agar mudah dipahami:

```text
📁 project_folder/
│
├── 📜 main.py        # File Utama (Jalankan file ini!)
├── 📜 pages.py          # Mengatur tampilan Menu, Tombol, dan Petunjuk
├── 📜 levels.py      # Database soal dan jawaban per level
├── 📜 utils.py       # Algoritma generator grid & logika acak
├── 📜 settings.py    # Konfigurasi warna, ukuran layar, dan font
│
└── 📁 assets/        # (Opsional) Tempat menyimpan gambar & font
    ├── bg.jpg
    ├── tile.png
    ├── tile_select.png
    ├── tile_correct.png
    └── alice_font.ttf
```

## **🛠️ Prasyarat (Requirements)**

Sebelum menjalankan game ini, pastikan komputer kamu memiliki:

1. **Python 3.x** terinstal.
2. Library **Pygame**.

## **📦 Cara Instalasi & Menjalankan**

1. **Clone atau Download** repositori ini ke komputer kamu.
2. Buka terminal/command prompt di folder proyek.
3. Instal library yang dibutuhkan (jika belum ada):

```bash
pip install pygame
```

4. Jalankan game:

```bash
python main.py
```

## **🎮 Cara Bermain**

1. **Menu Utama:** Klik tombol "MULAI" untuk masuk ke permainan, atau "PETUNJUK" untuk membaca cara main.
2. **Lihat Petunjuk:** Di sisi kanan layar terdapat daftar pertanyaan kuis (Contoh: "Tokoh utama Alice in...").
3. **Cari Kata:** Temukan jawaban dari pertanyaan tersebut di dalam grid huruf (Contoh: "WONDERLAND").
4. **Seleksi:**

   - Klik kiri dan tahan pada huruf pertama.

   - Geser (drag) mouse ke arah huruf terakhir kata tersebut.

   - Lepas tombol mouse.

5. Jika benar, huruf akan berubah menjadi **Hijau** dan jawaban di panel kanan akan terbuka.

## **⚙️ Kustomisasi (Modding)**

Karena struktur kodenya modular, kamu bisa memodifikasi game ini dengan mudah:

- **Menambah Level Baru:** Buka `levels.py` dan tambahkan entry baru ke dalam list `LEVEL_DATA`. Kamu bisa mengatur soal, jawaban, dan background spesifik per level.

- **Mengubah Warna/Ukuran:** Buka `settings.py`. Di sana kamu bisa mengubah resolusi layar (`SCREEN_WIDTH`), ukuran kotak (`GRID_SIZE`), atau palet warna.

- **Mengganti Tampilan:** Cukup ganti gambar di folder `assets/` dengan nama file yang sama. Tidak perlu mengubah kode!

_Catatan: Pastikan jawaban hanya berisi huruf kapital dan tanpa spasi agar sesuai dengan logika grid._

## **🧠 Konsep Pemrograman**

Proyek ini menerapkan prinsip Software Engineering yang baik:

- **Separation of Concerns (SoC):** Memisahkan logika game (`main.py`), tampilan (`pages.py`), dan data (`levels.py`).

- **Algorithm Design:** Logika penempatan kata Zig-Zag (Horizontal-Vertikal bergantian) untuk distribusi yang merata.

- **Error Handling:** Penggunaan blok `try-except` untuk menangani aset yang hilang.

- **State Management:** Mengelola status game (`MENU`, `PLAYING`, `LEVEL_COMPLETE`, `GAME_OVER`).

---

# **Made With** ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
