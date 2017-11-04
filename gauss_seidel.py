'''
@name    gauss_seidel.py
@brief   Solve for the coefficients ai, bi, ci, di
		 to define cubic spline
		 This script is disabled due to special cases
		 where there are 0's in the A matrix and the
		 target xi will be divided by 0
@author  Yun-Ha Jung, 2017
'''

import sys, os, math
import numpy as np

import img_util, cubic_spline

def gsSolve(A, b, xi, err=0.1):
	# Initialize variables for size of array and x vector
    n = len(b)
    delta_x = np.zeros((n,1))
    calc_err = err+1

    # Copy the initial guess vector
    xnew = list(xi)

    while (calc_err > err):
    	for i in range(n):
    		xnew[i] = b[i]

    		for j in range(n):
    			if j == i:
    				continue

    			xnew[i] -= A[i][j]*xnew[j]

    		xnew[i] /= A[i][i]

    	for k in range(n):
    		delta_x = abs(xnew[k] - xi[k])

    	norm_delta_x = np.linalg.norm(delta_x)
    	norm_xold = np.linalg.norm(xi)

    	calc_err = norm_delta_x/norm_xold
    	xi = list(xnew)

    return xnew

if  __name__ == "__main__":

	sample_points = [(0,0),(1,3),(2,1),(4,5)]
	A,b = cubic_spline.getAMatrixAndBVector(sample_points)
	xi = np.ones((len(b),1))
	print A
	print b
	x = gsSolve(A,b,xi)
	print x
	sys.exit()

