# Simple program of solar system simulation
# There are 4 prepared configurations of the program: out Solar System, system of two stars, system, where the force
# depends on a cube of distance, and the one where the force depends on a distance linearlynt


import math
import time
from typing import Tuple, List

import pygame
from pygame.surface import Surface

pygame.init()

WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planets")
FPS = 100000
AU = 149.6e6 * 1000
G = 6.67428e-11
SCALE = 250 / AU
TIMESTEP = 60 * 60 * 24
ORBIT_LIFETIME = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREY = (80, 80, 80)
ORANGE = (255, 140, 0)
LIGHT_ORANGE = (200, 100, 0)
SATURN = (204, 204, 0)
URANUS = (204, 76, 153)
NEPTUNE = (153, 255, 255)

TIME_FONT = pygame.font.SysFont("comicsans", 50)


class OrbitDot:
    def __init__(self, x, y, color):
        self.x, self.y, self.color, self.creation_time = x, y, color, time.time()

    def draw(self, win):
        x = self.x * SCALE + WIDTH / 2
        y = self.y * SCALE + HEIGHT / 2
        pygame.draw.rect(win, self.color, (x, y, 1, 1))


class Planet:
    def __init__(self, x: int, y: int, radius: int, mass: float, x_vel: float, y_vel: float,
                 color: Tuple[int, int, int]):
        self.x, self.y, self.radius, self.mass, self.color, self.x_vel, self.y_vel = \
            x, y, radius, mass, color, x_vel, y_vel

    def draw(self, win):
        x = self.x * SCALE + WIDTH / 2
        y = self.y * SCALE + HEIGHT / 2
        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def attraction(self, other) -> Tuple[float, float]:
        delta_x, delta_y = other.x - self.x, other.y - self.y
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        force = G * self.mass * other.mass / distance / distance
        theta = math.atan2(delta_y, delta_x)
        force_x = force * math.cos(theta)
        force_y = force * math.sin(theta)
        return force_x, force_y

    def attraction_linear(self, other) -> Tuple[float, float]:
        delta_x, delta_y = other.x - self.x, other.y - self.y
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        force = G * self.mass * other.mass / distance
        theta = math.atan2(delta_y, delta_x)
        force_x = force * math.cos(theta)
        force_y = force * math.sin(theta)
        return force_x, force_y

    def attraction_cube(self, other) -> Tuple[float, float]:
        delta_x, delta_y = other.x - self.x, other.y - self.y
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        force = G * self.mass * other.mass / distance / distance / distance
        theta = math.atan2(delta_y, delta_x)
        force_x = force * math.cos(theta)
        force_y = force * math.sin(theta)
        return force_x, force_y

    def update_pos(self, planets) -> OrbitDot:
        force_x = 0
        force_y = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            force_x += fx
            force_y += fy
        self.x_vel += force_x / self.mass * TIMESTEP
        self.y_vel += force_y / self.mass * TIMESTEP

        self.x += self.x_vel * TIMESTEP
        self.y += self.y_vel * TIMESTEP
        return OrbitDot(self.x, self.y, self.color)

    def update_pos_linear(self, planets) -> OrbitDot:
        force_x = 0
        force_y = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction_linear(planet)
            force_x += fx
            force_y += fy
        self.x_vel += force_x / self.mass * TIMESTEP
        self.y_vel += force_y / self.mass * TIMESTEP

        self.x += self.x_vel * TIMESTEP
        self.y += self.y_vel * TIMESTEP
        return OrbitDot(self.x, self.y, self.color)

    def update_pos_cube(self, planets) -> OrbitDot:
        force_x = 0
        force_y = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction_cube(planet)
            force_x += fx
            force_y += fy
        self.x_vel += force_x / self.mass * TIMESTEP
        self.y_vel += force_y / self.mass * TIMESTEP

        self.x += self.x_vel * TIMESTEP
        self.y += self.y_vel * TIMESTEP
        return OrbitDot(self.x, self.y, self.color)


def draw(win: Surface, planets: List[Planet], dots: List[OrbitDot], days, years):
    win.fill(BLACK)
    left_score_text = TIME_FONT.render(f"Years: {years}", 1, WHITE)
    right_score_text = TIME_FONT.render(f"Days: {days}", 1, WHITE)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH // 4 * 3 - right_score_text.get_width() // 2, 20))
    for planet in planets:
        planet.draw(win)
    for dot in dots:
        dot.draw(win)
    pygame.display.update()


