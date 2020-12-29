import json, sys, random, math, logging
import training
import numpy as np


def gameover(reason, score, dframes):
    logging.debug(f'Game over, reason: {reason}')
    return score, dframes


def overbody(snake):
    head = snake[-1]
    isOverlap = False
    for cell in snake[:-1]:
        if head[0] == cell[0] and head[1] == cell[1]:
            isOverlap = True
            break
    return isOverlap


def newapple(snake, tile_nb):
    logging.debug('Generating new apple...')
    isValid = False
    while not isValid:
        x, y = random.randrange(tile_nb), random.randrange(tile_nb)
        logging.debug(f'Testing with x={x}, y={y}')
        for cell in snake:
            if cell[0] == x and cell[1] == y:
                logging.debug('Trying again...')
                break
        else:
            isValid = True
    logging.debug('Apple generated successfully!')
    return x, y

def get_dst(snake, tile_nb, direction):
    x = snake[-1][0]
    y = snake[-1][1]
    if direction == 'up':
        for y in range(y-1, -1, -1):
            if [x, y] in snake:
                return snake[-1][1] - y
        return snake[-1][1] + 1
    elif direction == 'right':
        for x in range(x+1, tile_nb):
            if [x, y] in snake:
                return x - snake[-1][0]
        return tile_nb - snake[-1][0]
    elif direction == 'bottom':
        for y in range(y+1, tile_nb):
            if [x, y] in snake:
                return y - snake[-1][1]
        return tile_nb - snake[-1][1]
    elif direction == 'left':
        for x in range(x-1, -1, -1):
            if [x, y] in snake:
                return snake[-1][0] - x
        return snake[-1][0] + 1


def simulate_game(model):
    tile_nb = 10

    snake = [(int(tile_nb/2), int(tile_nb/2))]

    speeds = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    speed = speeds[0]

    apple = newapple(snake, tile_nb)
    score = 0
    dframes = 0

    apples = []

    while True:
        dframes += 1

        sensors = {
            'head_direction': [speed==speeds[i] for i in range(4)],
            'distance_to_apple': abs(snake[-1][0]-apple[0]) + abs(snake[-1][1]-apple[1]),
            'apple_direction': [snake[-1][1]>apple[1], snake[-1][0]<apple[0], snake[-1][1]<apple[1], snake[-1][0]>apple[0]],
            'distance_to_obstacle': [
                get_dst(snake, tile_nb, 'up'),
                get_dst(snake, tile_nb, 'right'),
                get_dst(snake, tile_nb, 'bottom'),
                get_dst(snake, tile_nb, 'left'),
            ]
        }

        i = training.make_decision(sensors, model)
        speed = speeds[i.item(0)]

        new_head = (snake[-1][0] + speed[0], snake[-1][1] + speed[1])
        snake.append(new_head)

        if new_head[0] == apple[0] and new_head[1] == apple[1]:
            score += 1
            if score == tile_nb**2:
                result = gameover('reached_max_score', score, dframes)
                return result
            apple = newapple(snake, tile_nb)
            apples.append(apple)
        else:
            snake.pop(0)
        
        if (snake[-1][0] < 0 or snake[-1][0] >= tile_nb) \
            or (snake[-1][1] < 0 or snake[-1][1] >= tile_nb):
            result = gameover('out_of_limits', score, dframes)
            return result
        if overbody(snake):
            result = gameover('ran_over_body', score, dframes)
            return result
        if dframes > 2000:
            result = gameover('timeout', score, dframes)
            return result


if __name__ == '__main__':
    # random.seed(0)
    # np.random.seed(0)

    model, chromosome = training.generate_model(hidden_layers=(10,))
    score, dframes = simulate_game(model)