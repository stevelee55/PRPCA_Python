import numpy

class OptShrink(object):


	# Data-Driven estimate of optimal shrinkage.
	# See Algorithm 1 of [1] for details.
	def optimalShrinkage(s, m, n, r)

	# Initializer for the this class' instance.
	def __init__(self):
		print("OptShrink is created!")


	def OptShrink_Main(self, Y, r):

		# Parsing inputs.
		m, n = numpy.array(Y).shape

		# Compute SVD.
		U,S,V = numpy.linalg.svd(Y, full_matrices=False)

		# Optimal Shrinkage.
		sX, MSE, RMSE = optimalShrinkage(sY, m, n, r)



