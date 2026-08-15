# Entry point aplikasi. Inisialisasi Pygame, membuat window fullscreen/windowed, 
# menjalankan game loop utama (event handling, update, render), mengatur delta-time, 
# adaptive quality (FPS-based), serta kontrol keyboard (SPACE, R, F, ESC) dan klik mouse.

import sys

try:
    import pygame
except ImportError:
    sys.stderr.write(
        "\n[ERROR] Modul 'pygame' belum terinstall.\n"
        "Jalankan: pip install -r requirements.txt\n\n"
    )
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    sys.stderr.write(
        "\n[ERROR] Modul 'numpy' belum terinstall.\n"
        "Jalankan: pip install -r requirements.txt\n\n"
    )
    sys.exit(1)

import config
from particles import ParticleSystem
from interaction import InteractionManager
from scenes import SceneManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("81 Tahun Merdeka")
        pygame.mouse.set_visible(True)

        self.fullscreen = not config.DEV_MODE
        self.screen = self._create_display(self.fullscreen)
        self.screen_w, self.screen_h = self.screen.get_size()

        self.clock = pygame.time.Clock()
        self.running = True
        self.time_elapsed = 0.0
        self.overlay_alpha = 0.0

        # quality/adaptive performance
        self.quality = "HIGH"
        self._fps_samples = []

        self.particle_layer = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)

        self.particles = ParticleSystem(config.PARTICLE_COUNT)
        self.particles.init_random(self.screen_w, self.screen_h)

        self.interaction = InteractionManager()
        self.scene_manager = SceneManager(self)

    # Create Display
    def _create_display(self, fullscreen):
        if fullscreen:
            info = pygame.display.Info()
            size = (info.current_w, info.current_h)
            try:
                screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
            except pygame.error:
                # fallback jika mode fullscreen native gagal di environment tertentu
                screen = pygame.display.set_mode(size)
        else:
            screen = pygame.display.set_mode(config.WINDOWED_SIZE, pygame.RESIZABLE)
        return screen

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.screen = self._create_display(self.fullscreen)
        self.screen_w, self.screen_h = self.screen.get_size()
        self.particle_layer = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        self.particles.set_screen_size(self.screen_w, self.screen_h)
        # ukuran layar berubah -> target teks/bendera scene aktif harus dihitung ulang
        self.scene_manager.rebuild_current()

    # Handle Events
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.scene_manager.skip()
                elif event.key == pygame.K_r:
                    self.scene_manager.restart()
                elif event.key == pygame.K_f:
                    self.toggle_fullscreen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.interaction.handle_click(self.particles, event.pos)

    # Update Quality
    def update_quality(self):
        fps = self.clock.get_fps()
        if fps <= 0:
            return
        self._fps_samples.append(fps)
        if len(self._fps_samples) > 30:
            self._fps_samples.pop(0)
        avg_fps = sum(self._fps_samples) / len(self._fps_samples)

        if avg_fps >= config.FPS_HIGH_THRESHOLD:
            self.quality = "HIGH"
        elif avg_fps >= config.FPS_MEDIUM_THRESHOLD:
            self.quality = "MEDIUM"
        else:
            self.quality = "LOW"

    def draw_stride(self):
        return {"HIGH": 1, "MEDIUM": 1, "LOW": 2}[self.quality]

    def glow_enabled(self):
        return self.quality == "HIGH"

    def update(self, dt):
        self.time_elapsed += dt
        self.scene_manager.update(dt)

        current_scene = self.scene_manager.current
        self.particles.update(
            dt,
            self.time_elapsed,
            wave_enabled=current_scene.wave_enabled,
            wave_amplitude=config.FLAG_WAVE_AMPLITUDE,
            wave_frequency=config.FLAG_WAVE_FREQUENCY,
        )
        self.interaction.update(self.particles, dt)
        self.update_quality()

    def render(self):
        self.screen.fill(config.BACKGROUND_COLOR)
        self.particles.draw(
            self.screen, self.particle_layer,
            glow=self.glow_enabled(), stride=self.draw_stride(),
        )

        if self.overlay_alpha > 0:
            overlay = pygame.Surface((self.screen_w, self.screen_h))
            overlay.set_alpha(int(self.overlay_alpha))
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

        pygame.display.flip()

    def run(self):
        while self.running:
            dt_ms = self.clock.tick(config.TARGET_FPS)
            dt = min(dt_ms / 1000.0, 0.05)  # clamp supaya lag spike tidak melompatkan animasi

            self.handle_events()
            self.update(dt)
            self.render()

        pygame.quit()


def main():
    try:
        game = Game()
    except pygame.error as e:
        sys.stderr.write(f"\n[ERROR] Gagal membuat display: {e}\n")
        sys.exit(1)
    game.run()


if __name__ == "__main__":
    main()
