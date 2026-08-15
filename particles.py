"""
Particle engine inti berbasis NumPy (vectorized). Menyimpan posisi, target, warna, alpha, 
dan ukuran seluruh particle sebagai array, dengan method untuk bergerak menuju target (assign_targets), pecah menyebar (scatter), ledakan lokal (burst), efek dorongan mouse (repel_from_point), update per-frame, dan rendering ke layar.
"""

import numpy as np
import pygame

from effects import ease_out_cubic


class ParticleSystem:
    def __init__(self, count):
        self.count = count

        self.pos = np.zeros((count, 2), dtype=np.float64)
        self.origin = np.zeros((count, 2), dtype=np.float64)
        self.target = np.zeros((count, 2), dtype=np.float64)

        self.color = np.full((count, 3), 255.0, dtype=np.float64)
        self.target_color = np.full((count, 3), 255.0, dtype=np.float64)

        self.alpha = np.zeros(count, dtype=np.float64)
        self.target_alpha = np.zeros(count, dtype=np.float64)

        self.size = np.full(count, 2.0, dtype=np.float64)
        self.base_size = np.full(count, 2.0, dtype=np.float64)

        # gerakan halus melayang (floating) supaya particle tidak terlihat kaku/statis
        self.noise_phase = np.random.uniform(0, np.pi * 2, count)
        self.noise_speed = np.random.uniform(0.4, 1.4, count)
        self.noise_amp = np.random.uniform(0.4, 1.8, count)

        # progres interpolasi 0..1 dari origin -> target
        self.move_t = np.ones(count, dtype=np.float64)
        self.move_duration = np.ones(count, dtype=np.float64)

        self.screen_w = 0
        self.screen_h = 0

    # SETUP
    def set_screen_size(self, w, h):
        self.screen_w = w
        self.screen_h = h

    def init_random(self, screen_w, screen_h):
        """Sebar semua particle secara acak di layar, tersembunyi (alpha 0)."""
        self.set_screen_size(screen_w, screen_h)
        self.pos[:, 0] = np.random.uniform(0, screen_w, self.count)
        self.pos[:, 1] = np.random.uniform(0, screen_h, self.count)
        self.origin[:] = self.pos
        self.target[:] = self.pos
        self.alpha[:] = 0.0
        self.target_alpha[:] = 0.0
        self.move_t[:] = 1.0

    # TARGET ASSIGNMENT
    def assign_targets(self, coords, colors=None, duration=1.3, stagger=0.6, fade_extra=True):
        """
        Kirim particle menuju bentuk baru (bendera / huruf / angka).

        coords : array (M, 2) - target posisi. M boleh lebih kecil dari total count;
                 sisanya (count - M) dianggap particle 'berlebih' dan akan
                 melayang bebas lalu fade out (fade_extra=True), sehingga
                 transisi antar bentuk tetap terlihat organik.
        colors : array (M, 3) atau None (warna tetap seperti sekarang)
        """
        coords = np.asarray(coords, dtype=np.float64)
        m = min(len(coords), self.count)

        # supaya particle tidak berpindah dengan pola yang sama tiap kali
        # (mis. selalu index 0..m-1), acak particle mana yang menuju target.
        perm = np.random.permutation(self.count)
        idx_target = perm[:m]
        idx_extra = perm[m:]

        self.origin[idx_target] = self.pos[idx_target]
        self.target[idx_target] = coords[:m]
        self.target_alpha[idx_target] = 255.0
        if colors is not None:
            colors = np.asarray(colors, dtype=np.float64)
            self.target_color[idx_target] = colors[:m]
        self.move_t[idx_target] = 0.0
        self.move_duration[idx_target] = np.clip(
            duration + np.random.uniform(-stagger, stagger, m), 0.25, None
        )

        if len(idx_extra) > 0:
            self.origin[idx_extra] = self.pos[idx_extra]
            drift_x = np.random.uniform(0, self.screen_w, len(idx_extra))
            drift_y = np.random.uniform(0, self.screen_h, len(idx_extra))
            self.target[idx_extra] = np.stack([drift_x, drift_y], axis=1)
            self.target_alpha[idx_extra] = 0.0 if fade_extra else self.target_alpha[idx_extra]
            self.move_t[idx_extra] = 0.0
            self.move_duration[idx_extra] = np.clip(
                duration + np.random.uniform(0, stagger + 0.4, len(idx_extra)), 0.25, None
            )

    def scatter(self, strength=420.0, duration=1.1):
        """Pecahkan formasi saat ini menjadi particle yang menyebar (dissolve)."""
        angles = np.random.uniform(0, np.pi * 2, self.count)
        radii = np.random.uniform(strength * 0.25, strength, self.count)
        offset = np.stack([np.cos(angles), np.sin(angles)], axis=1) * radii[:, None]
        new_targets = self.pos + offset
        new_targets[:, 0] = np.clip(new_targets[:, 0], -40, self.screen_w + 40)
        new_targets[:, 1] = np.clip(new_targets[:, 1], -40, self.screen_h + 40)

        self.origin[:] = self.pos
        self.target[:] = new_targets
        self.target_alpha[:] = np.random.uniform(140.0, 255.0, self.count)
        self.move_t[:] = 0.0
        self.move_duration[:] = np.clip(
            duration + np.random.uniform(0, 0.6, self.count), 0.2, None
        )

    def burst(self, x, y, radius=180.0, strength=1.0):
        """Dorongan lokal di sekitar (x, y) - dipakai untuk efek klik mouse."""
        d = self.pos - np.array([x, y])
        dist = np.linalg.norm(d, axis=1)
        mask = dist < radius
        if not np.any(mask):
            return
        dist_safe = np.where(dist[mask] < 1e-3, 1e-3, dist[mask])
        direction = d[mask] / dist_safe[:, None]
        falloff = 1.0 - (dist[mask] / radius)
        push = direction * (falloff[:, None] * radius * 0.85 * strength)

        self.origin[mask] = self.pos[mask]
        self.target[mask] = self.pos[mask] + push
        self.move_t[mask] = 0.0
        self.move_duration[mask] = np.random.uniform(0.3, 0.55, int(mask.sum()))
        self.size[mask] = np.clip(self.base_size[mask] * 1.6, 1.0, 7.0)

    def repel_from_point(self, x, y, radius, strength, dt):
        """Dorong posisi particle secara langsung (dipakai untuk hover mouse)."""
        d = self.pos - np.array([x, y])
        dist = np.linalg.norm(d, axis=1)
        mask = (dist < radius) & (dist > 1e-3)
        if not np.any(mask):
            return
        direction = d[mask] / dist[mask][:, None]
        falloff = (1.0 - dist[mask] / radius) ** 2
        self.pos[mask] += direction * falloff[:, None] * strength * dt
        # sedikit geser origin/target juga supaya tidak "ditarik balik" mendadak
        self.origin[mask] = self.pos[mask]

    # UPDATE
    def update(self, dt, time_elapsed, wave_enabled=False, wave_amplitude=5.0, wave_frequency=1.8):
        self.move_t = np.minimum(self.move_t + dt / self.move_duration, 1.0)
        t = ease_out_cubic(self.move_t)
        base_pos = self.origin + (self.target - self.origin) * t[:, None]

        noise_x = np.sin(time_elapsed * self.noise_speed + self.noise_phase) * self.noise_amp
        noise_y = np.cos(time_elapsed * self.noise_speed * 0.8 + self.noise_phase) * self.noise_amp

        self.pos[:, 0] = base_pos[:, 0] + noise_x
        self.pos[:, 1] = base_pos[:, 1] + noise_y

        if wave_enabled:
            wave = np.sin(time_elapsed * wave_frequency + base_pos[:, 1] * 0.02) * wave_amplitude
            self.pos[:, 0] += wave * t

        blend = min(dt * 4.0, 1.0)
        self.alpha += (self.target_alpha - self.alpha) * blend
        self.color += (self.target_color - self.color) * blend
        self.size += (self.base_size - self.size) * min(dt * 2.2, 1.0)

    # DRAW
    def draw(self, surface, layer, glow=True, stride=1):
        """
        layer  : pygame.Surface(SRCALPHA) seukuran surface, dipakai ulang
                 setiap frame (dibersihkan di sini) supaya tidak alloc surface baru.
        stride : lewati sebagian particle saat quality LOW (adaptive performance).
        """
        layer.fill((0, 0, 0, 0))

        pos = self.pos
        alpha = np.clip(self.alpha, 0, 255)
        color = np.clip(self.color, 0, 255).astype(np.int32)
        size = np.clip(self.size, 0.6, 8.0)

        w, h = surface.get_size()
        visible = (
            (pos[:, 0] >= -20) & (pos[:, 0] < w + 20)
            & (pos[:, 1] >= -20) & (pos[:, 1] < h + 20)
            & (alpha > 4)
        )
        idxs = np.nonzero(visible)[0]
        if stride > 1:
            idxs = idxs[::stride]

        draw_circle = pygame.draw.circle
        for i in idxs:
            x = int(pos[i, 0])
            y = int(pos[i, 1])
            a = int(alpha[i])
            r = size[i]
            c = (int(color[i, 0]), int(color[i, 1]), int(color[i, 2]))
            if glow and a > 90:
                draw_circle(layer, (c[0], c[1], c[2], a // 4), (x, y), int(r * 2.3) + 2)
            draw_circle(layer, (c[0], c[1], c[2], a), (x, y), max(1, int(round(r))))

        surface.blit(layer, (0, 0))
