import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Assets
bird_img = pygame.image.load("assets/bird.png").convert_alpha()
bg_img = pygame.image.load("assets/bg.png").convert()

flap = pygame.mixer.Sound("assets/flap.wav")
hit = pygame.mixer.Sound("assets/hit.wav")
point = pygame.mixer.Sound("assets/point.wav")
die = pygame.mixer.Sound("assets/die.wav")

bird_img = pygame.transform.scale(bird_img, (34, 24))
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

# Bird
bird_x = 80
bird_y = 300
bird_vel = 0
gravity = 0.4
jump = -6

# Pipes 
pipe_width = 60
pipe_gap = 150
pipe_speed = 2
pipes = []

GREEN = (0, 200, 0)

def create_pipe():
    return [WIDTH, random.randint(200, 400)]

pipes.append(create_pipe())

score = 0
game_over = False
started = False

def reset():
    global bird_y, bird_vel, pipes, score, game_over, started
    bird_y = 300
    bird_vel = 0
    pipes = [create_pipe()]
    score = 0
    game_over = False
    started = False

while True:
    clock.tick(60)
    screen.blit(bg_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset()
                else:
                    bird_vel = jump
                    flap.play()
                    started = True

    if started and not game_over:
        bird_vel += gravity
        bird_y += bird_vel

        for pipe in pipes:
            pipe[0] -= pipe_speed

        if pipes[-1][0] < 200:
            pipes.append(create_pipe())

        if pipes[0][0] < -pipe_width:
            pipes.pop(0)
            score += 1
            point.play()

    bird_rect = pygame.Rect(bird_x, bird_y, 34, 24)
    screen.blit(bird_img, (bird_x, bird_y))

    for pipe in pipes:
        top_height = pipe[1] - pipe_gap // 2
        bottom_y = pipe[1] + pipe_gap // 2

        top_rect = pygame.Rect(pipe[0], 0, pipe_width, top_height)
        bottom_rect = pygame.Rect(pipe[0], bottom_y, pipe_width, HEIGHT)

        pygame.draw.rect(screen, GREEN, top_rect)
        pygame.draw.rect(screen, GREEN, bottom_rect)

        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            hit.play()
            die.play()
            game_over = True

    if bird_y < 0 or bird_y > HEIGHT:
        die.play()
        game_over = True

    score_txt = font.render(f"Score : {score}", True, (255,255,255))
    screen.blit(score_txt, (10,10))

    if not started:
        t = font.render("PRESS SPACE", True, (255,255,255))
        screen.blit(t, (120,250))

    if game_over:
        g = font.render("GAME OVER - SPACE", True, (255,0,0))
        screen.blit(g, (80,300))

    pygame.display.flip()
