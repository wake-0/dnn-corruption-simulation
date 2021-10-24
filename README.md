# Description

The following python Simulation can be used to simulate corrupted behaviour on a DNN depending on corrupted layers. To improve the security a quorum based approach is used and can also be simulated.

## Simulation Scripts

There are four different scripts:

- simulation-layers-count.py: By using this script it is possible to change the number of layers for a DNN. Furthermore, the quorum size of each layer and the number of iterations can be adapted.
- simulation-quorum-count.py: By using this script it is possible to simulate different numbers of quorums. Usually, every layer has a quorum by using this script it can be defined how many layers do have a quorum. Furthermore, the number of layers and the size of the quorum can be defined.
- simulation-quorum-size.py: By using this script it is possible to change the size of the quorum and investigate the influence of changing the quorum size. Furthermore, the number of layers and the iterations can be defined.
- simulation-threshold.py: By using this script it is possible to set different thresholds (number of corrupted nodes inside a quorum so that the quorum itself is corrupted). Furthermore, the number of layers, the quorum size and the iterations can be defined.

## Usage:

Every script can be used in combination with python3. 

```
python simulation-layers-count.py
```

## Changing the Simulation
To change a simulation behaviour update the corresponding script. E.g. the binom_corrupted_generator can be exchanged by a fixed_corrupted_generator which is able to produce always the same number of corrupted nodes for each iteration. Beside that, every script has same parameters at bottom which an be changed easily. For xample (simulation-layers-count.py):

```
iteration_count = 10000
quorum_size = 11
layers_range = range(1, 11)
result = simulate(iteration_count, layers_range, quorum_size)
```

Can be changed to:

```
iteration_count = 1000
quorum_size = 5
layers_range = range(1, 5)
result = simulate(iteration_count, layers_range, quorum_size)
```