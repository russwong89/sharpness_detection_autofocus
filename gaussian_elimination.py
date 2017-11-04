'''
@name    gaussian_elimination.py
@brief   Solves a system of linear equations in the form
         [A]{x} = {b} using Gaussian Elimination with
         partial pivoting
@author  Russell Wong, Yun-Ha Jung 2017
'''

import sys, os, math, cv2
import numpy as np

import img_util, cubic_spline

def solve(A, b):
    # Initialize variables for size of array and x vector
    n = len(b)
    x = np.zeros((n,1))

    ###########################
    ###  Elimination stage  ###
    ###########################
    # Iterate through rows of A
    for i in range(n-1):
        # Implement partial pivoting
        # Find max value in current column and swap with the top
        pivoting_element = A[i][i]
        pivoting_index = i
        for row_index in range(i+1,n):
            if abs(A[row_index][i]) > abs(pivoting_element):
                pivoting_element = A[row_index][i]
                pivoting_index = row_index
        if pivoting_index != i:
            # Swap rows
            temp = list(A[i])
            A[i] = list(A[pivoting_index])
            A[pivoting_index] = list(temp)
            temp = list(b[i])
            b[i] = list(b[pivoting_index])
            b[pivoting_index] = list(temp)
        # Iterate through rows of A beneath current row
        for row_index in range(i+1,n):
            # Calculate f factor
            f = A[row_index][i] / A[i][i]
            # Iterate through columns of A greater than or equal to current row index and subtract
            for col_index in range(i,n):
                A[row_index][col_index] = A[row_index][col_index] - f*A[i][col_index]
            # Update b vector
            b[row_index] = b[row_index] - f*b[i]

    ###########################
    ###  Back substitution  ###
    ###########################
    for i in range(n-1, -1, -1):
        # Initialize x[i] to b[i]
        x[i] = b[i]

        # Loop through every column from the left   
        for j in range(i,n):
            # Subtract all elements from x[i] except for itself
            if i != j:
                x[i] -= A[i][j]*x[j]
        # Divide x[i] by the coefficient in the matrix
        x[i] /= A[i][i]

    return x


#######################
###  Main Function  ###
#######################
if __name__ == '__main__':
    sample_points = [(0,0),(1,3),(2,1),(4,5)]
    A,b = cubic_spline.getAMatrixAndBVector(sample_points)
    print A
    print b
    x = solve(A,b)
    print x
    sys.exit()