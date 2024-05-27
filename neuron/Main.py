import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from Network import Network


n_samples = 1000
X, y = make_circles(n_samples, noise=0.03, random_state=37)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

ann = Network()

epochs = 500
learning_rate = 0.01
# ann.train(X_train, y_train, epochs, learning_rate)

train_predictions = (ann(X_train) > 0.5).astype(int)
test_predictions = (ann(X_test) > 0.5).astype(int)

train_accuracy = accuracy_score(y_train, train_predictions)
test_accuracy = accuracy_score(y_test, test_predictions)

print("Training Accuracy:", train_accuracy)
print("Testing Accuracy:", test_accuracy)


def plot_decision_boundary(X, y, model, title):
    h = 0.01
    x_min, x_max = X[:, 0].min() - 0.1, X[:, 0].max() + 0.1
    y_min, y_max = X[:, 1].min() - 0.1, X[:, 1].max() + 0.1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = np.array([model(np.array([xxi, yyi])) for xxi, yyi in zip(xx.ravel(), yy.ravel())])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z > 0.5, cmap=plt.cm.RdBu, alpha=0.8)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdBu, edgecolors='k')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title(title)
    plt.show()


# plot_decision_boundary(X_test, y_test, ann, 'Decision Boundary on Testing Set')

def visualize_network():
    fig, ax = plt.subplots()

    # Define the positions of neurons
    positions = {
        'input': [(0, 0.9), (0, 0.5), (0, 0.1)],
        'hidden1': [(0.3, 0.9), (0.3, 0.65), (0.3, 0.4), (0.3, 0.1)],
        'hidden2': [(0.6, 0.9), (0.6, 0.65), (0.6, 0.4), (0.6, 0.1)],
        'output': [(0.9, 0.5)]
    }

    for layer, neurons in positions.items():
        for x, y in neurons:
            circle = plt.Circle((x, y), 0.05, color='black', fill=True)
            ax.add_artist(circle)

    for (start_layer, start_neurons), (end_layer, end_neurons) in zip(positions.items(), list(positions.items())[1:]):
        for (x1, y1) in start_neurons:
            for (x2, y2) in end_neurons:
                ax.plot([x1, x2], [y1, y2], 'k-')

    ax.set_xlim(-0.1, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.show()


visualize_network()
