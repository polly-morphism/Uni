import numpy as np


def f(x):
    return 3 * (x[0] - 2) * (x[0] - 2) - x[0] * x[1] + 4 * x[1] * x[1]


def H_f(x):
    return np.array([[6, -1], [-1, 8]])


x0 = np.array([-6.4, -6.4])


def nabla_f(x):
    return np.array([6 * x[0] - x[1] - 12, -x[0] + 8 * x[1]])


def lmbd(x, s):
    print(f"Calculating lambda")
    l = -((nabla_f(x).transpose()).dot(s)) / ((s.transpose().dot(H_f(x))).dot(s))
    print(f"\t llambda=-nabla_f(x).transpose().dot(s)/s.transpose().dot(H_f(x)).dot(s)")
    print(
        f"\t lambda=-({nabla_f(x).transpose()}*{s})/({s.transpose()}*{H_f(x)}*{s}) = {l}"
    )
    return l


A0 = np.array([[1, 0], [0, 1]])

x = x0
print(f"nabla_f(X) = {nabla_f(x)}")
print(f"||nabla_f(X)|| = {np.linalg.norm(nabla_f(x))}")
i = 0
print(f"Iter {i+1}\nfind direction and step size")

s = -A0.dot(nabla_f(x))
print(f"s={s}")

l = lmbd(x, s)


def new_x(x0, l, s):
    x1 = x0 + l * s
    print(f"Calculate new x")
    print(f"\tx1 =x0+l*s")
    print(f"\tx1 ={x}+{l}*{s}")
    print(f"\tx1={x1}")
    return x1


x1 = new_x(x0, l, s)

print(f"nabla_f(X) = {nabla_f(x1)}")
print(f"||nabla_f(X)|| = {np.linalg.norm(nabla_f(x1))}\n")


def new_dx(x1, x0):
    dx = x1 - x0
    print("Calculate new dx")
    print(f"\tdx=x1-x0")
    print(f"\tdx={x1}-{x0}")
    print(f"\tdx={dx}\n")
    return dx


print("Iteration 2")
dx = new_dx(x1, x0)


def new_dg(x1, x0):
    dg = nabla_f(x1) - nabla_f(x0)
    print(f"dg=nabla_f(x1)-nabla_f(x0)")
    print(f"dg={nabla_f(x1)}-{nabla_f(x0)}={dg}\n")
    return dg


dg = new_dg(x1, x0)


def new_A(A0, dx, dg):
    A1 = (
        A0
        + dx.dot(dx.transpose()) / (dx.transpose()).dot(dg)
        - ((A0.dot(dg)).dot(dg.transpose())) * (A0) / ((dg.transpose()).dot(A0)).dot(dg)
    )
    print("Calc new A")
    print(
        f"\tA1=A0+ dx.dot(dx.transpose())/(dx.transpose()).dot(dg)-((A0.dot(dg)).dot(dg.transpose()))*(A0)/((dg.transpose()).dot(A0)).dot(dg)"
    )
    print(
        f"\tA1={A0}+\n\t+ ({dx}*{dx.transpose()})/({dx.transpose()}*{dg})-\n\t-({A0}*{dg}*{dg.transpose()}*{A0})/({dg.transpose()}*{A0}*{dg})=\n\t={A1}"
    )
    return A1


A1 = new_A(A0, dx, dg)


l = lmbd(x1, s)

print(f"l={l}")


s1 = -A1.dot(nabla_f(x1))
print("s1 = ", s1)

x2 = new_x(x1, l, s1)

print("x2 = ", x2)

print(f"nabla_f(X) = {nabla_f(x2)}")
print(f"||nabla_f(X)|| = {np.linalg.norm(nabla_f(x2))}")

print("H = ", H_f(x2))

print("H-1 = ", np.linalg.inv(H_f(x2)))
