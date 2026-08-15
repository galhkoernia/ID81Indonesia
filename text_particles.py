"""
Generator koordinat target particle untuk teks. 
Font hanya dipakai sebagai sumber bentuk (mask alpha) bukan langsung ditampilkan 
sehingga hasil akhir tulisan (DIRGAHAYU, 81, MERDEKA!, dst) benar-benar tersusun dari particle.
"""

import numpy as np
import pygame

from config import FONT_CANDIDATES

_font_cache = {}


def load_font(size, bold=True):
    """Cari font modern yang tersedia di sistem, dengan fallback berlapis."""
    key = (size, bold)
    if key in _font_cache:
        return _font_cache[key]

    font = None
    for name in FONT_CANDIDATES:
        try:
            path = pygame.font.match_font(name, bold=bold)
        except Exception:
            path = None
        if path:
            font = pygame.font.Font(path, size)
            break

    if font is None:
        # fallback terakhir: font bawaan pygame, tetap jalan tanpa install apa pun
        font = pygame.font.Font(None, size)

    _font_cache[key] = font
    return font


def generate_text_targets(text, size, screen_w, screen_h, sample_step=3,
                           max_particles=None, y_offset=0, x_offset=0, bold=True):
    """
    Hasilkan array (N, 2) koordinat particle yang membentuk `text`.
    """
    font = load_font(size, bold=bold)
    text_surface = font.render(text, True, (255, 255, 255)).convert_alpha()
    tw, th = text_surface.get_size()

    x0 = (screen_w - tw) / 2.0 + x_offset
    y0 = (screen_h - th) / 2.0 + y_offset

    # array_alpha mengembalikan COPY (bukan reference terkunci ke surface),
    # bentuknya (width, height) sehingga nonzero() langsung memberi (x, y).
    alpha_array = pygame.surfarray.array_alpha(text_surface)
    xs, ys = np.nonzero(alpha_array > 60)

    if len(xs) == 0:
        return np.zeros((0, 2), dtype=np.float64)

    step = max(1, int(sample_step))
    grid_mask = (xs % step == 0) & (ys % step == 0)
    xs = xs[grid_mask]
    ys = ys[grid_mask]

    coords = np.stack([xs, ys], axis=1).astype(np.float64)
    coords[:, 0] += x0
    coords[:, 1] += y0

    if max_particles is not None and len(coords) > max_particles:
        idx = np.random.choice(len(coords), max_particles, replace=False)
        coords = coords[idx]

    return coords


def text_bounding_size(text, size, bold=True):
    """Util kecil untuk mengetahui lebar/tinggi render teks (dipakai untuk layout)."""
    font = load_font(size, bold=bold)
    return font.size(text)
