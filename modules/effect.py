import pygame
import random
import math


# ============================================================
# VISUAL EFFECTS
# ============================================================

class ParticleEffect:
    """Particle effect when a waste is caught."""

    def __init__(self, x, y, color=(100, 255, 100)):
        self.particles = []
        for _ in range(12):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            self.particles.append({
                "x": x, "y": y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": random.randint(15, 30),
                "size": random.randint(3, 7),
                "color": (
                    min(255, color[0] + random.randint(-30, 30)),
                    min(255, color[1] + random.randint(-30, 30)),
                    min(255, color[2] + random.randint(-30, 30)),
                )
            })

    def update(self):
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.15  # Gravity on particles
            p["life"] -= 1
            p["size"] = max(1, p["size"] - 0.1)
        self.particles = [p for p in self.particles if p["life"] > 0]

    def draw(self, screen):
        for p in self.particles:
            alpha = min(255, p["life"] * 10)
            size = int(p["size"])
            pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), size)

    def is_done(self):
        return len(self.particles) == 0


class FloatingText:
    """Floating text (+10, +20, Combo!) that rises and disappears."""

    def __init__(self, x, y, text, color=(255, 255, 100)):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.life = 40
        self.font = pygame.font.Font(None, 28)

    def update(self):
        self.y -= 1.5
        self.life -= 1

    def draw(self, screen):
        if self.life > 0:
            text_surface = self.font.render(self.text, True, self.color)
            screen.blit(text_surface, (self.x, self.y))

    def is_done(self):
        return self.life <= 0
