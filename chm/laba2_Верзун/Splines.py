from pylab import *

xi = [-2, -1, 1, 3]
yi = [2, 1, 3, 1]
n = len(xi) - 1
A = 2
B = 4
hi = np.diff(xi)
di = np.divide(np.diff(yi), hi)
List_x_points = []
List_x_points_derivatives = []
List_Si = []
List_Si_derivatives = []

system = np.array(
    [
        [1, 0.5, 0, 0],
        [hi[0], 2 * (hi[0] + hi[1]), hi[1], 0],
        [0, hi[1], 2 * (hi[1] + hi[2]), hi[2]],
        [0, 0, 0.5, 1],
    ]
)

answers = np.array(
    [
        3 / hi[0] * (di[0] - A),
        6 * (di[1] - di[0]),
        6 * (di[2] - di[1]),
        3 / hi[2] * (B - di[2]),
    ]
)

result = np.linalg.solve(system, answers)


print("mi = ", result, "\n")
for k in range(0, len(xi) - 1):
    s_k_0 = yi[k]
    s_k_1 = di[k] - hi[k] * (2 * result[k] + result[k + 1]) / 6
    s_k_2 = result[k] / 2
    s_k_3 = (result[k + 1] - result[k]) / (6 * hi[k])
    spline = f"S{k}(x) = {s_k_0} + ({s_k_1})(x - ({xi[k]})) + ({s_k_2})(x - ({xi[k]}))**2 + ({s_k_3})(x - ({xi[k]}))**3"
    print(spline)


for i in range(n):
    x_points = np.linspace(xi[i], xi[i + 1], 100)
    Si = []
    Si_derivative = []
    Si_second_derivatives = []
    for j in range(100):
        Si.append(
            yi[i]
            + (di[i] - (hi[i] * (2 * result[i] + result[i + 1]) / 6))
            * (x_points[j] - xi[i])
            + (result[i] / 2) * math.pow((x_points[j] - xi[i]), 2)  # Кубічний
            + ((result[i + 1] - result[i]) / 6 / hi[i]) * (x_points[j] - xi[i]) ** 3
        )

        Si_derivative.append(
            (di[i] - (hi[i] * (2 * result[i] + result[i + 1]) / 6))
            + 2 * (result[i] / 2) * (x_points[j] - xi[i])  # Похідна кубічного поліному
            + 3 * ((result[i + 1] - result[i]) / 6 / hi[i]) * (x_points[j] - xi[i]) ** 2
        )

    List_Si.append(Si)
    List_x_points.append(x_points)
    List_Si_derivatives.append(Si_derivative)
    List_x_points_derivatives.append(x_points)


plt.figure(1, (12, 9))
plt.plot(List_x_points[0], List_Si[0], color="#DC143C", label="Куб Сплайн 0")
plt.plot(List_x_points[1], List_Si[1], color="#FF0000", label="Куб Сплайн 1")
plt.plot(List_x_points[2], List_Si[2], color="#B22222", label="Куб Сплайн 2")

plt.plot(
    List_x_points_derivatives[0],
    List_Si_derivatives[0],
    color="#1E90FF",
    label="1ша Похідна 0",
)
plt.plot(
    List_x_points_derivatives[1],
    List_Si_derivatives[1],
    color="#022fba",
    label="1ша Похідна 1",
)
plt.plot(
    List_x_points_derivatives[2],
    List_Si_derivatives[2],
    color="#051547",
    label="1ша Похідна 2",
)

plt.plot(xi, yi, "o", color="black")
plt.plot(xi, yi, color="black", label="Лін Сплайн")

plt.legend()
plt.grid(True)
plt.show()
