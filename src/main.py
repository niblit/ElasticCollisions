import pygame
from particle import Particle, get_distance

FPS = 60
SCREEN_SIZE = 600
BACKGROUND = (0, 0, 0)
QUANTITY = 10
RADIUS = 50


def main():
    particles = list()
    for particle_id in range(QUANTITY):
        for i in range(1_000):
            par = Particle(particle_id, RADIUS, SCREEN_SIZE)
            bad_spawn = False
            for position in particles:
                if get_distance(*par.position, *position.position) <= (RADIUS * 2.5):
                    bad_spawn = True
            if not bad_spawn:
                particles.append(par)
                break
            else:
                print(f"Bad spawn, retry {i} of 1,000")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Collisions")
    clock = pygame.time.Clock()

    running = True
    while running:
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(BACKGROUND)

        # RENDER YOUR GAME HERE
        for particle in particles:
            particle.update(clock.get_time() / 100, particles)
            pygame.draw.circle(screen, particle.color, particle.position, particle.radius)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(FPS)  # limits FPS

    pygame.quit()


if __name__ == "__main__":
    main()
