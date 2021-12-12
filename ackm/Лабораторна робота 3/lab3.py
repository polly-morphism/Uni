import numpy as np
from matplotlib import pyplot as plt


class RungeKutta:
    @staticmethod
    def f(x, y, z):
        return 3 * z - 2 * y + 2 * x - 3

    @staticmethod
    def g(x, y, z):
        return z

    @classmethod
    def calculate(cls):
        x_0 = 0
        y_0 = 1
        z_0 = 2
        h = 0.2
        list_x = [x_0]
        list_y = [y_0]
        list_z = [z_0]
        print("\tX\t\tY\t\tZ")
        while x_0 < 2.00:
            k1 = h * cls.f(x_0, y_0, z_0)
            q1 = h * cls.g(x_0, y_0, z_0)

            k2 = h * cls.f(x_0 + h / 2.0, y_0 + q1 / 2.0, z_0 + k1 / 2.0)
            q2 = h * cls.g(x_0 + h / 2.0, y_0 + q1 / 2.0, z_0 + k1 / 2.0)

            k3 = h * cls.f(x_0 + h / 2.0, y_0 + q2 / 2.0, z_0 + k2 / 2.0)
            q3 = h * cls.g(x_0 + h / 2.0, y_0 + q2 / 2.0, z_0 + k2 / 2.0)

            k4 = h * cls.f(x_0 + h, y_0 + q3, z_0 + k3)
            q4 = h * cls.g(x_0 + h, y_0 + q3, z_0 + k3)

            z_1 = z_0 + (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
            y_1 = y_0 + (q1 + 2.0 * q2 + 2.0 * q3 + q4) / 6.0

            print(
                "\t"
                + str(np.round(x_0 + h, 3))
                + "\t\t"
                + str(np.round(y_1, 3))
                + "\t\t"
                + str(np.round(z_1, 3))
            )

            y_0 = y_1
            z_0 = z_1
            x_0 += h
            list_x.append(x_0)
            list_y.append(y_0)
            list_z.append(z_0)

        plt.plot(list_x, list_y, label="f")
        plt.plot(list_x, list_z, label="f'")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    RungeKutta.calculate()
