'''
@name	golden_section.py
@brief	Main file for finding the optimum of the given function
@author	Yun-Ha Jung, Russell Wong, 2017
'''
import sys, os, math

import sharpness_calc, quadratic_spline, gaussian_elimination

REQ_ERR = 0.01
GR = (math.sqrt(5) - 1)/2

# test function for testing the functionality
def testFunction(x):
	return (-x**3) + (5*x) + 6


'''
@name		evaluateSharpnessFunction
@brief		Calculates an estimated sharpness value based on
            quadratic splines
@param[in]	x: The distance value at which the sharpness function should be evaluated
			coefficients: A vector of a,b,c coefficients representing each parabola in the spline
			x_vals: A vector of distance values corresponding to the endpoints of each parabola in the spline
@return 	float: The calculated sharpness value
'''
def evaluateSharpnessFunction(x, coefficients, x_vals):
	# Find left and right bounds of x from x_vals
	# Use a binary search
	right_index = len(x_vals)-1
	left_index = 0
	middle_index = int((left_index+right_index)/2)
	while (x > x_vals[middle_index] or x < x_vals[middle_index-1]):
		if (middle_index == 0):
			print "Could not find x=%f with bounds of x_vals (%f,%f)!\n" % (x, x_vals[0], x_vals[len(x_vals)-1])
			return -1
		if (x > x_vals[middle_index]):
			left_index = middle_index
		elif (x < x_vals[middle_index-1]):
			right_index = middle_index-1
		middle_index = int((left_index+right_index)/2)

	# Extract the appropriate quadratic coefficients
	a = coefficients[3*(middle_index-1)]
	b = coefficients[3*(middle_index-1)+1]
	c = coefficients[3*(middle_index-1)+2]

	return a*x**2 + b*x + c

	


'''
@name		findOptimum
@brief		find optimum point (x,y) of the given function
@param[in]	xlow: lower bound of the range where the optimum is
			xup: upper bound of the range where the optimum is
			coefficients: A vector of a,b,c coefficients representing each parabola in the spline
			              (used for sharpness calculations)
			x_vals: A vector of distance values corresponding to the endpoints of each parabola in the spline
				    (used for sharpness calculations)
@return 	optimum: the optimum point (x,y)
'''
def findOptimum(xlow, xup, coefficients, x_vals):
	optimum = (0,0)
	
	# Calculate distance to define x1 and x2
	d = GR*abs(xup-xlow)
	x1 = xlow + d
	x2 = xup - d

	# Infinite loop to find the optimum of a function
	# Break the loop then the calculated error is smaller than REQ_ERR
	while(True):
		# Calculate new distance
		d = GR*d

		# Calculate y values for given x1 and x2 values
		y1 = evaluateSharpnessFunction(x1,coefficients,x_vals)
		y2 = evaluateSharpnessFunction(x2,coefficients,x_vals)

		if (y1 >= y2):
			max_err = max(abs(xup-x1), abs(x1-x2))
			if (max_err < REQ_ERR):
				optimum = (x1,y1)
				break
			xlow = x2
			x1 = xlow + d
			x2 = xup - d

		elif (y2 > y1):
			max_err = max(abs(x1-x2), abs(x2-xlow))
			if (max_err < REQ_ERR):
				optimum = (x2,y2)
				break
			xup = x1
			x1 = xlow + d
			x2 = xup - d

	return optimum


#######################
###  Main Function  ###
#######################
if __name__ == '__main__':
	# Find (distance, sharpness) data points for a given set of images
	if len(sys.argv) > 1:
		subject_name = sys.argv[1]
		print subject_name
		points = sc.getPoints(subject_name, show_images=False)
	else:
		points = sc.getPoints()

	# Get A matrix and b vector required to solve for coefficients of quadratic spline
	A,b = quadratic_spline.getAMatrixAndBVector(points)

	# Solve for coefficients using Gaussian Elimination
	coefficients = gaussian_elimination.solve(A,b)
	x_vals = [p[0] for p in points]

	# Find the optimum sharpness and focus distance using Golden-Section 
	opt = findOptimum(-5,5,coefficients,x_vals)
	print 'X: %f, Y: %f' % (opt[0], opt[1])