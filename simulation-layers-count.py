import random

import matplotlib.pyplot as plt
import numpy as np

def split_into_layers(validators, quorum_size):
    """ Split the array of validators into validators per layer.
    :type validators: int[]
    :param validators: An array of all validators over all layers. 

    :type quorum_size: int
    :param quorum_size: Number of validators per layer. Therefore,
    the validators have the condition len(validators) % quorum_size == 0.

    :rtype: int[] of size quorum_size
    """
    for i in range(0, len(validators), quorum_size):
        yield validators[i:i + quorum_size]

def fixed_corrupted_generator(number_of_validators, iterations, number_of_corrupted=0):
    """ Produce a fixed number of corrupted nodes for n iterations.
    :type number_of_validators: int
    :param number_of_validators: Is not used.

    :type iterations: int
    :param iterations: Number of values returned.

    :type number_of_corrupted: int
    :param number_of_corrupted: Fixed number of corrupted validators. Every 
    iteration returns the same fixed number of corrupted validators.

    :rtype: int
    """
    for _ in range(iterations + 1):
        yield number_of_corrupted

def binom_corrupted_generator(number_of_validators, iterations, ratio=0.5):
    """ Produce a binomial distributed number of corrupted nodes for n iterations.
    :type number_of_validators: int
    :param number_of_validators: The number of validators over all layers. 

    :type iterations: int
    :param iterations: Number of values returned.

    :type ratio: float
    :param ratio: Defines the distribution ratio for the binomial distribution.

    :rtype: int
    """
    for number_of_corrupted in np.random.binomial(number_of_validators, ratio, iterations):
        yield number_of_corrupted

def create_random_corrupted_combination(number_of_validators, number_of_corrupted):
    """ Create a random corrupted combination.
        E.g. number_of_validators = 5, number_of_corrupted = 2
        Possible outputs are:
        [0, 1, 0, 0, 1]
        [1, 0, 0, 1, 0]
    :type number_of_validators: int
    :param number_of_validators:  The number of validators over all layers. 

    :type number_of_corrupted: int
    :param number_of_corrupted: The number of corrupted validators in the generated combination.

    :rtype: int[]
    """
    if number_of_corrupted >= number_of_validators:
        return [1] * number_of_validators

    combination = [0] * number_of_validators
    for corrupted_index in random.sample(range(number_of_validators), number_of_corrupted):
        combination[corrupted_index] = 1
    return combination

def create_random_corrupted_combinations(number_of_validators, iterations):
    """ Create corrupted combinations based on the given corrupted_generator.
        The binom_corrupted_generator(number_of_validators, iterations, ratio=0.5) can be replaced
        by fixed_corrupted_generator(number_of_validators, iterations, number_of_corrupted=0)
    :type number_of_validators: int
    :param number_of_validators:  The number of validators over all layers. 

    :type iterations: int
    :param iterations: Number of values returned.

    :rtype: int[][] multiple validator combinations
    """
    for number_of_corrupted in binom_corrupted_generator(number_of_validators, iterations):
        combination = create_random_corrupted_combination(number_of_validators, number_of_corrupted)
        yield combination

def threshold_range_from_to(min_threshold, max_threshold):
    """ Create a threshold range from min_threshold to max_threshold (inclusive). 
        Each threshold in the range is used for comparision.
    :type min_threshold: int
    :param min_threshold: The number of the minimal threshold (inclusive).

    :type max_threshold: int
    :param max_threshold: The number of the maximal threshold (inclusive).

    :rtype: int[]
    """
    return range(min_threshold, max_threshold + 1)

def simulate(iterations, layers_range, quorum_size):
    """ Executes a simulation and calculates the results.
    :type iterations: int
    :param iterations: The number of iterations.

    :type layers_range: int[]
    :param layers_range: The range of layers which are simulated.

    :type quorum_size: int
    :param quorum_size: Number of validators per layer. Therefore,
    the validators have the condition len(validators) % quorum_size == 0.

    :rtype: { 'layers': [], 'attack_successful_prob': [] }
    """

    result = {
        'layers': [],
        'attack_successful_prob': []
    }

    number_of_corrupted = {}

    for number_of_layers in layers_range:
        validators_count = number_of_layers * quorum_size
        number_of_corrupted[number_of_layers] = 0

        min_quorum_threshold = quorum_size // 2 + 1
        max_quorum_threshold = quorum_size

        for combination in create_random_corrupted_combinations(validators_count, iterations):
            for quorum in split_into_layers(combination, quorum_size):

                current_threshold = sum(quorum)
                is_corrupted = False

                for threshold_count in threshold_range_from_to(min_quorum_threshold, max_quorum_threshold):
                    if current_threshold >= threshold_count:
                        is_corrupted = True
                        break

                # Break after a successful corrupted quorum
                if is_corrupted:
                    number_of_corrupted[number_of_layers] = number_of_corrupted[number_of_layers] + 1
                    break

    """
    Iterate all different layer counts.
    """
    for number_of_layers in layers_range:
        successful_corrupted = number_of_corrupted[number_of_layers]
        attack_successful_prob = successful_corrupted / iterations
        print("( " + str(number_of_layers) + ", " + str(attack_successful_prob) + " )")

        result['layers'].append(threshold_count)
        result['attack_successful_prob'].append(attack_successful_prob)

    return result

# CALL THE SIMULATION
iteration_count = 10000
quorum_size = 11
layers_range = range(1, 11)
result = simulate(iteration_count, layers_range, quorum_size)

layers = result['layers']
attack_successful_prob = result['attack_successful_prob']

plt.xlabel('Layers')
plt.ylabel('Attack Success Probability')
plt.title('Layers Attack Success Probability')
plt.bar(layers, attack_successful_prob)
plt.show()