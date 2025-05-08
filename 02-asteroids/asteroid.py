import pygame
import random

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, width=2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            random_angle = random.uniform(20, 50)
            new_velo1 = self.velocity.rotate(random_angle)
            new_velo2 = self.velocity.rotate(-random_angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS

            new_aste1 = Asteroid(self.position.x, self.position.y, new_radius)
            new_aste1.velocity = new_velo1 * 1.2
            new_aste2 = Asteroid(self.position.x, self.position.y, new_radius)
            new_aste2.velocity = new_velo2 * 1.2

