"""
Scene Manager beserta seluruh scene individual (INTRO sampai ENDING). 
Setiap scene mendefinisikan enter/update/exit dan menentukan target bentuk particle berikutnya, sehingga alur cerita animasi (bendera → teks → angka 81 → interaktif → MERDEKA! → ending) 
berjalan berurutan dan transisinya organik.
"""

import math

import numpy as np

from config import SCENE_DURATIONS, FLAG_WAVE_AMPLITUDE, FLAG_WAVE_FREQUENCY, WHITE_COLOR
from flag_particles import generate_flag_targets
from text_particles import generate_text_targets

SCENE_SEQUENCE = [
    "INTRO",
    "FLAG_FORMING",
    "FLAG_WAVING",
    "FLAG_DISSOLVE",
    "TEXT_DIRGAHAYU",
    "TEXT_REPUBLIC",
    "NUMBER_81",
    "INTERACTIVE",
    "FINALE",
    "ENDING",
]


class Scene:
    """Base class untuk semua scene."""

    wave_enabled = False
    interaction_enabled = False

    def __init__(self, game):
        self.game = game
        self.elapsed = 0.0
        self.duration = 3.0

    def enter(self):
        self.elapsed = 0.0

    def update(self, dt):
        self.elapsed += dt

    def exit(self):
        pass

    def is_finished(self):
        return self.elapsed >= self.duration

    # helper dipakai banyak scene turunan
    @property
    def ps(self):
        return self.game.particles

    @property
    def screen_w(self):
        return self.game.screen_w

    @property
    def screen_h(self):
        return self.game.screen_h


class IntroScene(Scene):
    """Layar hitam, satu titik muncul, lalu semakin banyak titik muncul perlahan."""

    def enter(self):
        super().enter()
        self.duration = SCENE_DURATIONS["intro"]
        ps = self.ps
        cx, cy = self.screen_w / 2.0, self.screen_h / 2.0
        spread = min(self.screen_w, self.screen_h) * 0.42

        angles = np.random.uniform(0, np.pi * 2, ps.count)
        radii = np.random.uniform(0, spread, ps.count)
        xs = cx + np.cos(angles) * radii
        ys = cy + np.sin(angles) * radii
        coords = np.stack([xs, ys], axis=1)

        ps.pos[:] = coords
        ps.origin[:] = coords
        ps.target[:] = coords
        ps.move_t[:] = 1.0
        ps.alpha[:] = 0.0
        ps.target_alpha[:] = 0.0
        ps.color[:] = WHITE_COLOR
        ps.target_color[:] = WHITE_COLOR

        self._revealed = 0
        self._reveal_order = np.random.permutation(ps.count)

    def update(self, dt):
        super().update(dt)
        ps = self.ps
        # titik pertama muncul di tengah lebih dulu, lalu makin banyak menyusul
        frac = min(self.elapsed / max(self.duration * 0.85, 0.01), 1.0)
        target_revealed = int(frac * ps.count)
        if target_revealed > self._revealed:
            idxs = self._reveal_order[self._revealed:target_revealed]
            ps.target_alpha[idxs] = 255.0
            self._revealed = target_revealed


class FlagFormingScene(Scene):
    """Particle merah & putih berkumpul membentuk Bendera Merah Putih."""

    def enter(self):
        super().enter()
        self.duration = SCENE_DURATIONS["flag_forming"]
        coords, colors = generate_flag_targets(self.screen_w, self.screen_h, self.ps.count)
        self.ps.assign_targets(coords, colors=colors, duration=self.duration * 0.75, stagger=0.8)


class FlagWavingScene(Scene):
    """Bendera yang sudah terbentuk diberi efek berkibar halus."""

    wave_enabled = True

    def enter(self):
        super().enter()
        self.duration = SCENE_DURATIONS["flag_waving"]
        # tidak mengganti target - bendera tetap di posisi, hanya wave_enabled
        # di ParticleSystem.update() yang menambahkan gelombang horizontal.


