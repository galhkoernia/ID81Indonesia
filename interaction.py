"""
Mengelola interaksi mouse terhadap particle 
dorongan menjauh saat hover (repulsion) dan ledakan particle saat klik (burst) 
hanya aktif ketika scene mengizinkan.
"""

import pygame

from config import MOUSE_REPEL_RADIUS, MOUSE_REPEL_STRENGTH, CLICK_BURST_RADIUS


class InteractionManager:
    def __init__(self):
        self.enabled = False
        self.repel_radius = MOUSE_REPEL_RADIUS
        self.repel_strength = MOUSE_REPEL_STRENGTH
        self.burst_radius = CLICK_BURST_RADIUS

    def set_enabled(self, enabled):
        self.enabled = enabled

    def update(self, particle_system, dt):
        if not self.enabled:
            return
        mx, my = pygame.mouse.get_pos()
        particle_system.repel_from_point(mx, my, self.repel_radius, self.repel_strength, dt)

    def handle_click(self, particle_system, pos):
        if not self.enabled:
            return
        particle_system.burst(pos[0], pos[1], radius=self.burst_radius)
