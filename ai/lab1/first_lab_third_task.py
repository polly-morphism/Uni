import numpy as np
import math
import pandas as pd

np.random.seed(42)


def find_rand_w(n):
    w_rand = np.random.uniform(0, 1, n)
    w = []
    for i in range(n):
        w.append(w_rand[i])
    w = np.array(w)
    return w


def find_f(x):
    y_m = 1 / (1 + (1 / math.e ** x))
    return y_m


def find_net(x, w):
    net = sum(x * w)
    return net


def find_error(y_m, y):
    error = abs((y_m - y) / y)
    return error


def find_new_w(y_m, y, w, x):
    sigma = y_m * (1 - y_m) * (y - y_m)
    w_diff = x * sigma
    w_new = w + w_diff
    return w_new


def find_rand_w(n):
    w_rand = np.random.uniform(0, 1, n)
    w = []
    for i in range(n):
        w.append(w_rand[i])
    return np.array(w)


def recognition(x, w_1_2, w_2_3, w_0_1=w_0_1, w_0_2=w_0_2):
    total_1 = np.array(x).dot(w_1_2) + w_0_1

    y_m_1 = np.array(list(map(find_f, np.array(total_1))))

    total_2 = y_m_1.dot(w_2_3) + w_0_2

    y_m_2 = find_f(total_2[0][0])

    return y_m_2


x0 = 1

y = 0.03
E = 0.1

x = np.array([1.0, 1.5])  # input vector
w_1_2 = [find_rand_w(3), find_rand_w(3)]  # x1, x2 weights
w_0_1 = [find_rand_w(3)]  # weights
w_2_3 = [
    find_rand_w(1),
    find_rand_w(1),
    find_rand_w(1),
]  # last layer weights
w_0_2 = find_rand_w(1)  # last neuron

total_1 = x.dot(w_1_2)  # weighted sum
# vector x*w of the first hidden layer values
total_1 = total_1 + w_0_1

# vector y_molule of the first hidden layer
y_m_1 = np.array(list(map(find_f, total_1)))

total_2 = y_m_1.dot(w_2_3) + w_0_2

# final y_molule of the first hidden layer
y_m_2 = find_f(total_2[0][0])

error = find_error(y_m_2, y)
df = pd.DataFrame(columns=["y модельне", "дельта"])

i = 0
while True:
    if error <= E:
        break
    else:
        df = df.append({"y модельне": y_m_2, "дельта": error}, ignore_index=True)

        q_3_2 = y_m_2 * (1 - y_m_2) * (y - y_m_2)

        b_3_2 = q_3_2 * y_m_1
        b_3_2_0 = x0 * q_3_2  # типо сами в себя

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
        y_m_1 = np.array(list(map(find_f, total_1)))

        total_2 = y_m_1.dot(w_2_3) + w_0_2
        y_m_2 = find_f(total_2[0][0])

        error = find_error(y_m_2, y)
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
print("y_m = " + str(recognition([1.1, 1.4], w_1_2, w_2_3)))
