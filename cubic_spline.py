'''
@name    cubic_spline.py
@brief   Determines appropriate matrices and vectors
         in the form [A]{x} = {b} required to solve for
         the coefficients of several cubic functions
         in a cubic spline given N points of a function
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

    # For N data points, we will be solving for 4*(N-1) unknowns
    #   There are N-1 cubic functions required to be fit in the splines, and
    #   four unknowns a,b c and d for each cubic function, where a cubic function is
    #   defined as ax^3 + bx^2 + cx + d
    # Set n = N - 1
    n = len(x) - 1

    # Initalize 4*n x 4*n matrix, A (since we require a system of 4*n equations)
    A = np.zeros((4*n,4*n))
    # Initialize 4*n length vector, b
    b = np.zeros((4*n,1))

    # Iterate through rows of A (which is equal to the rows of b)
    
    # The first 2*n rows pertain to the known points in relation to each cubic function
    # E.g. x[0]^3*a0 + x[0]^2*b0 + x[0]*c0 + 1*d0 = y[0]    
    row_count = 0
    while (row_count < 2*n):
        A[row_count][4*row_count/2] = x[row_count/2]**3
        A[row_count][4*row_count/2+1] = x[row_count/2]**2
        A[row_count][4*row_count/2+2] = x[row_count/2]
        A[row_count][4*row_count/2+3] = 1
        b[row_count] = y[row_count/2]

        A[row_count+1][4*row_count/2] = x[row_count/2+1]**3
        A[row_count+1][4*row_count/2+1] = x[row_count/2+1]**2
        A[row_count+1][4*row_count/2+2] = x[row_count/2+1]
        A[row_count+1][4*row_count/2+3] = 1
        b[row_count+1] = y[row_count/2+1]

        row_count += 2

    # The equations for the next n-1 rows are derived from the fact that
    # the first derivative is continuous (so at internal points, the derivative
    # of the left cubic subtracted by the derivative of the right cubic evaluated
    # at the internal point is equal to 0)
    # E.g. 3*x[1]^2*a0 + 2*x[1]*b0 + c0 - 3*x[1]^2*a1 - 2*x[1]*b1 - c1 = 0
    while (row_count < 3*n-1):
        A[row_count][4*(row_count-2*n)] = 3*x[row_count-2*n+1]**2
        A[row_count][4*(row_count-2*n)+1] = 2*x[row_count-2*n+1]
        A[row_count][4*(row_count-2*n)+2] = 1

        A[row_count][4*(row_count-2*n)+4] = -3*x[row_count-2*n+1]**2
        A[row_count][4*(row_count-2*n)+5] = -2*x[row_count-2*n+1]
        A[row_count][4*(row_count-2*n)+6] = -1

        # No need to update b because all equations are equal to 0
        row_count += 1

    # The equations for the next n-1 rows are derived from the fact that
    # the second derivative is continuous (so at internal points, the second derivative
    # of the left cubic subtracted by the second derivative of the right cubic evaluated
    # at the internal point is equal to 0)
    # E.g. 6*x[1]*a0 + 2*b0 - 6*x[1]*a1 - 2*b1 = 0
    while (row_count < 4*n-2):
        A[row_count][4*(row_count-(3*n-1))] = 6*x[row_count-(3*n-1)+1]
        A[row_count][4*(row_count-(3*n-1))+1] = 2

        A[row_count][4*(row_count-(3*n-1))+4] = -6*x[row_count-(3*n-1)+1]
        A[row_count][4*(row_count-(3*n-1))+5] = -2

        # No need to update b because all equations are equal to 0        
        row_count += 1

    # The last 2 rows are defined such that the second derivatives at the endpoints are 0
    A[row_count][0] = 6*x[0]
    A[row_count][1] = 2
    A[row_count+1][4*n-4] = 6*x[n]
    A[row_count+1][4*n-3] = 2
    # No need to update b because the equation is equal to 0

    return A,b

if __name__ == '__main__':
    sample_points = [(0,0),(1,3),(2,1),(4,5)]
    A,b = getAMatrixAndBVector(sample_points)
    print A
    print b
    img_util.plotPoints(sample_points, 'Points')
    sys.exit()