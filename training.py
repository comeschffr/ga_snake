import random, logging
import numpy as np
from sklearn.neural_network import MLPClassifier


def prepare_sensors(sensors):
    X = sensors['head_direction']
    X.append(sensors['distance_to_apple'])
    X.extend(sensors['apple_direction'])
    X.extend(sensors['distance_to_obstacle'])
    return X


def init_coefs(hidden_layers, input_nb):
    coefs_list = [get_coef((input_nb, hidden_layers[0]))]
    for i in range(len(hidden_layers)-1):
        coefs_list.append(get_coef((hidden_layers[i], hidden_layers[i+1])))
    coefs_list.append(get_coef((hidden_layers[-1], 4)))
    return coefs_list

def coefs_to_list(coefs_array):
    return np.concatenate([arr.ravel() for arr in coefs_array])

def coefs_to_array(coefs_list, hidden_layers, input_nb):
    index = input_nb*hidden_layers[0]
    coefs_array = [np.array(coefs_list[:index]).reshape((input_nb, hidden_layers[0]))]
    for i in range(len(hidden_layers)-1):
        new_index = index + hidden_layers[i] * hidden_layers[i+1]
        coefs_array.append(np.array(coefs_list[index:new_index]).reshape((hidden_layers[i], hidden_layers[i+1])))
        index = new_index
    coefs_array.append(np.array(coefs_list[index:]).reshape((hidden_layers[-1], 4)))
    return coefs_array

def get_coef(arr_shape=None):
    if arr_shape is None:
        return np.random.normal(0, 1)
    else:
        return np.random.normal(0, 1, arr_shape)


def init_bias(hidden_layers):
    bias_list = [np.ones((layer,)) for layer in hidden_layers]
    bias_list.append(np.ones((4,)))
    return bias_list

def bias_to_list(bias_array):
    return np.concatenate(bias_array)

def bias_to_array(bias_list, hidden_layers):
    index = 0
    bias_array = []
    for i in range(len(hidden_layers)):
        new_index = index + hidden_layers[i]
        bias_array.append(np.array(bias_list[index:new_index]))
        index = new_index
    bias_array.append(np.array(bias_list[index:]))
    return bias_array


def generate_model(coefs_list=None, bias_list=None, hidden_layers=(15, 10), input_nb=13):
    model = MLPClassifier(hidden_layer_sizes=hidden_layers)
    init_X = np.ones((4, input_nb))
    init_y = [0, 1, 2, 3]
    model.fit(init_X, init_y)

    if coefs_list is None:
        model.coefs_ = init_coefs(hidden_layers, input_nb)
        coefs_list = coefs_to_list(model.coefs_)
    else:
        model.coefs_ = coefs_to_array(coefs_list, hidden_layers, input_nb)

    if bias_list is None:
        model.intercepts_ = init_bias(hidden_layers)
        bias_list = bias_to_list(model.intercepts_)
    else:
        model.intercepts_ = bias_to_array(bias_list)

    chromosome = (coefs_list, bias_list)

    return (model, chromosome)


def make_decision(sensors, model):
    X = prepare_sensors(sensors)

    pred = model.predict([X])

    return pred


if __name__=='__main__':
    model, chromosome = generate_model(hidden_layers=(2, 3, 4))

    sensors = {
        'head_direction': [False, True, False, False], 
        'distance_to_apple': 1, 
        'apple_direction': [False, False, True, False], 
        'distance_to_obstacle': [6, 4, 5, 7]
    }
    pred = make_decision(sensors, model)
    print(pred)