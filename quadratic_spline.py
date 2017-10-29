'''
@name    quadratic_spline.py
@brief   Determines appropriate matrices and vectors
         in the form [A]{x} = {b} required to solve for
         the coefficients of several quadratic functions
         in a quadratic spline given n points of a function
@author  Russell Wong, 2017
'''

import sys, os, math, cv2
import numpy as np

import img_util

# Assumes points are ordered by x-value
def getAMatrixAndBVector(points):
    if len(points) <= 1:
        print 'Not enough points!\n'
        return [[],[]]

    # Extract x and y values
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    print x
    print y
    # For N data points, we will be solving for 3*(N-1) unknowns
    #   There are N-1 parabolas required to be fit in the splines, and
    #   three unknowns a,b and c for each parabola, where a parabola is
    #   defined as ax^2 + bx + c
    # Set n = N - 1
    n = len(x) - 1
    # Initalize 3*n x 3*n matrix, A (since we require a system of 3*n equations)
    A = np.zeros((3*n,3*n))
    # Initialize 3*n length vector, b
    b = np.zeros((3*n,1))

    # Iterate through rows of A (which is equal to the rows of b)
    
    # The first 2*n rows pertain to the known points in relation to each parabola
    # E.g. x[0]^2 * a0 + x[0] * b0 + 1 * c0 = y[0]    
    row_count = 0
    while (row_count < 2*n):
        A[row_count][3*row_count/2] = x[row_count/2]**2
        A[row_count][3*row_count/2+1] = x[row_count/2]
        A[row_count][3*row_count/2+2] = 1
        b[row_count] = y[row_count/2]

        A[row_count+1][3*row_count/2] = x[row_count/2+1]**2
        A[row_count+1][3*row_count/2+1] = x[row_count/2+1]
        A[row_count+1][3*row_count/2+2] = 1
        b[row_count+1] = y[row_count/2+1]

        row_count += 2

    # The equations for the next n-1 rows are derived from the fact that
    # the first derivative is continuous (so at internal points, the derivative
    # of the left parabola subtracted by the derivative of the right parabola evaluated
    # at the internal point is equal to 0)
    # E.g. 2*x[1]*a0 + b0 - 2*x[2]*a1 - b1 = 0
    while (row_count < 3*n-1):
        A[row_count][3*(row_count-2*n)] = 2*x[row_count-2*n+1]
        A[row_count][3*(row_count-2*n)+1] = 1
        A[row_count][3*(row_count-2*n)+3] = -2*x[row_count-2*n+1]
        A[row_count][3*(row_count-2*n)+4] = -1
        # No need to update b because all equations are equal to 0
        row_count += 1

    # The last row is defined such that a0 = 0
    A[row_count][0] = 1
    # No need to update b because the equation is equal to 0

    return A,b

if __name__ == '__main__':
    sample_points = [(0,0),(1,3),(2,1),(4,5)]
    A,b = getAMatrixAndBVector(sample_points)
    print A
    print b
    img_util.plotPoints(sample_points, 'Points')
    sys.exit()