class FlagDissolveScene(Scene):
    """Bendera pecah menjadi partikel yang menyebar, siap membentuk teks berikutnya."""

    def enter(self):
        super().enter()
        self.duration = SCENE_DURATIONS["flag_dissolve"]
        self.ps.scatter(strength=self.screen_w * 0.22, duration=self.duration * 0.9)


class TextDirgahayuScene(Scene):
    """Particle yang menyebar berkumpul kembali membentuk tulisan DIRGAHAYU."""

    def enter(self):
        super().enter()
        self.duration = SCENE_DURATIONS["text_dirgahayu"]
        size = int(self.screen_h * 0.16)
        coords = generate_text_targets(
            "DIRGAHAYU", size, self.screen_w, self.screen_h,
            sample_step=3, max_particles=self.ps.count,
        )
        self.ps.assign_targets(coords, colors=np.tile(WHITE_COLOR, (len(coords), 1)),
                                duration=self.duration * 0.7, stagger=0.9)


class TextRepublicScene(Scene):
    """Transisi ke REPUBLIK INDONESIA + subtext 17 AGUSTUS 1945, keduanya berbasis particle."""

    def enter(self):
        super().enter()
        self.duration = SCENE_DURATIONS["text_republic"]
        ps = self.ps

        main_size = int(self.screen_h * 0.09)
        sub_size = int(self.screen_h * 0.035)

        main_count = int(ps.count * 0.72)
        sub_count = ps.count - main_count

        main_coords = generate_text_targets(
            "REPUBLIK INDONESIA", main_size, self.screen_w, self.screen_h,
            sample_step=3, max_particles=main_count, y_offset=-int(self.screen_h * 0.05),
        )
        sub_coords = generate_text_targets(
            "17 AGUSTUS 1945", sub_size, self.screen_w, self.screen_h,
            sample_step=2, max_particles=sub_count, y_offset=int(self.screen_h * 0.07),
        )

        coords = np.concatenate([main_coords, sub_coords], axis=0)
        colors = np.tile(WHITE_COLOR, (len(coords), 1))
        ps.assign_targets(coords, colors=colors, duration=self.duration * 0.65, stagger=0.9)


class NumberScene(Scene):
    """Angka 81 sebagai hero moment, dengan subtext tahun kemerdekaan."""

    def enter(self):
        super().enter()
        self.duration = SCENE_DURATIONS["number_81"]
        ps = self.ps

        number_size = int(self.screen_h * 0.42)
        label_size = int(self.screen_h * 0.045)
        year_size = int(self.screen_h * 0.03)

        number_count = int(ps.count * 0.62)
        label_count = int(ps.count * 0.22)
        year_count = ps.count - number_count - label_count

        number_coords = generate_text_targets(
            "81", number_size, self.screen_w, self.screen_h,
            sample_step=3, max_particles=number_count, y_offset=-int(self.screen_h * 0.06),
        )
        label_coords = generate_text_targets(
            "TAHUN KEMERDEKAAN", label_size, self.screen_w, self.screen_h,
            sample_step=2, max_particles=label_count, y_offset=int(self.screen_h * 0.22),
        )
        year_coords = generate_text_targets(
            "1945 - 2026", year_size, self.screen_w, self.screen_h,
            sample_step=2, max_particles=year_count, y_offset=int(self.screen_h * 0.28),
        )

        coords = np.concatenate([number_coords, label_coords, year_coords], axis=0)
        colors = np.tile(WHITE_COLOR, (len(coords), 1))
        ps.assign_targets(coords, colors=colors, duration=self.duration * 0.6, stagger=1.0)


class InteractiveScene(Scene):
    """Angka 81 tetap terbentuk, tapi sekarang particle merespons mouse."""

    interaction_enabled = True

    def enter(self):
        super().enter()
        self.duration = SCENE_DURATIONS["interactive"]
        self.game.interaction.set_enabled(True)
        # bentuk tetap dipertahankan dari NumberScene sebelumnya (tidak reassign target)

    def exit(self):
        self.game.interaction.set_enabled(False)


