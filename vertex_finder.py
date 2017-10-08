'''
@name	vertex_finder.py
@brief	find vertex of the quadratic equation defined
@author	Yun-Ha Jung, 2017
'''

import sys, os, math
import sharpness_calc as sc

'''
@name		define_quad
@brief		find coefficients (a, b, and c) of quadratic equation
@param[in]	point1: x0 and f(x0) of first point
			point2: x1 and f(x1) of second point
			point3: x2 and f(x2) of third point
@return 	coeffs: an array of a, b, and c values calculated using given 3 points
'''
def define_quad( point1, point2, point3 ):
	# assign point values
	x0 = point1[0]
	fx0 = point1[1]

	x1 = point2[0]
	fx1 = point2[1]

	x2 = point3[0]
	fx2 = point3[1]

	# calculate b values
	b0 = fx0
	b1 = (fx1 - fx0) / (x1 - x0)
	b2 = (((fx2 - fx1) / (x2 - x1)) - b1) / (x2 - x0)

	# calculate coefficients of quadratic quation
	a0 = b0 - b1*x0 + b2*x0*x1
	a1 = b1 - b2*x0 - b2*x1
	a2 = b2

	# return coeffs array created
	coeffs = [a0, a1, a2]
	return coeffs


'''
@name		find_roots
@brief		find roots of quadratic equation
@param[in]	coefficients: an array of coefficients of a quadratic equation
@return 	roots: an array of roots caculated using given quadratic equation
'''
def find_roots( coefficients ):
	# assign values in coefficients array to a, b, and c
	a = coefficients[2]
	b = coefficients[1]
	c = coefficients[0]

	# calculate roots
	p_root = (-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
	n_root = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)

	# return roots
	roots = [p_root, n_root]
	return roots


#######################
###  Main Function  ###
#######################
if __name__ == '__main__':

	#if( len(sys.argv) == 1 ):
	#	print 'Please specify the subject name'
	#	sys.exit()

	if ( len( sys.argv ) > 1 ):
		arguments = str(sys.argv)
		subject_name = arguments[1]
		points = sc.getPoints(subject_name)
	else:
		points = sc.getPoints()

	point1 = points[0]
	point2 = points[1]
	point3 = points[2]

	print 'Point 1 = (%f, %f) \n Point 2 = (%f, %f) \n Point 3 = (%f, %f)' \
			% (point1[0], point1[1], point2[0], point2[1], point3[0], point3[1])

	quad_eq = define_quad(poin1, point2, point3)

	print 'Coefficients of quadratic equation: \n a = %f \n b = %f \n c = %f' \
			% (quad_eq[2], quad_eq[1], quad_eq[0])

	roots = find_roots(quad_eq)
	print 'Roots of calculated quadratic equation are: %f, %f' % (roots[0], roots[1])

	x_vertex = (roots[0] + roots[2]) / 2

	print 'Focusing distance of quadratic equation defined is: %f' % (x_vertex)

	sys.exit()