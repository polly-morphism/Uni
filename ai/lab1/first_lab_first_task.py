# First task of the first lab AI
from math import exp
from random import random

N = 4


class ClassicNeuron:
    """Class for classic neuron"""

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
            raise ValueError(f"Розмірність вектору {N}")
        self._x = x

    def activate_function(self):
        """Активаційна функція, в нашому випадку сигмоїда"""
        return 1 / (1 + exp(-self.x_s))

    def calculate_x_s(self):
        """Функція для обрахунку суми комбінованго входу"""
        return sum([self._x[j] * self.w[j] for j in range(N)])

    def train(self):
        """Функція для тренування нейрону, на виході отримуємо нові ваги"""
        while True:
            self.x_s = self.calculate_x_s()

            self.y_i = self.activate_function()

            dn = abs((self.y_r - self.y_i) / self.y_r)

            print(f"\nІтарація: {self.i}\ny_i = {self.y_i}\ndn = {dn}")

            if dn <= self.dd:
                print(
                    f"\nНові ваги: w1:{self.w[0]} w2:{self.w[1]} w3:{self.w[2]} w4:{self.w[3]}"
                )
                print(f"y = {self.y_i} \n")
                return self.w

            else:
                q = (
                    self.y_i * (1 - self.y_i) * (self.y_r - self.y_i)
                )  # друга частина відповісти чим залежить від функції активації похідна функції активації, яка виражена
                for j in range(N):
                    dw = self._x[j] * q
                    self.w[j] += dw

            self.i += 1


if __name__ == "__main__":
    neuron = ClassicNeuron([1, 3, 5, 7], 0.3, 0.1)  # Створюємо екземпляр класу

    neuron.train()  # тренуємо нейрон

    neuron.x = [1, 3.5, 5.4, 7.2]  # робимо тестові дані

    neuron.calculate_x_s()  # Рахуємо комбінований вхід

    print(f"End: {neuron.activate_function()}")  # активуэмо нейрон
