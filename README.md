# 🇮🇩 81 TAHUN MERDEKA

### Interactive Particle Animation — Hari Kemerdekaan Republik Indonesia 2026

> Sebuah **cinematic interactive particle experience** yang memvisualisasikan perjalanan dari titik-titik cahaya menjadi **Bendera Merah Putih**, kemudian berubah menjadi pesan **Dirgahayu Republik Indonesia**, **81 Tahun Kemerdekaan**, hingga mencapai klimaks **MERDEKA!**

---

## Tentang Project

**81 TAHUN MERDEKA** adalah project creative coding berbasis **Python + Pygame + NumPy** yang dibuat untuk memperingati Hari Kemerdekaan Republik Indonesia ke-81 pada tahun 2026.

Project ini tidak menggunakan slideshow atau pergantian teks sederhana.

Setiap elemen visual utama dibangun menggunakan **particle system**.

Partikel dapat:

* membentuk objek,
* berpindah menuju target,
* menyebar,
* kembali berkumpul,
* merespons pergerakan mouse,
* menghasilkan particle burst,
* dan bertransformasi dari satu visual menjadi visual lainnya.

Konsep utama:

```text
                    PARTICLES
                        │
                        ▼
               🇮🇩 BENDERA INDONESIA
                        │
                        ▼
                  FLAG WAVING
                        │
                        ▼
                  FLAG DISSOLVE
                        │
                        ▼
                 DIRGAHAYU
                        │
                        ▼
             REPUBLIK INDONESIA
                        │
                        ▼
                17 AGUSTUS 1945
                        │
                        ▼
                       81
                        │
                        ▼
              TAHUN KEMERDEKAAN
                        │
                        ▼
                   MERDEKA!
```

---

## Konsep Visual

Project dirancang sebagai **motion graphic interaktif**, bukan aplikasi dengan tampilan UI konvensional.

### Visual Direction

* Cinematic
* Minimalist
* Modern
* Elegant
* Patriotic
* Particle-based
* Smooth motion
* Dark background
* Subtle glow
* Responsive interaction

Palet warna utama:

| Elemen     | Warna          |
| ---------- | -------------- |
| Background | Dark / Black   |
| Primary    | Indonesian Red |
| Secondary  | White          |
| Supporting | Neutral Gray   |

Tidak menggunakan efek neon berlebihan atau animasi yang terlalu ramai.

Tujuannya adalah membuat visual yang terasa **sederhana tetapi berkelas**.

---

# Fitur Utama

## 🇮🇩 Particle-Based Indonesian Flag

Bendera Merah Putih tidak ditampilkan sebagai gambar statis.

Bendera dibentuk dari ribuan particle yang bergerak menuju koordinat target.

```text
Random Particles
       ↓
Target Coordinates
       ↓
🇮🇩 Indonesian Flag
```

---

## Flag Wave Animation

Setelah terbentuk, partikel bendera bergerak menggunakan fungsi gelombang sehingga menghasilkan efek **bendera berkibar**.

Gerakan dibuat secara subtle agar tetap terlihat natural dan tidak berlebihan.

---

## Particle Dissolve

Bendera kemudian mengalami transformasi:

```text
FLAG
  ↓
DISSOLVE
  ↓
SCATTER
  ↓
PARTICLES
```

Particle tidak langsung dihapus.

Particle yang sama digunakan kembali untuk membentuk scene berikutnya.

---

## Particle Typography

Tulisan utama juga dibuat dari particle.

Text diproses menggunakan:

```text
Font
  ↓
Text Mask
  ↓
Pixel Sampling
  ↓
Particle Coordinates
  ↓
Particle Formation
```

Dengan pendekatan tersebut, teks seperti:

* `DIRGAHAYU`
* `REPUBLIK INDONESIA`
* `17 AGUSTUS 1945`
* `81`
* `TAHUN KEMERDEKAAN`
* `MERDEKA!`

tidak hanya berupa font biasa.

Secara visual, teks benar-benar tersusun dari partikel.

---

## 81 Tahun Kemerdekaan

Project menampilkan angka:

# 81

sebagai visual utama.

Angka tersebut merepresentasikan **81 tahun kemerdekaan Indonesia pada 2026**.

Visual kemudian dilengkapi dengan:

```text
81

TAHUN KEMERDEKAAN

1945 — 2026
```

---

# Interactive Particle System

Project tidak hanya bersifat pasif.

Particle dapat merespons input pengguna.

