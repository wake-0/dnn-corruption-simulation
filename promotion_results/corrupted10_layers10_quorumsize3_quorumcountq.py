import random

import matplotlib.pyplot as plt
import numpy as np

def split_into_layers(validators, number_of_layers, quorum_size, quorum_count):
    """ Split the array of validators into validators per layer.
    :type validators: int[]
    :param validators: An array of all validators over all layers. 

    :type number_of_layers: int
    :param number_of_layers: The number of layers.

    :type quorum_size: int
    :param quorum_size: The size of a quorum.

    :type quorum_count: int
    :param quorum_count: The number of quorums inside the layers.

    :rtype: int[] of size quorum_size
    """
    layers = [0] * number_of_layers
    for quorum_index in random.sample(range(0, number_of_layers), quorum_count):
        layers[quorum_index] = 1

    current_index = 0
    for layer in layers:
        if layer == 0:
            yield [validators[current_index]]
            current_index += 1
        else:
            yield validators[current_index:current_index+quorum_size]
            current_index += quorum_size

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
    for _ in range(iterations):
        # always return ten corrupted validator
        yield 10

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
    for number_of_corrupted in fixed_corrupted_generator(number_of_validators, iterations, number_of_validators//10):
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

def simulate(iterations, number_of_layers, quorum_size):
    """ Executes a simulation and calculates the results.
    :type iterations: int
    :param iterations: The number of iterations.

    :type number_of_layers: int
    :param number_of_layers: The number of layers which are simulated.

    :type quorum_size_range: int[]
    :param quorum_size_range: The number of validators per layer. Therefore,
    the validators have the condition len(validators) % quorum_size == 0.

    :rtype: { 'quorum_count': [], 'attack_successful_prob': [] }
    """

    result = {
        'quorum_count': [],
        'attack_successful_prob': []
    }

    number_of_corrupted = {}

    for quorum_count in range(0, number_of_layers + 1):
        validators_count = (quorum_size*quorum_count) + (number_of_layers - quorum_count) 
        number_of_corrupted[quorum_count] = 0

        min_quorum_threshold = quorum_size // 2 + 1
        for combination in create_random_corrupted_combinations(validators_count, iterations):
            layers = list(split_into_layers(combination, number_of_layers, quorum_size, quorum_count))
            print(layers)
            for quorum in layers:
                current_threshold = sum(quorum)

                # Is no quorum
                if len(quorum) == 1:
                    # Is corrupted
                    if current_threshold == 1:
                        number_of_corrupted[quorum_count] =  number_of_corrupted[quorum_count] + 1
                        break

                # Is quorum
                else:
                    # Is corrupted
                    if current_threshold >= min_quorum_threshold:
                        number_of_corrupted[quorum_count] =  number_of_corrupted[quorum_count] + 1
                        break

    """
    Iterate all different quorum counts.
    """
    for quorum_count in range(0, number_of_layers + 1):
        successful_corrupted = number_of_corrupted[quorum_count]
        attack_successful_prob = successful_corrupted / iterations
        print("Quorum Count: " + str(quorum_count))
        print("( Successful Corrupted Count: " + str(successful_corrupted) + " )")
        print("( Quorum Count: " + str(quorum_count) + ", Attack Success Probability: " + str(attack_successful_prob) + " )")
        print("-"*50)

        result['quorum_count'].append(quorum_count)
        result['attack_successful_prob'].append(attack_successful_prob)

    return result

# CALL THE SIMULATION
iterations = 1000
quorum_size = 3
number_of_layers = 10
result = simulate(iterations, number_of_layers, quorum_size)
print(result)

quorum_count = result['quorum_count']
attack_successful_prob = result['attack_successful_prob']

plt.xlabel('Quorum Count')
plt.ylabel('Attack Success Probability')
plt.title('Quorum Attack Success Probability')
plt.bar(quorum_count, attack_successful_prob)
plt.show()
