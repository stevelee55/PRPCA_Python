import numpy

class OptShrink(object):


	# Data-Driven estimate of optimal shrinkage.
	# See Algorithm 1 of [1] for details.
	def optimalShrinkage(s, m, n, r):
		# Parse inputs.
		q = min(m, n)

		# Signal singular values.
		# It's getting the very first value.
		ss = s[0][r]

		# Noise singular values.
		sn2 = numpy.power(s[r + 1][q], 2) # Column Vector.
		pressH = [sn2, numpy.zeros(m - q, 1)]
		ssH = pressH.getH() # Test this. Row vector.
		presHs = [sn2, numpy.zeros(n - q, 1)]
		sHs = presHs.getH()

		ss2 = numpy.power(ss, 2)
		# "Broadcasting in Matlab has to be done in a specific way, where as in Python, it's automatic." 
		ss2mssH = ss2 - ssH
		ss2msHs = ss2 - sHs
		s1oss2mssH = sum(numpy.divide(1, ss2mssH), 2)
		s1oss2msHs = sum(numpy.divide(1, ss2msHs), 2)
	# Watch out for precision dropping. Check and see if matlab drops the precision.
		phimss = numpy.multiply((ss / (m - r)), s1oss2mssH)
		phinss = numpy.multiply((ss / (n - r)), s1oss2msHs)
		Dss = numpy.multiply(phimss, phinss)

		# Numerical approximation of D transform derivative. 
	# Check for the precision drop.
		phimpss = (1 / (m - r)) * (sum(((-2 * numpy.power((ss / ss2mssH), 2))), 2) + s1oss2mssH)
		phinpss = (1 / (n - r)) * (sum(((-2 * numpy.power((ss / ss2msHs), 2))), 2) + s1oss2msHs)
		Dpss = numpy.multiply(phimss, phinpss) + numpy.multiply(phinss, phimpss)

		# Optimal Shrinkage.
		w = -2 * (numpy.divide(Dss, Dpss))
		for i in range(len(w)):
	# See if this is correct with "isnan"
			if (w[i] == None):
				w[i] = 0

		# MSE estimate.
		tmp = sum(numpy.divide(1, Dss))
		MSE = tmp - sum(numpy.power(w, 2))

		# RMSE estimate.
		RMSE = MSE / tmp

		return w, MSE, RMSE

	# Initializer for the this class' instance.
	def __init__(self):
		print("OptShrink is created!")

	def OptShrink_Main(self, Y, r):

		# Parsing inputs.
		m, n = numpy.array(Y).shape

		# Compute SVD.
		U,sY,V = numpy.linalg.svd(Y, full_matrices=False)

		# Optimal Shrinkage.
		sX, MSE, RMSE = optimalShrinkage(sY, m, n, r)

		# Construct estimate.
		Xhat = U[:][1:r] * diag(sX) * (V[:][1:r]).getH()

		return Xhat, sX, MSE, RMSE


