import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import _pickle as picklerick
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_moons, make_circles


class MLP(object):

    def __init__(self, X, y, filename='mlp', inspect_rate=50, iterations=1000, learning_rate=0.000025, nodes=(2,8,4,1), batch=(False, 0), activation_function='sigmoid'):
        # store input and expected output data
        self.X = X
        self.y = np.atleast_2d(y)

        # saved network name
        self.filename = filename

        # inspect rate to print and store current error and accuracy
        self.inspect_rate = inspect_rate

        # decide whether batching occurs (not implemented yet)
        self.batch, self.batch_size = batch

        # number of iterations
        self.iterations = iterations

        # learning hyperparameters
        self.learning_rate = learning_rate

        # activation function
        self.activation_function = activation_function

        # network layers
        self.nodes = nodes
        # store costs and accuracy over iterations
        self.costs = []
        self.accuracies = []

        # initialize placeholder layers
        self.layers = []

        # initialize placeholder weights
        self.weights = self.initialize_weights()

    def initialize_weights(self):
        weights = []
        for i in range(1, len(self.nodes)):
            weights.append(np.random.randn(self.nodes[i - 1] + 1, self.nodes[i]))
        return weights

    def train(self, X, y):
        for i in range(self.iterations):
            hypothesis = self.feedforward(X)
            self.backpropagate(hypothesis, self.y.T)
            cost = np.average(0.5 * ((y - hypothesis) ** 2))
            if i % self.inspect_rate == 0:
                self.costs.append(cost)
                accuracy = self.test_accuracy(X, y)
                self.accuracies.append(accuracy)
                print(self.inspect_performance(i, cost, accuracy))

    def test_accuracy(self, X_test, y_test, percent=True):
        hypothesis = self.feedforward(X_test)
        evaluation = np.int_(np.round(hypothesis) == y_test.T)
        if not percent:
            return evaluation
        return np.sum(evaluation) / X_test.shape[0] * 100

    def add_bias(self, x):
        return np.hstack((np.ones((x.shape[0], 1)), x))

    def feedforward(self, X):
        num_weight_matrices = len(self.weights)
        layer = self.add_bias(X)
        self.layers.append(layer)
        for i in range(num_weight_matrices):
            if i == num_weight_matrices - 1:
                w = self.weights[i]
                layer = self.activate(np.dot(layer, w))
            else:
                w = self.weights[i]
                layer = self.add_bias(self.activate(np.dot(layer, w)))
            self.layers.append(layer)
        return layer

    def backpropagate(self, hypothesis, y):
        deltas = [y - hypothesis]
        for layer, weights in zip(reversed(self.layers[:-1]), reversed(self.weights)):
            prev_delta = deltas[-1]
            if prev_delta.shape[1] - 1 != weights.shape[1]:
                delta = prev_delta.dot(weights.T) * self.activate(layer, d=True)
            else:
                delta = prev_delta[:, 1:].dot(weights.T) * self.activate(layer, d=True)
            deltas.append(delta)
        for i in range(1, len(deltas)):
            delta = deltas[i - 1]
            layer = self.layers[:-1][-i]
            if i == 1:
                self.weights[-i] += self.learning_rate * delta.T.dot(layer).T
            else:
                self.weights[-i] += self.learning_rate * delta[:, 1:].T.dot(layer).T

        return deltas

    def activate(self, X, d=False):
        if self.activation_function == 'sigmoid':
            return self.sigmoid(X, d)
        elif self.activation_function == 'tanh':
            return self.tanh(X, d)
        else:
            return self.relu(X, d)

    def sigmoid(self, X, d=False):
        if d:
            return X * (1 - X)
        return 1 / (1 + np.exp(-X))

    def tanh(self, X, d=False):
        if d:
            return 1 - np.tanh(X) ** 2
        return np.tanh(X)

    def relu(self, X, d=False):
        if d:
            return np.multiply(1., (X > 0))
        return np.maximum(X, 0, X)

    def save(self):
        picklerick.dump(self, open("{}.p".format(self.filename), 'wb'))

    def load(self):
        return picklerick.load(open("{}.p".format(self.filename), 'rb'))

    def plot_decision_boundary(self, x, y, c):
        plt.figure(0)
        x_min, x_max = np.min(x), np.max(x)
        y_min, y_max = np.min(y), np.max(y)
        x_1 = np.atleast_2d(np.repeat(np.linspace(x_min - 0.1, x_max + 0.1, 200), 100)).T
        x_2 = np.atleast_2d(np.tile(np.linspace(y_min - 0.1, y_max + 0.1, 200), 100)).T
        X_ = np.column_stack((x_1, x_2))
        classifications = np.round(self.feedforward(X_))

        plt.scatter(X_.T[0], X_.T[1], classifications.T[0], cmap=plt.get_cmap('Blues'))
        plt.scatter(x, y, c=c, marker='.')
        plt.show()

    def plot_performance(self, cost=True, accuracy=True):
        plt.figure(1)
        if cost:
            x_cost = list(range(len(self.costs)))
            y_cost = self.costs
            plt.scatter(x_cost, y_cost, cmap=plt.get_cmap('Oranges'))
        if accuracy:
            x_accuracy = list(range(len(self.accuracies)))
            y_accuracy = self.accuracies
            plt.scatter(x_accuracy, y_accuracy, cmap=plt.get_cmap('Blues'))
        plt.show()

    def inspect_performance(self,iteration, cost, accuracy):
        return "Iteration: {} , Cost: {} , Accuracy: {}".format(iteration, cost, accuracy)

