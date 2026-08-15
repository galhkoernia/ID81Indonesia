"""
Pusat konfigurasi seluruh project resolusi, jumlah particle, palet warna, 
daftar font fallback, durasi tiap scene, parameter interaksi mouse, dan 
parameter easing/wave. Tidak ada logic di sini, hanya konstanta.

"""

# DISPLAY
DEV_MODE = False            # True = jalan windowed pakai WINDOWED_SIZE, False = fullscreen native
WINDOWED_SIZE = (1280, 720)
TARGET_FPS = 60

# PARTICLES
PARTICLE_COUNT = 4000        # jumlah target di quality HIGH (3000-5000 disarankan)
PARTICLE_COUNT_MEDIUM = 2600
PARTICLE_COUNT_LOW = 1600

# Adaptive quality thresholds (berdasarkan FPS rata-rata beberapa frame terakhir)
FPS_HIGH_THRESHOLD = 55
FPS_MEDIUM_THRESHOLD = 45

# COLORS  (R, G, B)
BACKGROUND_COLOR = (6, 6, 10)
RED_COLOR = (206, 17, 38)     # merah bendera Indonesia
WHITE_COLOR = (245, 245, 245)
GRAY_COLOR = (150, 150, 155)

# TYPOGRAPHY
# Prioritas font sans-serif modern & tegas. match_font akan mencoba satu per satu.
FONT_CANDIDATES = [
    "dejavusans",
    "arial",
    "liberationsans",
    "helvetica",
    "verdana",
]
FONT_DIR = "assets/fonts"     # taruh .ttf custom di sini jika ingin override (lihat README)

TEXT_SAMPLE_STEP = 3          # jarak antar sample pixel untuk mask teks (lebih besar = lebih jarang titik)

# SCENE DURATIONS (detik)
SCENE_DURATIONS = {
    "intro": 3.0,
    "flag_forming": 4.5,
    "flag_waving": 4.0,
    "flag_dissolve": 2.2,
    "text_dirgahayu": 4.5,
    "text_republic": 5.0,
    "number_81": 5.0,
    "interactive": 7.0,
    "finale": 6.5,
}

# INTERACTION
MOUSE_REPEL_RADIUS = 120.0
MOUSE_REPEL_STRENGTH = 220.0
CLICK_BURST_RADIUS = 190.0

# EASING / MOTION
DEFAULT_MOVE_DURATION = 1.3
MOVE_STAGGER = 0.7            # variasi durasi antar particle supaya tidak bergerak serentak & kaku

# FLAG WAVE
FLAG_WAVE_AMPLITUDE = 5.0
FLAG_WAVE_FREQUENCY = 1.8
