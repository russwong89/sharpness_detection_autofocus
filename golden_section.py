'''
@name	golden_section.py
@brief	Main file for finding the optimum of the given function
@author	Yun-Ha Jung, Russell Wong, 2017
'''
import sys, os, math

import sharpness_calc, cubic_spline, gaussian_elimination, img_util

REQ_ERR = 0.01
GR = (math.sqrt(5) - 1)/2

# test function for testing the functionality
def testFunction(x):
	return (-x**3) + (5*x) + 6


'''
@name		evaluateCubicSharpnessFunction
@brief		Calculates an estimated sharpness value based on
            cubic splines
@param[in]	x: The distance value at which the sharpness function should be evaluated
			coefficients: A vector of a,b,c,d coefficients representing each cubic function in the spline
			x_vals: A vector of distance values corresponding to the endpoints of each cubic function in the spline
@return 	float: The calculated sharpness value
'''

def evalCubicSharpnessFunction(x,coefficients,x_vals):
	# Initialize right, left, and middle indices
	right_index = len(x_vals)-1
	left_index = 0
	middle_index = int(math.ceil((left_index+right_index)/2.0))

	# Loop until the index where the x value belongs (binary search)
	while (x > x_vals[middle_index] or x < x_vals[middle_index-1]):
		if (middle_index == 0):
			print "Could not find x=%f with bounds of x_vals (%f,%f)!\n" % (x, x_vals[0], x_vals[len(x_vals)-1])
			return -1
		if (x > x_vals[middle_index]):
			left_index = middle_index
		elif (x < x_vals[middle_index-1]):
			right_index = middle_index-1
		middle_index = int(math.ceil((left_index+right_index)/2.0))

	# Extract the appropriate cubic coefficients
	a = coefficients[4*(middle_index-1)]
	b = coefficients[4*(middle_index-1)+1]
	c = coefficients[4*(middle_index-1)+2]
	d = coefficients[4*(middle_index-1)+3]

	return a*x**3 + b*x**2 + c*x + d


def evaluateSharpnessFunction(x, coefficients, x_vals):
	# Find left and right bounds of x from x_vals
	# Use a binary search
	right_index = len(x_vals)-1
	left_index = 0
	middle_index = int(math.ceil((left_index+right_index)/2.0))
	while (x > x_vals[middle_index] or x < x_vals[middle_index-1]):
		if (middle_index == 0):
			print "Could not find x=%f with bounds of x_vals (%f,%f)!\n" % (x, x_vals[0], x_vals[len(x_vals)-1])
			return -1
		if (x > x_vals[middle_index]):
			left_index = middle_index
		elif (x < x_vals[middle_index-1]):
			right_index = middle_index-1
		middle_index = int(math.ceil((left_index+right_index)/2.0))

	# Extract the appropriate cubic coefficients
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
	# Since golden ratio has a larger percentage than 50%,
	# x1 is going to be closer to upper bound and 
	# x2 will be closer to lower bound
	d = GR*abs(xup-xlow)
	x1 = xlow + d
	x2 = xup - d

	# Infinite loop to find the optimum of a function
	# Break the loop when the calculated error is smaller than REQ_ERR
	while(True):
		# Calculate new distance
		d = GR*d

		# Calculate y values for given x1 and x2 values
		y1 = evalCubicSharpnessFunction(x1,coefficients,x_vals)
		y2 = evalCubicSharpnessFunction(x2,coefficients,x_vals)
		# print "X1: %f Y1: %f X2: %f Y2: %f\n" % (x1, y1, x2, y2)

		# Compare y1 and y2, if y1 is greater than y2 
		# it means that the optimum falls between x2-xup range
		# therefore all the x values from xlow to x2 can be eliminated
		if (y1 >= y2):
			max_err = max(abs(xup-x1), abs(x1-x2))
			if (max_err < REQ_ERR):
				optimum = (x1,y1)
				break

			# x2 becomes new lower bound
			xlow = x2
			# Calculate new x1 and x2
			x1 = xlow + d
			x2 = xup - d

		# Compare y1 and y2, if y2 is greater than y1
		# it means that the optimum falls between x1-xlow range
		# therefore all the x values from x1 to xup can be eliminated
		elif (y2 > y1):
			max_err = max(abs(x1-x2), abs(x2-xlow))
			if (max_err < REQ_ERR):
				optimum = (x2,y2)
				break

			# x1 becomes new upper bound
			xup = x1
			# Calculate new x1 and x2
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
		points = sharpness_calc.getPoints(subject_name, show_images=False)
	else:
		points = sharpness_calc.getPoints()
	print points

	# Get A matrix and b vector required to solve for coefficients of cubicratic spline
	A,b = cubic_spline.getAMatrixAndBVector(points)

	# Solve for coefficients using Gaussian Elimination
	coefficients = gaussian_elimination.solve(A,b)
	x_vals = [p[0] for p in points]

	# Find the optimum sharpness and focus distance using Golden-Section 
	opt = findOptimum(x_vals[0],x_vals[len(x_vals)-1],coefficients,x_vals)
	print 'X: %f, Y: %f' % (opt[0], opt[1])
	img_util.plotCubic(coefficients, x_vals, 'Cubic Spline for Subject #' + subject_name, opt[0], opt[1])
