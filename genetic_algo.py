import random, sys
import snake_sim, training
from tqdm import trange, tqdm
import numpy as np
import matplotlib.pyplot as plt
import joblib

import logging
from warnings import simplefilter
from sklearn.exceptions import ConvergenceWarning


logging.basicConfig(level=logging.INFO)
simplefilter('ignore', category=ConvergenceWarning)


def init_pop(nb=100, NNetwork=(10,)):
    logging.info('Generating initial population...')
    pop = [training.generate_model(hidden_layers=NNetwork) for _ in trange(nb)]
    return pop

def get_fitness(model):
    score, dframes = snake_sim.simulate_game(model)
    fitness = score
    return fitness, (score, dframes)

def get_ranking(pop):
    ranking = [(ind[0], ind[1], get_fitness(ind[0])) for ind in pop]
    ranking = sorted(ranking, reverse=True, key=lambda x: x[2][0])
    return ranking

def get_selection(ranking, nb=100, portion=0.2):
    last_ind = int(portion * nb)
    selection = ranking[:last_ind]
    return selection

def trigger_mutations(chromosomes, mutation_rate):
    for i in range(len(chromosomes)):
        for j in range(len(chromosomes[i])):
            if random.random() < mutation_rate:
                chromosomes[i][j] = training.get_coef()
    return chromosomes

def crossover(parents, mutation_rate, NNetwork):
    # chromosomes = [[], []]
    # indexes = [0] + random.sample(range(len(parents[0][1][0])), 4) + [len(parents[0][1][0])]
    # for i in range(1, len(indexes), 2):

    # min_range = int(len(parents[0][1][0]) * 0.1)
    # max_range = int(len(parents[0][1][0]) * 0.9)
    # xover_point = random.randrange(min_range, max_range)
    # chromosomes = [
    #     np.concatenate((parents[0][1][0][:xover_point], parents[1][1][0][xover_point:])),
    #     np.concatenate((parents[1][1][0][:xover_point], parents[0][1][0][xover_point:]))
    # ]
    
    chromosomes = [[], []]
    for i in range(len(parents[0][1][0])):
        if random.random() > 0.5:
            chromosomes[0] += parents[0][1][0][i]
            chromosomes[1] += parents[1][1][0][i]
        else:
            chromosomes[1] += parents[0][1][0][i]
            chromosomes[0] += parents[1][1][0][i]

    chromosomes = trigger_mutations(chromosomes, mutation_rate)
    children = [training.generate_model(coefs_list=chromosome, hidden_layers=NNetwork) for chromosome in chromosomes]
    return children

def reproduction(selection, nb=100, mutation_rate=0.05, NNetwork=(10,)):
    # Elitist selection
    new_pop = selection[:1]
    # then usual reproduction
    while len(new_pop) < nb:
        parents = random.sample(selection, 2)
        children = crossover(parents, mutation_rate, NNetwork)
        new_pop.extend(children)
    return new_pop[:nb]


def update_line(figure, line, new_x, new_y):
    new_xdata = np.append(line.get_xdata(), new_x)
    new_ydata = np.append(line.get_ydata(), new_y)

    line.set_xdata(new_xdata)
    line.set_ydata(new_ydata)
    
    plt.xlim([0, max(1, new_x)])
    if np.max(new_ydata) >= line.axes.get_ylim()[1]:
        plt.ylim([0, np.max(new_ydata)])

    figure.canvas.draw()
    figure.canvas.flush_events()


if __name__=='__main__':
    np.random.seed(0)
    random.seed(0)

    isInteractive = False
    if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
        isInteractive = True

    if isInteractive:
        plt.ion()
        figure, ax = plt.subplots()
        line, = ax.plot([],[], '-')
        plt.axis(xmin=0, xmax=1, ymin=0, ymax=5)

    best_fits = []
    best_scores = []

    nb = 20
    portion = 0.2
    mutation_rate = 0.05
    generations = 200
    NNetwork = (8,)

    logging.info(f'Population: {nb}')
    logging.info(f'Selection rate: {portion:.1%}')
    logging.info(f'Mutation rate: {mutation_rate:.1%}')
    logging.info(f'Neural Network: {NNetwork}')

    pop = init_pop(nb, NNetwork)
    ranking = get_ranking(pop)

    for i in range(generations):
        logging.info('---------------------------------')
        logging.info(f'Generation {i}')

        selection = get_selection(ranking, nb, portion)
        pop = reproduction(selection, nb, mutation_rate, NNetwork)
        ranking = get_ranking(pop)

        top5 = [ind[2][1][0] for ind in ranking[:5]]
        logging.info(f'score top 5: {top5}')

        logging.info(f'Best fitness: {ranking[0][2][0]}')
        logging.info(f'Best score: {ranking[0][2][1][0]}')

        best_snake = ranking[0]
        model, fitness, score, dframes = best_snake[0], best_snake[2][0], best_snake[2][1][0], best_snake[2][1][1]
        # model: best_snake[0], coefs: best_snake[1], results: best_snake[2]
        # fitness: best_snake[2][0], score: best_snake[2][1][0], dframes: best_snake[2][1][1]
        best_fits.append(fitness)
        best_scores.append(score)
        if score > 20:
            joblib.dump(model, 'save_model.pkl')
            logging.warning('Saved model to "save_model.pkl"')
        if isInteractive:
            update_line(figure, line, i, score)

    plt.savefig('results_ga/final_plot1.png')
