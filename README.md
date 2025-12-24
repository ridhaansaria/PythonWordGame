# **🕵️‍♀️ Alice's Word Search Game**

Sebuah permainan **Cari Kata (Word Search)** klasik yang dibangun menggunakan **Python** dan library **Pygame**. Game ini menantang pemain untuk menemukan kata-kata tersembunyi di dalam grid acak berdasarkan petunjuk kuis bertema *"Alice in Wonderland"*.

## **✨ Fitur Utama**

- **Grid Dinamis:** Huruf-huruf diacak dan ditempatkan secara otomatis setiap kali game dimulai.

- **Orientasi Kata:** Mendukung penempatan kata secara **Horizontal (Mendatar)** dan **Vertical (Menurun)**.

- **Interaktif:** Menggunakan mouse (drag & drop) untuk memilih deretan huruf.

- **Validasi Cerdas:** Mendeteksi jawaban baik dari kiri-ke-kanan/atas-ke-bawah maupun sebaliknya (terbalik).

- **Visual Feedback:** Indikator warna untuk seleksi aktif (Biru) dan jawaban benar (Hijau).

- **Sistem Aset Aman:** Game tetap berjalan menggunakan warna default meskipun file gambar (aset) tidak ditemukan.

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
python game.py
```

## **🎮 Cara Bermain**

1. **Lihat Petunjuk:** Di sisi kanan layar terdapat daftar pertanyaan kuis (Contoh: "Tokoh utama Alice in...").
2. **Cari Kata:** Temukan jawaban dari pertanyaan tersebut di dalam grid huruf (Contoh: "WONDERLAND").
3. **Seleksi:**
    - Klik kiri dan tahan pada huruf pertama.

    - Geser (drag) mouse ke arah huruf terakhir kata tersebut.

    - Lepas tombol mouse.
4. Jika benar, huruf akan berubah menjadi **Hijau** dan jawaban di panel kanan akan terbuka.

## **📂 Struktur File & Aset**

Game ini dirancang untuk memuat aset gambar jika tersedia, namun akan menggunakan warna *fallback* jika gambar tidak ada.

- `game.py`: File utama kode program.

- (Opsional) `bg.jpg`: Gambar latar belakang (Ukuran 1000x700).

- (Opsional) `tile.png`: Gambar kotak huruf normal.

- (Opsional) `tile_select.png`: Gambar kotak saat dipilih.

- (Opsional) `tile_correct.png`: Gambar kotak saat jawaban benar.

## **⚙️ Kustomisasi Soal**

Kamu bisa mengubah pertanyaan dan jawaban dengan mudah. Buka file game.py dan edit bagian `DATA_KUIS`:

```python
DATA_KUIS = {
    "Pertanyaan Kamu": "JAWABAN",
    "Ibu Kota Indonesia": "JAKARTA",
    "Bahasa Pemrograman ini": "PYTHON"
}
```

*Catatan: Pastikan jawaban hanya berisi huruf kapital dan tanpa spasi agar sesuai dengan logika grid.*

## **🧠 Konsep Pemrograman**

Proyek ini menerapkan beberapa konsep dasar Informatika:

- **Array 2 Dimensi:** Representasi grid huruf.

- **Algoritma Pengacakan:** Penempatan kata secara acak (Randomize placement) dengan pengecekan tabrakan (collision detection).

- **Event Handling:** Memproses input mouse (Click, Drag, Release) di Pygame.

- **String Manipulation:** Membalikkan string (slicing) untuk mengecek jawaban terbalik.

---

Made With ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)