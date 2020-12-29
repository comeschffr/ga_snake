import sys, json, glob
import pygame


def makerect(position):
    x, y = position
    return pygame.Rect(x, y, width, height)


print('Which file?')
for i, file in enumerate(glob.glob("*.txt")):
    print(f'{i}: {file}')
f_index = int(input('>> '))

with open(glob.glob("*.txt")[f_index]) as json_file:
    path = json.load(json_file)

tile_nb = 10
screen_width, screen_height = 500, 500
width, height = screen_width/tile_nb, screen_height/tile_nb
BLACK = (0, 0, 0)
RED = (181, 30, 0)
WHITE = (255, 255, 255)
GREEN = (22, 255, 18)

clock = pygame.time.Clock()
FPS = 5

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.font.init()
font = pygame.font.Font(None, 30)

frame_max = len(path)

print(f'100% Loaded, running simulation at {FPS} fps')


for frame, state in enumerate(path):
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

    snake = state['snake']
    apple = state['apple']
    score = state['score']

    text_fps = font.render(f'{round(clock.get_fps())}fps', 1, GREEN)
    text_score = font.render(f'score={score}', 1, GREEN)
    text_frame = font.render(f'{frame}/{frame_max}', 1, GREEN)

    screen.fill(BLACK)
    
    pygame.draw.rect(screen, GREEN, makerect(apple))

    for i, pos in enumerate(snake):
        cell = makerect(pos)
        if i == len(snake)-1:
            pygame.draw.rect(screen, RED, cell)
        else:
            pygame.draw.rect(screen, WHITE, cell)

    screen.blit(text_fps, (0, 0))
    screen.blit(text_score, (0, 20))
    screen.blit(text_frame, (0, 40))
    
    pygame.display.update()

