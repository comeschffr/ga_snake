import sys, random, json
import pygame

pygame.init()

def gameover(reason):
    print(f'Game over, reason: {reason}')
    with open('ind0.txt', 'w') as outfile:
        json.dump(path, outfile)
    sys.exit()

def newapple(snake):
    print('Generating new apple...')
    isValid = False
    while not isValid:
        x = random.randrange(0, tile_nb) * width
        y = random.randrange(0, tile_nb) * height
        print(f'Testing with x={x}, y={y}')
        for cell in snake:
            if cell.x == x and cell.y == y:
                print('Trying again...')
                break
        else:
            isValid = True
    print('Apple generated successfully!')
    return x, y

def overbody(snake):
    head = snake[-1]
    isOverlap = False
    for cell in snake[:-1]:
        if head.x == cell.x and head.y == cell.y:
            isOverlap = True
            break
    return isOverlap

def processframestate(snake, apple, score):
    frame_state = {
        'snake': [[cell.x, cell.y] for cell in snake],
        'apple': [apple.x, apple.y],
        'score': score
    }
    return frame_state


tile_nb = 10
screen_width, screen_height = 500, 500
width, height = screen_width/tile_nb, screen_height/tile_nb
BLACK = (0, 0, 0)
RED = (181, 30, 0)
WHITE = (255, 255, 255)
GREEN = (22, 255, 18)

clock = pygame.time.Clock()
FPS = 8

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.font.init()
font = pygame.font.Font(None, 30)

snake = [pygame.Rect(0, 0, width, height)]
speed = [width, 0]

apple_x, apple_y = newapple(snake)
apple = pygame.Rect(apple_x, apple_y, width, height)
score = 0

path = []


while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed = [-width, 0] 
            if event.key == pygame.K_RIGHT:
                speed = [width, 0]
            if event.key == pygame.K_UP:
                speed = [0, -height]
            if event.key == pygame.K_DOWN:
                speed = [0, height]


    snake.append(snake[-1].move(speed))

    if snake[-1].x == apple.x and snake[-1].y == apple.y:
        score += 1
        if score == screen_width * screen_height:
            gameover('reached_max_score')
        apple_x, apple_y = newapple(snake)
        apple = pygame.Rect(apple_x, apple_y, width, height)
    else:
        snake.pop(0)

    frame_state = processframestate(snake, apple, score)
    path.append(frame_state)

    if (snake[-1].top < 0 or snake[-1].top >= screen_height) \
        or (snake[-1].left < 0 or snake[-1].left >= screen_width):
        gameover('out_of_limits')
    if overbody(snake):
        gameover('ran_over_body')

    text_fps = font.render(f'{round(clock.get_fps())}fps', 1, GREEN)
    text_score = font.render(f'score={score}', 1, GREEN)

    screen.fill(BLACK)
    
    pygame.draw.rect(screen, GREEN, apple)

    for i, cell in enumerate(snake):
        if i == len(snake)-1:
            pygame.draw.rect(screen, RED, cell)
        else:
            pygame.draw.rect(screen, WHITE, cell)

    screen.blit(text_fps, (0, 0))
    screen.blit(text_score, (0, 30))
    
    pygame.display.update()