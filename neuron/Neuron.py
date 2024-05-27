import numpy as np


class Neuron:
    def __init__(self, n_inputs, bias=0., weights=None):
        self.b = bias
        if weights:
            self.ws = np.array(weights)
        else:
            self.ws = np.random.rand(n_inputs)
        self.output = None  # Initialize output attribute

    def _f(self, x):  # activation function (here: leaky_relu)
        return np.maximum(x * 0.1, x)

    def __call__(self, xs):  # calculate the neuron's output: multiply the inputs with the weights and sum the values together, add the bias value,
        return self._f(xs @ self.ws + self.b)    # then transform the value via an activation function

    def _f_derivative(self, x):  # derivative of leaky_relu
        return np.where(x > 0, 1, 0.1)

    def update_weights(self, inputs, delta, learning_rate):
        gradient = delta * inputs
        self.ws -= learning_rate * gradient
        self.b -= learning_rate * delta










