import plotly.graph_objs as go
import numpy as np
import math
import mpmath
import functools as ft

def Lagrange(x,y,t):
	z=0
	for j in range(len(y)):
		p1=1; p2=1
		for i in range(len(x)):
			if i==j:
				p1=p1*1; p2=p2*1   
			else: 
				p1=p1*(t-x[i])
				p2=p2*(x[j]-x[i])
		z=z+y[j]*p1/p2
	return z



def get_max_of_error(x_points, max_of_abs_n_diff):

    curr_point = x_points[0]
    points_number = 100
    step = (x_points[-1] - x_points[0])/points_number
    max_error = -math.inf

    while curr_point <= x_points[-1]:

        differences = list(map(lambda x: abs(curr_point - x), x_points))
        mult_differences = ft.reduce(lambda x, y: x/2 + y/2, differences)
        max_error = max(max_error, max_of_abs_n_diff *
                        mult_differences)
        curr_point += step

    return max_error

class Newton(object):
	def __init__(self, x, y):
	    self.x = x
	    self.y = y

	def newton(self, tmp_x):
	    table = np.zeros([len(self.x), len(self.x) + 1], dtype=float)

	    for i in range(len(self.x)):
	        table[i][0] = self.x[i]
	        table[i][1] = self.y[i]
	    for i in range(2, table.shape[1]):  
	        for j in range(i - 1, table.shape[0]):
	            table[j][i] = (table[j][i - 1] - table[j - 1][i - 1]) / (self.x[j] - self.x[j - i + 1])

	    tmp_y = []
	    for ans_x in tmp_x:
	        ans_y = 0  
	        for i in range(table.shape[0]):
	            tmp = table[i][i + 1]  
	            for j in range(i):
	                tmp *= (ans_x - self.x[j])
	            ans_y += tmp
	        tmp_y.append(ans_y)
	    return tmp_y

def plot_interpolation():
	answer = input('Method (type 1 or 2): ')
	x=np.array([-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3], dtype=float)
	y=np.array([1.4918, 1.8221, 2.2255, 2.7183, 3.3201, 4.0552, 4.9530], dtype=float)

	if answer == '1':
		xnew=np.linspace(np.min(x),np.max(x),100)
		ynew=[Lagrange(x,y,i) for i in xnew]
		print(f"Precision: {get_max_of_error(x, 0.002)}")
		fig = go.Figure()
		fig.add_trace(go.Scatter(x=xnew, y=ynew, name='Function'))
		fig.add_trace(go.Scatter(x=x, y=y, name='Interpolation (Lagrange)'))
		fig.update_layout(
			    title="Lagrange method",
			    xaxis_title="x",
			    yaxis_title="y",
			    font=dict(
			        family="Courier New, monospace",
			        size=18,
			        color="RebeccaPurple"
			    )
			)
		fig.show()

	elif answer == '2':
		s = Newton(x, y)
		xnew=np.linspace(np.min(x),np.max(x),100)
		ynew=s.newton(xnew)
		print(f"Precision: {get_max_of_error(x, 0.002)}")
		fig = go.Figure()
		fig.add_trace(go.Scatter(x=xnew, y=ynew, name='Function'))
		fig.add_trace(go.Scatter(x=x, y=y, name='Interpolation (Newtone)'))
		fig.update_layout(
			    title="Newton method",
			    xaxis_title="x",
			    yaxis_title="y",
			    font=dict(
			        family="Courier New, monospace",
			        size=18,
			        color="RebeccaPurple"
			    )
			)
		fig.show()

plot_interpolation()

