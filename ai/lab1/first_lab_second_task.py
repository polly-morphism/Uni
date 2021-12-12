from random import random
from math import exp


class TwoLayerPerceptron:
    """Class for two layer perceptron"""

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
    def activate_function(x_s):
        """Активаційна функція, в нашому випадку сигмоїда"""

        return 1 / (1 + exp(-x_s))

    def train(self):
        """Функція для тренування нейрону, на виході отримуємо нові ваги"""

        while True:
            x2_s = self._x * self.w1
            self.y2 = self.activate_function(x2_s)
            x3_s = self.y2 * self.w2
            self.y3 = self.activate_function(x3_s)
            dn = abs((self.y_r - self.y3) / self.y_r)

            if dn < self.dd:
                print(f"Відповідь: {self.y3}")
                return 0

            else:

                q3 = self.y3 * (1 - self.y3) * (self.y_r - self.y3)
                q2 = self.y2 * (1 - self.y2) * (q3 * self.w2)

                delta_w2 = q3 * self.y2
                delta_w1 = q2 * self._x

                self.w1 += delta_w1
                self.w2 += delta_w2

                self.i += 1

                print(f"\nІтарація: {self.i}\ny3 = {self.y3}\ndn = {dn}")


if __name__ == "__main__":
    perceptron = TwoLayerPerceptron(2, 0.1, 0.1)

    perceptron.train()

    perceptron.x = 2.4

    z1 = perceptron.x * perceptron.w1

    z2 = perceptron.activate_function(z1) * perceptron.w2

    print(f"\nРежим розпізнавання: {perceptron.activate_function(z2)}")
