import pygame
import random
import math


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1.5, 4.5)

        self.velocity_x = math.cos(angle) * speed
        self.velocity_y = math.sin(angle) * speed

        self.life = random.randint(15, 30)
        self.size = random.randint(2, 5)

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        self.velocity_y += 0.08
        self.life -= 1

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(
                screen,
                (255, 190, 70),
                (int(self.x), int(self.y)),
                self.size
            )


class Effects:
    def __init__(self):
        self.particles = []

        self.muzzle_timer = 0
        self.muzzle_x = 0
        self.muzzle_y = 0

    def create_hit_effect(self, x, y):
        for _ in range(12):
            self.particles.append(
                Particle(x, y)
            )

    def create_muzzle_flash(self, x, y):
        self.muzzle_x = x
        self.muzzle_y = y
        self.muzzle_timer = 5

    def update(self):
        for particle in self.particles:
            particle.update()

        self.particles = [
            particle
            for particle in self.particles
            if particle.life > 0
        ]

        if self.muzzle_timer > 0:
            self.muzzle_timer -= 1

    def draw(self, screen):
        # Hit particles
        for particle in self.particles:
            particle.draw(screen)

        # Muzzle flash
        if self.muzzle_timer > 0:
            pygame.draw.circle(
                screen,
                (255, 220, 100),
                (int(self.muzzle_x), int(self.muzzle_y)),
                10
            )

            pygame.draw.circle(
                screen,
                (255, 245, 180),
                (int(self.muzzle_x), int(self.muzzle_y)),
                5
            )