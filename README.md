A contrast-based autofocus algorithm employing various techniques
pertinent to MTE 204 - Numerical Methods

by Yun-Ha Jung, Ruoyu Jessen Liang and Russell Wong

This library of code contains all Python scripts that were developed
for this project, including scripts that were tested during the development
stage but not used for the final implementation of the autofocus algorithm.
For more information regarding the important functions for the finalized
algorithm, see Appendix B in the report, "Development of a Contrast-Based
Autofocus Algorithm using Numerical Methods"

The main function is contained within golden_section.py. The algorithmic steps
are as follows:

1) Load image data and focus distance data based on a subject number
   and calculate sharpness for each image (sharpness_calc.py)
2) Set up a system of equations for determining a set of cubic functions
   to approximate the sharpness curve as a function of focus distance
   (cubic_spline.py)
3) Solve this system of equations using Gaussian Elimination (gaussian_elimination.py),
   thereby calculating the required coefficients for cubic spline interpolation
4) Approximate the maximum of this cubic spline function using the Golden Section
   Method, which will identify a maximum sharpness value corresponding to an optimal
   focus distance (golden_section.py)

Algorithmic details can be found in the report, "Development of a Contrast-Based 
Autofocus Algorithm using Numerical Methods"  