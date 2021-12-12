# First task of the first lab AI
from math import exp
from random import random

import numpy as np
import math
import pandas as pd

np.random.seed(42)

N = 4


class ClassicNeuron:
    # can't believe I worked 2 years as a deep learning engineer just to be doing this now... education system is dead
    def __init__(self, x, y_r, dd):
        self._x = x
        self.y_r = y_r
        self.dd = dd
        self.w = [random() for i in range(N)]
        self.i = 1
        self.y_i = None
        self.x_s = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if len(x) != N:
            raise ValueError(f"Dim {N}")
        self._x = x

    def sigmoid(self):
        return 1 / (1 + exp(-self.x_s))  # sigmoid activation

    def weighted_sum(self):
        return sum([self._x[j] * self.w[j] for j in range(N)])  # weighted sum

    def train(self):
        # weights update, training
        while True:
            self.x_s = self.weighted_sum()

            self.y_i = self.sigmoid()

            dn = abs((self.y_r - self.y_i) / self.y_r)

            print(f"\n Iteration: {self.i}\n y_i = {self.y_i} \n dn = {dn}")

            if dn <= self.dd:
                print(
                    f"\n New weights: w1:{self.w[0]} w2:{self.w[1]} w3:{self.w[2]} w4:{self.w[3]}"
                )
                print(f"y = {self.y_i} \n")
                return self.w

            else:
                q = self.y_i * (1 - self.y_i) * (self.y_r - self.y_i)
                for j in range(N):
                    dw = self._x[j] * q
                    self.w[j] += dw

            self.i += 1


class TwoLayerPerceptron:
    # this is embarassing
    def __init__(self, x, y_r, dd):
        self.w1 = random()
        self.w2 = random()
        self._x = x
        self.y_r = y_r
        self.dd = dd
        self.y2 = None
        self.y3 = None
        self.i = 1

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @staticmethod
    def sigmoid(x_s):
        return 1 / (1 + exp(-x_s))

    def train(self):
        while True:
            x2_s = self._x * self.w1
            self.y2 = self.sigmoid(x2_s)
            x3_s = self.y2 * self.w2
            self.y3 = self.sigmoid(x3_s)
            dn = abs((self.y_r - self.y3) / self.y_r)

            if dn < self.dd:
                print(f"Answer: {self.y3}")
                return 0

            else:

                q3 = self.y3 * (1 - self.y3) * (self.y_r - self.y3)
                q2 = self.y2 * (1 - self.y2) * (q3 * self.w2)

                delta_w2 = q3 * self.y2
                delta_w1 = q2 * self._x

                self.w1 += delta_w1
                self.w2 += delta_w2

                self.i += 1

                print(f"\n Iteration: {self.i} \n y3 = {self.y3} \n dn = {dn}")


def calculate_f(x):
    y_m = 1 / (1 + (1 / math.e ** x))
    return y_m


def calculate_net(x, w):
    net = sum(x * w)
    return net


def calculate_error(y_m, y):
    error = abs((y_m - y) / y)
    return error


def calculate_new_w(y_m, y, w, x):
    sigma = y_m * (1 - y_m) * (y - y_m)
    w_diff = x * sigma
    w_new = w + w_diff
    return w_new


def calculate_rand_w(n):
    w_rand = np.random.uniform(0, 1, n)
    w = []
    for i in range(n):
        w.append(w_rand[i])
    return np.array(w)


def recognition(x, w_1_2, w_2_3, w_0_1, w_0_2):
    total_1 = np.array(x).dot(w_1_2) + w_0_1

    y_m_1 = np.array(list(map(calculate_f, np.array(total_1))))

    total_2 = y_m_1.dot(w_2_3) + w_0_2

    y_m_2 = calculate_f(total_2[0][0])

    return y_m_2


def recognition_func(x, w_12, w_01, w_23, w_02):
    total_1 = x.dot(w_12)
    # vector x*w of the first hidden layer values

    total_1 = total_1 + w_01
    # vector y_molule of the first hidden layer

    y_m_1 = np.array(list(map(calculate_f, total_1)))

    total_2 = y_m_1.dot(w_23) + w_02

    # final y_molule of the first hidden layer
    y_m_2 = calculate_f(total_2[0][0])

    return y_m_2


def find_new_w(x, y, y_m_2, y_m_1, w_12, w_01, w_23, w_02):
    q_3_2 = y_m_2 * (1 - y_m_2) * (y - y_m_2)

    b_3_2 = q_3_2 * y_m_1
    b_3_2_0 = x0 * q_3_2

    for j in range(len(b_3_2[0])):
        w_23[j][0] = w_23[j][0] + b_3_2[0][j]
    w_02 = w_02 + b_3_2_0
    q_2_1 = []
    for k in range(len(y_m_1[0])):
        q_2_1.append([y_m_1[0][k] * (1 - y_m_1[0][k]) * (q_3_2 * w_23[k][0])])

    b_2_1 = (np.array(q_2_1)).dot(np.matrix([x0, x[0], x[1]])).transpose()

    w_12 = w_12 + b_2_1[1:][:]
    w_01 = w_01 + b_2_1[0][:]

    return w_01, w_12, w_02, w_23


def learn_alg(x, y, w_12, w_01, w_23, w_02):
    total_1 = x.dot(w_12)
    # vector x*w of the first hidden layer values

    total_1 = total_1 + w_01
    # vector y_molule of the first hidden layer

    y_m_1 = np.array(list(map(calculate_f, total_1)))

    total_2 = y_m_1.dot(w_23) + w_02

    # final y_molule of the first hidden layer
    y_m_2 = calculate_f(total_2[0][0])

    error = calculate_error(y_m_2, y)

    w01, w12, w02, w23 = find_new_w(x, y, y_m_2, y_m_1, w_12, w_01, w_23, w_02)

    return y_m_2, error, np.array(w12), np.array(w01), w23, w02