def solar_system():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 3, 1.98892 * 10 ** 30, 0, 0, YELLOW)
    mercury = Planet(0.387 * AU, 0, 3, 3.30 * 10 ** 23, 0, -47.4 * 1000, GREY)
    venus = Planet(0.723 * AU, 0, 3, 4.8685 * 10 ** 24, 0, -35.02 * 1000, ORANGE)
    earth = Planet(-1 * AU, 0, 3, 5.9742 * 10 ** 24, 0, 29.783 * 1000, BLUE)
    mars = Planet(-1.524 * AU, 0, 3, 6.39 * 10 ** 23, 0, 24.077 * 1000, RED)
    jupiter = Planet(5.20 * AU, 0, 3, 1.899 * 10 ** 27, 0, -13.1 * 1000, ORANGE)
    saturn = Planet(-9.58 * AU, 0, 3, 5.685 * 10 ** 26, 0, 9.7 * 1000, SATURN)
    uranus = Planet(19.14 * AU, 0, 3, 8.682 * 10 ** 25, 0, 6.8 * 1000, URANUS)
    neptune = Planet(-30.20 * AU, 0, 3, 1.024 * 10 ** 26, 0, -5.4 * 1000, NEPTUNE)

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
    dots = []

    days = 0
    years = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            dots.append(planet.update_pos(planets))
        new_dots = []
        for dot in dots:
            if time.time() - dot.creation_time < ORBIT_LIFETIME:
                new_dots.append(dot)
        dots = new_dots
        draw(WIN, planets, dots, days, years)
        days += 1
        years += days // 365
        days %= 365
    pygame.quit()


def system_two_sun():
    run = True
    clock = pygame.time.Clock()

    # usual binary star
    # sun1 = Planet(-0.3 * AU, 0, 5, 1.98892 * 10 ** 29, 0, 11 * 1000, YELLOW)
    # sun2 = Planet(0.3 * AU, 0, 5, 1.98892 * 10 ** 29, 0, -11 * 1000, LIGHT_ORANGE)
    sun1 = Planet(-0.5 * AU, 0, 5, 1 * 10 ** 29, 0, 4.5 * 1000, YELLOW)
    sun2 = Planet(0.5 * AU, 0, 5, 1 * 10 ** 29, 0, -4.5 * 1000, LIGHT_ORANGE)

    planets = [sun1, sun2]
    dots = []

    days = 0
    years = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            dots.append(planet.update_pos(planets))
        new_dots = []
        for dot in dots:
            if time.time() - dot.creation_time < ORBIT_LIFETIME:
                new_dots.append(dot)
        dots = new_dots
        draw(WIN, planets, dots, days, years)
        days += 1
        years += days // 365
        days %= 365
    pygame.quit()


def linear_force():
    run = True
    clock = pygame.time.Clock()

    # binary stars for force~(1/distance), not square of distance
    sun1 = Planet(-0.5 * AU, 0, 5, 1.98892 * 10 ** 17, 0, 5 * 1000, YELLOW)
    sun2 = Planet(0.5 * AU, 0, 5, 1.98892 * 10 ** 18, 0, -0.5 * 1000, LIGHT_ORANGE)
    sun1 = Planet(-0.5 * AU, 0, 5, 1.98892 * 10 ** 12, 0, 5 * 1000, YELLOW)
    sun2 = Planet(0.5 * AU, 0, 5, 1.98892 * 10 ** 19, 0, 0 * 1000, LIGHT_ORANGE)

    planets = [sun1, sun2]
    dots = []

    days = 0
    years = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            dots.append(planet.update_pos_linear(planets))
        new_dots = []
        for dot in dots:
            if time.time() - dot.creation_time < ORBIT_LIFETIME:
                new_dots.append(dot)
        dots = new_dots
        draw(WIN, planets, dots, days, years)
        days += 1
        years += days // 365
        days %= 365
    pygame.quit()


def cube_force():
    run = True
    clock = pygame.time.Clock()

    sun1 = Planet(-0.94 * AU, 0, 5, 1.98892 * 10 ** 12, 0, 5 * 1000, YELLOW)
    sun2 = Planet(0 * AU, 0, 5, 8 * 10 ** 39, 0, 0 * 1000, LIGHT_ORANGE)
    # sun1 = Planet(-0.91 * AU, 0, 5, 1.98892 * 10 ** 12, 0, 5 * 1000, YELLOW)
    # sun2 = Planet(0 * AU, 0, 5, 8 * 10 ** 39, 0, 0 * 1000, LIGHT_ORANGE)

    planets = [sun1, sun2]
    dots = []

    days = 0
    years = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            dots.append(planet.update_pos_cube(planets))
        new_dots = []
        for dot in dots:
            if time.time() - dot.creation_time < ORBIT_LIFETIME:
                new_dots.append(dot)
        dots = new_dots
        draw(WIN, planets, dots, days, years)
        days += 1
        years += days // 365
        days %= 365
    pygame.quit()


if __name__ == "__main__":
    # solar_system()
    system_two_sun()
    # linear_force()
    # cube_force()
