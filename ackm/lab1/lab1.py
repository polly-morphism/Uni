import numpy as np
from scipy.linalg import solve
from prettytable import PrettyTable

A = np.array([
	[0.31, 0.14, 0.30, 0.27],
	[0.26, 0.32, 0.18, 0.24],
	[0.61, 0.22, 0.20, 0.31],
	[0.40, 0.34, 0.36, 0.17]
	])
	
b = np.array([1.02, 1.00, 1.34, 1.27]).reshape((4, 1))


def view_matrix(matrix):
	table = PrettyTable(header=False)
	table.add_rows(matrix)
	print(table)

	return None

def check_rank(matrix):
	rank = np.linalg.matrix_rank(matrix)
	shape = matrix.shape[0]

	if rank == shape:
		print("Ранг матриці є повним та дорівнює {}\n".format(rank))
		return True

	else:
		print("Ранг матриці є невпоним")
		return False

def get_det(matrix):
	det = np.linalg.det(matrix)

	if det != 0:
		print("Матриця є навиродженою та її визначник дорівнює {}\n".format(det))
		return True

	else:
		print("Матриця є виродженою")
		return False


if __name__ == "__main__":
	
	print("\nМатриця А:")
	view_matrix(A)
	print("\nВектор вільних членів b:")
	view_matrix(b)

	if check_rank(A) and get_det(A):
		x = solve(A, b)
		print("Розв'язок:")
		table = PrettyTable(header=False)
		table.add_rows([x])
		print(table)
		print("\nA * x = ") 
		print(np.dot(A, x).reshape((4,1)))
