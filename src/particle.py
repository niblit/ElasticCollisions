from random import randint
import numpy as np


def get_distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5


def calculate_collision_response(v1, v2, c1, c2):
    v1 = np.array(v1)
    v2 = np.array(v2)

    c1 = np.array(c1)
    c2 = np.array(c2)

    v1f = v1 - (
        (np.inner(v1-v2, c1-c2)) / (np.linalg.norm(c1 - c2))**2
    ) * (c1 - c2)

    v2f = v2 - (
            (np.inner(v2 - v1, c2 - c1)) / (np.linalg.norm(c2 - c1)) ** 2
    ) * (c2 - c1)

    return v1f, v2f


class Particle:
    def __init__(self, particle_id, radius, screen_size):
        self.particle_id = particle_id
        self.radius = radius
        self.screen_size = screen_size
        self.position = [randint(self.radius * 2, screen_size - self.radius * 2), randint(10, screen_size - self.radius * 2)]
        self.velocity = [randint(-20, 20), randint(-20, 20)]
        self.acceleration = [0, 0]

        while True:
            self.color = (
                randint(0, 255),
                randint(0, 255),
                randint(0, 255)
            )
            if abs(sum(self.color)) > 100:
                break

    def update(self, delta_time, particles=None):
        self.check_edges()

        if particles is not None:
            interactions = set()
            for other in particles:
                string_id = f"{self.particle_id}:{other.particle_id}"
                if self.particle_id == other.particle_id or string_id in interactions:
                    continue
                else:
                    interactions.add(string_id)
                if get_distance(*self.position, *other.position) <= (self.radius + other.radius):
                    v1, v2 = calculate_collision_response(self.velocity, other.velocity, self.position, other.position)
                    self.velocity = list(v1)
                    other.velocity = list(v2)

        self.position[0] += delta_time * self.velocity[0]
        self.position[1] += delta_time * self.velocity[1]

        self.velocity[0] += delta_time * self.acceleration[0]
        self.velocity[1] += delta_time * self.acceleration[1]

    def check_edges(self):
        if self.position[0] <= self.radius:
            self.position[0] = self.radius
            self.velocity[0] *= -1

        if self.position[1] <= self.radius:
            self.position[1] = self.radius
            self.velocity[1] *= -1

        if self.position[0] >= self.screen_size - self.radius:
            self.position[0] = self.screen_size - self.radius
            self.velocity[0] *= -1

        if self.position[1] >= self.screen_size - self.radius:
            self.position[1] = self.screen_size - self.radius
            self.velocity[1] *= -1