### Mouse Movement

Ketika cursor mendekati particle:

```text
        • • • •
      • • • • • •
    • •    🖱️    • •
      • • • • • •
        • • • •
```

Particle akan terdorong menjauh.

Ketika cursor menjauh, particle perlahan kembali menuju posisi target.

---

## Mouse Click Particle Burst

Klik kiri menghasilkan particle burst.

Particle di sekitar cursor akan:

1. terdorong keluar,
2. bergerak dengan easing,
3. sedikit berubah ukuran/opacity,
4. kemudian kembali menuju formasi awal.

Efek dibuat tetap cinematic dan tidak menyerupai efek ledakan game.

---

# Scene System

Animasi menggunakan sistem scene sehingga setiap bagian dapat dikembangkan secara independen.

```text
INTRO
  ↓
FLAG_FORMING
  ↓
FLAG_WAVING
  ↓
FLAG_DISSOLVE
  ↓
TEXT_DIRGAHAYU
  ↓
TEXT_REPUBLIC
  ↓
TEXT_DATE
  ↓
NUMBER_81
  ↓
INTERACTIVE
  ↓
FINALE
  ↓
ENDING
```

Setiap scene memiliki lifecycle:

```text
enter()
update(dt)
draw()
exit()
```

Pendekatan ini membuat project lebih mudah dikembangkan dan dirawat.

---

# ⌨Keyboard Controls

| Tombol  | Fungsi                            |
| ------- | --------------------------------- |
| `SPACE` | Skip / lanjut ke scene berikutnya |
| `R`     | Restart seluruh animasi           |
| `F`     | Toggle fullscreen / windowed      |
| `ESC`   | Keluar dari aplikasi              |

### Mouse

| Input      | Fungsi                    |
| ---------- | ------------------------- |
| Move       | Interaksi dengan particle |
| Left Click | Particle burst            |

---

# Teknologi

Project dibangun menggunakan:

* **Python 3.12+**
* **Pygame**
* **NumPy**

### Python

Digunakan sebagai bahasa utama untuk seluruh sistem:

* particle engine,
* scene management,
* animation,
* interaction,
* rendering.

### Pygame

Digunakan untuk:

* window management,
* rendering,
* keyboard input,
* mouse input,
* timing,
* display management.

### NumPy

Digunakan untuk membantu perhitungan posisi particle secara efisien.

---

# Arsitektur Project

Struktur project yang direkomendasikan:

```text
independence_day_81/
│
├── main.py
├── config.py
│
├── particles.py
├── scenes.py
├── text_particles.py
├── flag_particles.py
├── effects.py
├── interaction.py
│
├── requirements.txt
├── README.md
│
└── assets/
    └── fonts/
```

### Tanggung Jawab Modul

| File                | Tanggung Jawab                         |
| ------------------- | -------------------------------------- |
| `main.py`           | Entry point aplikasi dan main loop     |
| `config.py`         | Konfigurasi global                     |
| `particles.py`      | Particle engine                        |
| `scenes.py`         | Scene management dan scene transitions |
| `text_particles.py` | Konversi text menjadi particle targets |
| `flag_particles.py` | Generator particle Bendera Merah Putih |
| `effects.py`        | Visual effects dan easing              |
| `interaction.py`    | Mouse dan keyboard interaction         |
| `requirements.txt`  | Python dependencies                    |
| `README.md`         | Dokumentasi project                    |
| `assets/fonts/`     | Font tambahan jika diperlukan          |

---

# System Requirements

Project dirancang agar dapat berjalan pada laptop/desktop modern tanpa GPU dedicated.

### Minimum

* Windows 10 / 11
* Python 3.12+
* RAM 4 GB
* Integrated Graphics
* Display dengan resolusi minimal 1280×720

### Recommended

* Windows 10 / 11
* Python 3.12+
* RAM 8 GB+
* Modern integrated graphics atau dedicated GPU
* Display 1920×1080

Project menargetkan:

```text
Target FPS: 60
Particle Count: ±3.000–5.000
```

Jumlah particle dapat disesuaikan melalui konfigurasi.

---

# Installation

## 1. Clone Repository

```bash
git clone <repository-url>
cd independence_day_81
```

> Ganti `<repository-url>` dengan URL repository project.

Jika project tidak menggunakan Git, cukup buka folder project melalui terminal.

---

## 2. Pastikan Python Terinstall

Periksa versi Python:

```bash
python --version
```

atau:

```bash
py --version
```