class FinaleScene(Scene):
    """Klimaks visual: MERDEKA! sebagai teks utama."""

    def enter(self):
        super().enter()
        self.duration = SCENE_DURATIONS["finale"]
        ps = self.ps

        main_size = int(self.screen_h * 0.20)
        sub_size = int(self.screen_h * 0.032)

        main_count = int(ps.count * 0.68)
        sub_count = ps.count - main_count

        main_coords = generate_text_targets(
            "MERDEKA!", main_size, self.screen_w, self.screen_h,
            sample_step=3, max_particles=main_count, y_offset=-int(self.screen_h * 0.06),
        )
        sub_coords = generate_text_targets(
            "81 TAHUN INDONESIA MERDEKA", sub_size, self.screen_w, self.screen_h,
            sample_step=2, max_particles=sub_count, y_offset=int(self.screen_h * 0.11),
        )

        coords = np.concatenate([main_coords, sub_coords], axis=0)
        colors = np.tile(WHITE_COLOR, (len(coords), 1))
        ps.assign_targets(coords, colors=colors, duration=self.duration * 0.55, stagger=1.0)


class EndingScene(Scene):
    """Semua particle berkumpul menjadi satu titik, tahan sebentar, lalu fade to black.
    Scene ini tidak pernah 'selesai' secara otomatis - aplikasi tetap terbuka
    di layar hitam sampai user menekan R (restart) atau ESC (keluar)."""

    def enter(self):
        super().enter()
        self.duration = math.inf
        ps = self.ps
        cx, cy = self.screen_w / 2.0, self.screen_h / 2.0
        center = np.array([[cx, cy]], dtype=np.float64)
        ps.assign_targets(center, colors=np.array([WHITE_COLOR], dtype=np.float64),
                           duration=1.3, stagger=0.5)
        self._hold_time = 0.0
        self.game.overlay_alpha = 0.0

    def update(self, dt):
        super().update(dt)
        if self.elapsed > 1.8:
            self._hold_time += dt
        if self._hold_time > 1.0:
            self.game.overlay_alpha = min(255.0, self.game.overlay_alpha + dt * 110.0)


class SceneManager:
    def __init__(self, game):
        self.game = game
        self.scenes = {
            "INTRO": IntroScene(game),
            "FLAG_FORMING": FlagFormingScene(game),
            "FLAG_WAVING": FlagWavingScene(game),
            "FLAG_DISSOLVE": FlagDissolveScene(game),
            "TEXT_DIRGAHAYU": TextDirgahayuScene(game),
            "TEXT_REPUBLIC": TextRepublicScene(game),
            "NUMBER_81": NumberScene(game),
            "INTERACTIVE": InteractiveScene(game),
            "FINALE": FinaleScene(game),
            "ENDING": EndingScene(game),
        }
        self.index = 0
        self.current = self.scenes[SCENE_SEQUENCE[0]]
        self.current.enter()

    @property
    def current_name(self):
        return SCENE_SEQUENCE[self.index]

    def update(self, dt):
        self.current.update(dt)
        if self.current.is_finished():
            self.next_scene()

    def next_scene(self):
        self.current.exit()
        self.index = (self.index + 1) % len(SCENE_SEQUENCE)
        self.current = self.scenes[SCENE_SEQUENCE[self.index]]
        self.game.overlay_alpha = 0.0
        self.current.enter()

    def skip(self):
        self.next_scene()

    def restart(self):
        self.current.exit()
        self.index = 0
        self.current = self.scenes[SCENE_SEQUENCE[0]]
        self.game.overlay_alpha = 0.0
        self.current.enter()

    def rebuild_current(self):
        """Dipanggil saat resolusi berubah (mis. toggle fullscreen) supaya
        target particle scene aktif dihitung ulang sesuai ukuran layar baru."""
        self.current.enter()
