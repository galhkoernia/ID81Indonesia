"""
flag_particles.py
Menghasilkan koordinat target particle yang membentuk Bendera Merah Putih
Indonesia (proporsi 2:3), dengan sedikit variasi acak supaya tidak terlihat
seperti grid yang terlalu sempurna.
"""

import numpy as np

from config import RED_COLOR, WHITE_COLOR


def generate_flag_targets(screen_w, screen_h, particle_count, scale=0.42):
    """
    Return (coords, colors):
        coords : (particle_count, 2) posisi target di layar
        colors : (particle_count, 3) warna RGB masing-masing particle
    """
    flag_w = screen_w * scale
    flag_h = flag_w * (2.0 / 3.0)   # rasio resmi bendera Indonesia = 2:3

    x0 = (screen_w - flag_w) / 2.0
    y0 = (screen_h - flag_h) / 2.0

    half = particle_count // 2
    rest = particle_count - half

    # sedikit jitter di tepi supaya bentuk terasa organik, bukan grid kaku
    jitter = flag_w * 0.004

    red_x = np.random.uniform(x0, x0 + flag_w, half)
    red_y = np.random.uniform(y0, y0 + flag_h / 2.0, half)
    red_x += np.random.uniform(-jitter, jitter, half)

    white_x = np.random.uniform(x0, x0 + flag_w, rest)
    white_y = np.random.uniform(y0 + flag_h / 2.0, y0 + flag_h, rest)
    white_x += np.random.uniform(-jitter, jitter, rest)

    coords = np.concatenate([
        np.stack([red_x, red_y], axis=1),
        np.stack([white_x, white_y], axis=1),
    ], axis=0)

    colors = np.concatenate([
        np.tile(np.array(RED_COLOR, dtype=np.float64), (half, 1)),
        np.tile(np.array(WHITE_COLOR, dtype=np.float64), (rest, 1)),
    ], axis=0)

    return coords, colors