Pastikan menggunakan:

```text
Python 3.12+
```

---

# 3. Membuat Virtual Environment

Disarankan menggunakan virtual environment agar dependency project terisolasi.

### Windows

```bash
python -m venv .venv
```

Aktifkan:

```bash
.venv\Scripts\activate
```

Jika menggunakan PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

---

### Linux / macOS

```bash
python3 -m venv .venv
```

Aktifkan:

```bash
source .venv/bin/activate
```

---

# 4. Install Dependencies

Pastikan virtual environment aktif.

Kemudian:

```bash
pip install -r requirements.txt
```

Dependency utama:

```text
pygame
numpy
```

---

#  5. Menjalankan Project

Setelah dependency selesai diinstall:

```bash
python main.py
```

Atau pada Windows:

```bash
py main.py
```

Aplikasi akan membuka visualisasi dalam mode fullscreen sesuai konfigurasi.

---

# Windowed Development Mode

Selama proses pengembangan, disarankan menggunakan mode windowed terlebih dahulu.

Konfigurasi dapat diatur melalui:

```text
config.py
```

Misalnya:

```python
FULLSCREEN = False
```

Setelah project siap dipresentasikan:

```python
FULLSCREEN = True
```

---

# Configuration

Parameter utama dapat diatur melalui:

```text
config.py
```

Contoh:

```python
TARGET_FPS = 60
PARTICLE_COUNT = 4000

BACKGROUND_COLOR = ...
RED_COLOR = ...
WHITE_COLOR = ...
```

Parameter scene juga dapat disesuaikan:

```python
INTRO_DURATION = ...
FLAG_DURATION = ...
TEXT_DURATION = ...
FINALE_DURATION = ...
```

Dengan konfigurasi terpusat, perubahan visual tidak perlu dilakukan pada banyak file.

---

# Performance

Project dirancang dengan mempertimbangkan performa laptop.

Beberapa pendekatan optimasi:

* target 60 FPS,
* delta-time animation,
* particle count terkontrol,
* precomputed text coordinates,
* precomputed flag coordinates,
* sampling text mask,
* reusable particle objects,
* menghindari operasi berat berulang,
* adaptive particle quality.

### Adaptive Quality

Jika FPS menurun, jumlah particle dapat dikurangi secara dinamis.

Contoh:

```text
FPS ≥ 55
HIGH QUALITY

FPS 45–54
MEDIUM QUALITY

FPS < 45
LOW QUALITY
```

Tujuannya adalah mempertahankan animasi tetap responsif.

---

# Delta Time

Animasi tidak menggunakan delay berbasis:

```python
time.sleep()
```

Sebagai gantinya, project menggunakan delta time:

```python
dt = clock.get_time() / 1000.0
```

Dengan pendekatan ini, kecepatan animasi tidak bergantung secara langsung pada jumlah frame per detik.

---

# Resolution Independence

Project tidak mengunci visual pada satu resolusi.

Sistem menggunakan:

```python
screen_width
screen_height
```

sehingga visual dapat menyesuaikan berbagai display seperti:

```text
1280 × 720
1366 × 768
1600 × 900
1920 × 1080
2560 × 1440
```

Ukuran dan posisi elemen dihitung secara relatif terhadap ukuran layar.

---

# Font

Project memiliki sistem fallback font.

Prioritas font dapat mencakup:

1. DejaVu Sans
2. Arial
3. Liberation Sans
4. System fallback

Jika ingin menggunakan font tertentu, letakkan file font di:

```text
assets/fonts/
```

Kemudian sesuaikan konfigurasi font pada project.

### Rekomendasi

Gunakan font:

* sans-serif,
* bold,
* clean,
* modern,
* mudah dibaca.

Hindari font dekoratif yang terlalu rumit karena dapat mengurangi kualitas particle typography.

---

# Particle Text Pipeline

Text particle dibuat melalui pipeline:

```text
"MERDEKA!"
     │
     ▼
Font Rendering
     │
     ▼
Alpha Mask
     │
     ▼
Pixel Sampling
     │
     ▼
Coordinate Extraction
     │
     ▼
Particle Target Positions
     │
     ▼
Particle Formation
```

Metode ini memungkinkan satu particle system digunakan untuk membentuk berbagai kata dan angka.

---

# 🇮🇩 Flag Particle Pipeline

Bendera dibuat menggunakan koordinat target:

