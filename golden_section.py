'''
@name	golden_section.py
@brief	Main file for finding the optimum of the given function
@author	Yun-Ha Jung, 2017
'''
import sys, os, math

REQ_ERR = 0.01
GR = (math.sqrt(5) - 1)/2

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