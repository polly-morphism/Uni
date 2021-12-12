import numpy as np
import math
import pandas as pd

np.random.seed(70)


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


def find_rand_w(n):
	w_rand = np.random.uniform(0, 1, n)
	w = []
	for i in range(n):
		w.append(w_rand[i])
	return np.array(w)


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


def learn_algorythm(x, y, w_12, w_01, w_23, w_02):
	total_1 = x.dot(w_12)
	# vector x*w of the first hidden layer values

	total_1 = total_1 + w_01
	# vector y_molule of the first hidden layer

	y_m_1 = np.array(list(map(find_f, total_1)))

	total_2 = y_m_1.dot(w_23) + w_02

	# final y_molule of the first hidden layer
	y_m_2 = find_f(total_2[0][0])

	error = find_error(y_m_2, y)

	w01, w12, w02, w23 = find_new_w(x, y, y_m_2, y_m_1, w_12, w_01, w_23, w_02)

	return y_m_2, error, np.array(w12), np.array(w01), w23, w02


X = np.array([[1., 1.], [2., 1.], [1.5, 1.5], [1., 2.5]])  # input vector
Y = np.array([0.02, 0.03, 0.03, 0.035])
x0 = 1

n_epohs = 1000


def online_learning(X, Y, n_epohs):
	w_1_2 = [find_rand_w(3), find_rand_w(3)]
	w_0_1 = [find_rand_w(3)]

	w_2_3 = [find_rand_w(1), find_rand_w(1), find_rand_w(1)]
	w_0_2 = find_rand_w(1)

	n = 0
	while n <= n_epohs:
		y_model_n = []
		error_n = []
		for i in range(len(Y)):
			y_m_2, error, w_1_2, w_0_1, w_2_3, w_0_2 = learn_algorythm(X[i], Y[i], w_1_2, w_0_1, w_2_3, w_0_2)
			y_model_n.append(y_m_2)
			error_n.append(error)
		if n % 100 == 0:
			print("\n Epoch  #{}".format(n))
			print("Y modeled: {}".format(y_model_n))
			print("Delta {}".format(error_n))
		n += 1
	return w_1_2, w_0_1, w_2_3, w_0_2


w_1_2, w_0_1, w_2_3, w_0_2 = online_learning(X, Y, n_epohs)


def recognition_func(x, w_12, w_01, w_23, w_02):
	total_1 = x.dot(w_12)
	# vector x*w of the first hidden layer values

	total_1 = total_1 + w_01
	# vector y_molule of the first hidden layer

	y_m_1 = np.array(list(map(find_f, total_1)))

	total_2 = y_m_1.dot(w_23) + w_02

	# final y_molule of the first hidden layer
	y_m_2 = find_f(total_2[0][0])

	return y_m_2


print('\nRecognition part')
print('x = {}'.format([1., 1.5]))
print('y = {}'.format(recognition_func(np.array([1., 1.5]), w_1_2, w_0_1, w_2_3, w_0_2)))
