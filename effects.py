"""
Kumpulan fungsi easing (smoothstep, ease-out-cubic, ease-in-out-cubic) dan 
util visual kecil seperti fungsi wave untuk efek bendera berkibar. 
Semua vectorized agar kompatibel dengan array NumPy di particle system.
"""

import numpy as np


def smoothstep(t):
    """Klasik smoothstep: halus di kedua ujung (0 dan 1)."""
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def ease_out_cubic(t):
    """Cepat di awal, melambat menuju target. Cocok untuk particle 'mendarat'."""
    t = np.clip(t, 0.0, 1.0)
    return 1.0 - (1.0 - t) ** 3


def ease_in_out_cubic(t):
    """Lambat - cepat - lambat. Dipakai untuk transisi yang terasa 'cinematic'."""
    t = np.clip(t, 0.0, 1.0)
    return np.where(t < 0.5, 4.0 * t ** 3, 1.0 - ((-2.0 * t + 2.0) ** 3) / 2.0)


def wave_offset(y, time_elapsed, amplitude, frequency, phase_scale=0.02):
    """Menghasilkan offset horizontal untuk efek bendera berkibar."""
    return np.sin(time_elapsed * frequency + y * phase_scale) * amplitude


def lerp_color(current, target, factor):
    """Interpolasi warna sederhana (dipakai di luar numpy vector update bila perlu)."""
    return current + (target - current) * factor
