# 📘 DOKUMENTASI LENGKAP: WORD GAMES

Dokumen ini berisi informasi teknis dan panduan penggunaan aplikasi **Word Games**.

---

## **1. Cara Memainkan / Menjalankan Aplikasi**

Aplikasi ini bersifat **Portable**, artinya bisa langsung dimainkan tanpa perlu menginstal program tambahan (seperti Python).

### **Langkah-Langkah:**
1.  Buka folder proyek permainan.
2.  Masuk ke folder bernama **`dist`**.
3.  Cari file aplikasi bernama **`Word Games.exe`**.
4.  Klik ganda (Double Click) file tersebut.
5.  Game akan terbuka dan siap dimainkan!

> **Catatan:** Jika muncul peringatan keamanan dari Windows (SmartScreen), klik **"More Info"** lalu pilih **"Run Anyway"**. Ini wajar karena aplikasi ini dibuat sendiri dan belum memiliki sertifikat digital komersial.


## **🎮 Kontrol Permainan**

- **Klik Kiri (Drag):** Menandai kata di dalam kotak permainan.
- **Tombol HINT:** Membuka huruf awal dari kata yang belum ditemukan.
- **Tombol ESC:** Kembali ke menu sebelumnya (Saat bermain) atau Keluar (Di Menu Utama).
- **Tombol R:** Ulangi level saat waktu habis.
- **Tombol SPASI:** Lanjut ke level berikutnya saat menang.

---

## **2. Fitur-Fitur Game**

Game ini dirancang dengan berbagai fitur modern untuk pengalaman bermain yang seru:

*   **⚡ Sistem Drag & Drop:** Cara memilih kata yang intuitif, cukup tarik garis dari huruf awal ke akhir (mendatar atau menurun).
*   **🧩 25 Level Tematik:** Tantangan bertingkat mulai dari tema Hutan, Kota, hingga Lautan dengan tingkat kesulitan yang semakin naik.
*   **💡 Sistem Hint (Bantuan):** Tombol bantuan cerdas yang akan memberitahu lokasi huruf pertama dari kata yang belum ditemukan.
*   **⏱️ Timer & Tantangan:** Setiap level memiliki batas waktu, melatih pemain berpikir cepat dan tepat.
*   **⚙️ Menu Pengaturan:** Pemain bisa mengatur durasi waktu dan jumlah hint sesuai keinginan.
*   **📱 Responsif UI:** Tampilan yang menyesuaikan dengan rapi, termasuk text-wrapping otomatis untuk soal yang panjang.
*   **🎨 Visual & Audio:** Dilengkapi dengan background berganti, efek suara (klik, menang, salah), dan musik latar.

---

## **3. Bahasa Pemrograman & Tools**

Game ini dibangun menggunakan teknologi berikut:

*   **Bahasa Pemrograman:** Python 3.10+
    *   Dipilih karena sintaksnya yang bersih, mudah dibaca, dan sangat populer untuk pengembangan cepat.
*   **Library Utama:** Pygame (Community Edition)
    *   Library standar industri untuk pengembangan game 2D di Python. Menangani grafis, input (mouse/keyboard), dan audio.
*   **Build Tool:** PyInstaller
    *   Digunakan untuk mengonversi kode Python (`.py`) menjadi aplikasi Windows mandiri (`.exe`).

---

## **4. Proses Pembuatan Game (Step by Step)**

Berikut adalah tahapan pengembangan game ini dari awal hingga akhir:

### **Tahap 1: Perancangan Fondasi (Core Logic)**
*   **Grid Generator:** Membuat algoritma untuk menghasilkan kotak huruf acak ukuran 12x12.
*   **Word Placement:** Mengembangkan logika "Zig-Zag" agar kata bisa ditempatkan secara Horizontal atau Vertikal secara acak namun tidak bertabrakan.

### **Tahap 2: Implementasi Gameplay**
*   **Seleksi Kata:** Membuat sistem input mouse agar pemain bisa menarik garis.
*   **Validasi:** Menambahkan logika pengecekan. Jika garis yang ditarik sesuai dengan daftar kata, warnanya berubah hijau.

### **Tahap 3: Pengembangan Level & Konten**
*   **Database Level:** Menyusun file `levels.py` yang berisi 25 level dengan tema edukatif (karakter, etika, lingkungan).
*   **Sistem Paging:** Membuat menu pemilihan level (Pagination) agar 25 level bisa ditampilkan dengan rapi.

### **Tahap 4: Antarmuka Pengguna (UI/UX)**
*   **Halaman Menu:** Mendesain Main Menu, Settings, dan Halaman Instruksi.
*   **Visual Polishing:** Menambahkan gambar karakter, background yang berubah sesuai level, dan font yang menarik.
*   **Fitur "Back":** Menambahkan tombol navigasi agar pemain tidak tersesat.

### **Tahap 5: Perbaikan & Optimasi (Bug Fixing)**
*   **Crash Fix:** Memperbaiki bug "Not Responding" pada level tinggi dengan menyingkat kata-kata yang terlalu panjang agar muat di grid.
*   **Text Wrapping:** Memperbaiki tampilan soal agar tidak terpotong.

### **Tahap 6: Finalisasi & Distribusi**
*   **Branding:** Mengubah nama window menjadi "Word Games" dan menambahkan watermark pembuat.
*   **Building:** Menggunakan PyInstaller untuk membungkus semua kode dan aset (gambar/suara) menjadi satu file `.exe` yang mudah dibagikan.

---

**Dibuat oleh:**
M. Ridha Ansari Adriansyah

[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com/ridhaansaria_) 
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mridhaansariadriansyah)