```text
Flag Dimensions
      │
      ▼
Red / White Region
      │
      ▼
Particle Sampling
      │
      ▼
Target Coordinates
      │
      ▼
Particle Formation
      │
      ▼
Wave Animation
```

Dengan demikian bendera dapat:

* terbentuk,
* berkibar,
* terurai,
* menyebar,
* dan berubah menjadi formasi particle lainnya.

---

# Design Philosophy

Project ini menggunakan prinsip:

> **One Particle System — Multiple Forms**

Particle yang sama digunakan untuk membentuk berbagai visual.

```text
PARTICLES
    │
    ├── FLAG
    │
    ├── DIRGAHAYU
    │
    ├── REPUBLIK INDONESIA
    │
    ├── 17 AGUSTUS 1945
    │
    ├── 81
    │
    └── MERDEKA!
```

Hal ini membuat transisi terasa sebagai satu perjalanan visual yang berkesinambungan.

---

# Visual Story

Secara naratif, animasi menggambarkan:

### 1. Keheningan

Satu titik muncul dalam kegelapan.

### 2. Persatuan

Ribuan titik berkumpul.

### 3. Identitas

Titik membentuk Merah Putih.

### 4. Perjalanan

Bendera terurai menjadi partikel.

### 5. Perayaan

Partikel membentuk pesan kemerdekaan.

### 6. Refleksi

Angka `81` menjadi simbol perjalanan kemerdekaan.

### 7. Interaksi

Pengguna dapat menyentuh dan memengaruhi partikel.

### 8. Klimaks

Semua partikel membentuk:

# MERDEKA!

---

# Troubleshooting

## `ModuleNotFoundError: No module named 'pygame'`

Install Pygame:

```bash
pip install pygame
```

atau:

```bash
pip install -r requirements.txt
```

---

## `ModuleNotFoundError: No module named 'numpy'`

Install NumPy:

```bash
pip install numpy
```

atau:

```bash
pip install -r requirements.txt
```

---

## Program Terasa Lag

Coba turunkan:

```python
PARTICLE_COUNT
```

misalnya dari:

```python
PARTICLE_COUNT = 5000
```

menjadi:

```python
PARTICLE_COUNT = 3000
```

Kemudian jalankan kembali.

Pastikan juga tidak ada aplikasi berat lain yang berjalan di background.

---

## Fullscreen Bermasalah

Coba jalankan dalam mode windowed:

```python
FULLSCREEN = False
```

Jika mode windowed berjalan normal, periksa display/driver GPU sistem.

---

## Font Tidak Ditemukan

Pastikan font tersedia di:

```text
assets/fonts/
```

atau gunakan system font fallback yang tersedia.

---

# Project Safety

Project ini hanya melakukan:

* rendering graphics,
* particle calculations,
* keyboard input,
* mouse input,
* local asset loading.

Project tidak membutuhkan:

* koneksi internet,
* database,
* API key,
* akun online,
* server eksternal,
* cloud service.

Seluruh animasi berjalan secara lokal pada komputer.

---

# Recommended Git Structure

Jika project dikelola menggunakan Git:

```text
independence_day_81/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── main.py
├── config.py
├── particles.py
├── scenes.py
├── text_particles.py
├── flag_particles.py
├── effects.py
├── interaction.py
│
└── assets/
    └── fonts/
```

---

# 🇮🇩 81 TAHUN INDONESIA MERDEKA

Project ini dibuat sebagai bentuk apresiasi terhadap perjalanan panjang kemerdekaan Republik Indonesia.

Dari satu titik menjadi ribuan.

Dari ribuan titik menjadi Merah Putih.

Dari Merah Putih menjadi sebuah pesan.

Dan akhirnya:

# MERDEKA!

**Dirgahayu Republik Indonesia.**

**81 Tahun Indonesia Merdeka — 1945–2026** 🇮🇩

---

## Developer

<table align="center">
  <tr>
    <td align="center" style="padding: 20px; background-color: #F6F4EF; border: 1px solid #D8CFC5;">
      <b>galhkoernia</b>
      <br />
      <sub>Developer</sub>
      <br /><br />
      <sub>
        <a href="https://github.com/galhkoernia">GitHub</a>
        &nbsp;&middot;&nbsp;
        <a href="mailto:galuhkoernia@gmail.com">Email</a>
      </sub>
    </td>
  </tr>
</table>

Built with:

**Python · Pygame · NumPy · Creative Coding · Particle Systems**

Designed as an interactive digital celebration of Indonesian Independence Day.
