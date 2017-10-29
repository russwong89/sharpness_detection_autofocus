'''
@name	golden_section.py
@brief	find optimum of the given function
@author	Yun-Ha Jung, 2017
'''
import sys, os, math
'''
	Pseudo Code
	1. get 2 initial points xl and xu, (xlow, ylow) and (xup, yup), and the function defined using quadratic spline
	2. calculate x1 and x2 using golden ratio ((sqrt(5) - 1)/2)*(xup-xlow)
		x1 = xlow + distance
		x2 = xup - distance
	3. while calc_err > req_err
		distance = ratio*distance
		calculate y1 and y2 using the given function
		if y1 > y2
			calculate max err
			if max error less than required err
				optimum = x1
				break the loop
		 	xlow = x2
		 	x2 = xu - distance
			x1 = xl + distance
		   
		else if y2 > y1
			calculate max error
			if max error less than required err
				optimum = x2
				break the loop
			xup = x1
			x2 = xu - distance
			x1 = xl + distance
'''
REQ_ERR = 0.01

# test function for testing the functionality
def testFunction(x):
	return (-x**3) + (5*x) + 6

'''
@name		findOptimum
@brief		find optimum point (x,y) of the given function
@param[in]	xlow: lower bound of the range where the optimum is
			xup: upper bound of the range where the optimum is
@return 	optimum: the optimum point (x,y)
'''

def findOptimum(xlow, xup):
	optimum = (0,0)
	R = (math.sqrt(5) - 1)/2
	d = R*abs(xup-xlow)
	x1 = xlow + d
	x2 = xup - d

	while(True):
		d = R*d
		y1 = testFunction(x1)
		y2 = testFunction(x2)

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
	opt = findOptimum(-5,5)
	print 'X: %f, Y: %f' % (opt[0], opt[1])