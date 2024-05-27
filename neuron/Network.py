import numpy as np
from sklearn.metrics import accuracy_score
from Layer import Layer
from Neuron import Neuron


class Network:
    def __init__(self):
        self.input_layer = Layer(3, 2)
        self.hidden_layer1 = Layer(4, 2)
        self.hidden_layer2 = Layer(4, 4)
        self.output_layer = Neuron(4)

    def __call__(self, inputs):
        self.h1_outputs = self.hidden_layer1(inputs).T
        self.h2_outputs = self.hidden_layer2(self.h1_outputs).T
        self.output = self.output_layer(self.h2_outputs).T
        return self.output

    def backward(self, X, y, learning_rate):
        output_delta = (self.output - y) * self.output_layer._f_derivative(self.output)

        h2_deltas = np.dot(output_delta, self.output_layer.ws) * self.hidden_layer2.neurons[0]._f_derivative(self.h2_outputs.T)
        h1_deltas = np.dot(h2_deltas, np.array([neuron.ws for neuron in self.hidden_layer2.neurons]).T) * self.hidden_layer1.neurons[0]._f_derivative(self.h1_outputs.T)

        self.output_layer.update_weights(self.h2_outputs, output_delta, learning_rate)
        self.hidden_layer2.update_weights(self.h1_outputs.T, h2_deltas.T, learning_rate)
        self.hidden_layer1.update_weights(X.T, h1_deltas.T, learning_rate)

    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            for xi, yi in zip(X, y):
                self.__call__(xi)
                self.backward(xi, yi, learning_rate)
            if epoch % 100 == 0:
                predictions = (self.__call__(X) > 0.5).astype(int)
                accuracy = accuracy_score(y, predictions)
                print(f"Epoch {epoch}: Accuracy = {accuracy}")