def online_learning(X, Y, n_epohs):
    w_1_2 = [calculate_rand_w(3), calculate_rand_w(3)]
    w_0_1 = [calculate_rand_w(3)]

    w_2_3 = [calculate_rand_w(1), calculate_rand_w(1), calculate_rand_w(1)]
    w_0_2 = calculate_rand_w(1)

    n = 0
    while n <= n_epohs:
        y_model_n = []
        error_n = []
        for i in range(len(Y)):
            y_m_2, error, w_1_2, w_0_1, w_2_3, w_0_2 = learn_alg(
                X[i], Y[i], w_1_2, w_0_1, w_2_3, w_0_2
            )
            y_model_n.append(y_m_2)
            error_n.append(error)
        if n % 100 == 0:
            print("\n Epoch  #{}".format(n))
            print("Y modeled: {}".format(y_model_n))
            print("Delta {}".format(error_n))
        n += 1
    return w_1_2, w_0_1, w_2_3, w_0_2


if __name__ == "__main__":
    print("Task1")
    neuron = ClassicNeuron([1, 3, 5, 7], 0.3, 0.1)

    neuron.train()

    neuron.x = [1, 3.5, 5.4, 7.2]

    neuron.weighted_sum()

    print(f"End: {neuron.sigmoid()}")

    print("Task2")

    perceptron = TwoLayerPerceptron(2, 0.1, 0.1)

    perceptron.train()

    perceptron.x = 2.4

    z1 = perceptron.x * perceptron.w1

    z2 = perceptron.sigmoid(z1) * perceptron.w2

    print(f"\n Detection: {perceptron.sigmoid(z2)}")

    print("Task3")

    x0 = 1

    y = 0.03
    E = 0.1

    x = np.array([1.0, 1.5])  # input vector
    w_1_2 = [calculate_rand_w(3), calculate_rand_w(3)]  # x1, x2 weights
    w_0_1 = [calculate_rand_w(3)]  # weights
    w_2_3 = [
        calculate_rand_w(1),
        calculate_rand_w(1),
        calculate_rand_w(1),
    ]  # last layer weights
    w_0_2 = calculate_rand_w(1)  # last neuron

    total_1 = x.dot(w_1_2)  # weighted sum
    # vector x*w of the first hidden layer values
    total_1 = total_1 + w_0_1

    # vector y_molule of the first hidden layer
    y_m_1 = np.array(list(map(calculate_f, total_1)))

    total_2 = y_m_1.dot(w_2_3) + w_0_2

    # final y_molule of the first hidden layer
    y_m_2 = calculate_f(total_2[0][0])

    error = calculate_error(y_m_2, y)
    df = pd.DataFrame(columns=["y model", "delta"])

    i = 0
    while True:
        if error <= E:
            break
        else:
            df = df.append({"y model": y_m_2, "delta": error}, ignore_index=True)

            q_3_2 = y_m_2 * (1 - y_m_2) * (y - y_m_2)

            b_3_2 = q_3_2 * y_m_1
            b_3_2_0 = x0 * q_3_2

            for j in range(len(b_3_2[0])):
                w_2_3[j][0] = w_2_3[j][0] + b_3_2[0][j]
            w_0_2 = w_0_2 + b_3_2_0
            q_2_1 = []
            for k in range(len(y_m_1[0])):
                q_2_1.append([y_m_1[0][k] * (1 - y_m_1[0][k]) * (q_3_2 * w_2_3[k][0])])

            b_2_1 = (np.array(q_2_1)).dot(np.matrix([x0, x[0], x[1]])).transpose()

            w_1_2 = w_1_2 + b_2_1[1:][:]
            w_0_1 = w_0_1 + b_2_1[0][:]

            total_1 = x.dot(w_1_2)
            total_1 = np.array(total_1 + w_0_1)
            y_m_1 = np.array(list(map(calculate_f, total_1)))

            total_2 = y_m_1.dot(w_2_3) + w_0_2
            y_m_2 = calculate_f(total_2[0][0])

            error = calculate_error(y_m_2, y)
            i = i + 1
    print(w_0_2)

    print("n iterations = " + str(i))
    print("y_m = " + str(y_m_2))
    print("\n")
    print("w_1 = " + str(w_1_2))
    print("\n")
    print("w_2 = " + str(w_2_3))
    print("\n")
    print(df)

    print("\n")
    print("Detection")
    print("Example: " + str([1.1, 1.4]))
    print(
        "y_m = " + str(recognition([1.1, 1.4], w_1_2, w_2_3, w_0_1=w_0_1, w_0_2=w_0_2))
    )

    print("Online Learning")
    X = np.array([[1.0, 1.0], [2.0, 1.0], [1.5, 1.5], [1.0, 2.5]])  # input vector
    Y = np.array([0.02, 0.03, 0.03, 0.035])
    x0 = 1

    n_epohs = 1000

    w_1_2, w_0_1, w_2_3, w_0_2 = online_learning(X, Y, n_epohs)

    print("\nRecognition part")
    print("x = {}".format([1.0, 1.5]))
    print(
        "y = {}".format(
            recognition_func(np.array([1.0, 1.5]), w_1_2, w_0_1, w_2_3, w_0_2)
        )
    )
