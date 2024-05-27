import numpy as np
from Neuron import Neuron

class Layer:
    def __init__(self, n_neurons, n_inputs_per_neuron):
        self.neurons = [Neuron(n_inputs_per_neuron) for _ in range(n_neurons)]

    def __call__(self, inputs):
        outputs = np.array([neuron(inputs) for neuron in self.neurons])
        return outputs

    def update_weights(self, inputs, deltas, learning_rate):
        for neuron, delta in zip(self.neurons, deltas):
            neuron.update_weights(inputs, delta, learning_rate)