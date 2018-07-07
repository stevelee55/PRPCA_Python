import numpy

#class OptShrink(object):


# Data-Driven estimate of optimal shrinkage.
# See Algorithm 1 of [1] for details.
def optimalShrinkage(s, m, n, r):
	# Parse inputs.
	q = min(m, n)
	# Signal singular values.
	# It's getting the very first value.
	# print(s)
	# This means get the elements from 0 - r (r not included) and it doesn't do anything
	# if I just leave it 0 - 0.
	ss = s[0:r + 1]
	# print("ss",ss)

	# Noise singular values.
	# The left of : is included so r + 1 is used and q isn't included so I used q + 1.
	sn2 = numpy.power(s[r + 1:q + 1], 2) # Column Vector.
	# print(len(sn2))
	# print(m)
	# print(q)
	pressH = numpy.append(sn2, numpy.zeros((m - q)))
	# print(pressH)
	# print(len(pressH))
	# print(pressH.shape)
	# Doesn't transposes because it's 1D so just try manually doing it.
	ssH = numpy.array([pressH]) #numpy.transpose(pressH) # Test this. Row vector.
	# print(len(ssH))
	# print("SSH",ssH)
	presHs = numpy.append(sn2, numpy.zeros((n - q)))
	sHs = numpy.array([presHs]) #numpy.transpose(presHs)

	ss2 = numpy.power(ss, 2)
	# "Broadcasting in Matlab has to be done in a specific way, where as in Python, it's automatic." 
	ss2mssH = ss2 - ssH
	ss2msHs = ss2 - sHs
	s1oss2mssH = numpy.sum((1 / numpy.array(ss2mssH)), axis=1)
	s1oss2msHs = numpy.sum((1 / numpy.array(ss2msHs)), axis=1)
	# print(s1oss2mssH)
	# print(s1oss2msHs)
# Watch out for precision dropping. Check and see if matlab drops the precision.
	phimss = numpy.multiply((ss / (m - r)), s1oss2mssH)
	phinss = numpy.multiply((ss / (n - r)), s1oss2msHs)
	Dss = numpy.multiply(phimss, phinss)

	# print("1", phimss)
	# print("2",phinss)
	# print("Dss", Dss)

	# Numerical approximation of D transform derivative. 
# Check for the precision drop.
	phimpss = (1 / (m - r)) * (numpy.sum(((-2 * numpy.power((ss / ss2mssH), 2))), axis=1) + s1oss2mssH)
	phinpss = (1 / (n - r)) * (numpy.sum(((-2 * numpy.power((ss / ss2msHs), 2))), axis=1) + s1oss2msHs)
	Dpss = numpy.multiply(phimss, phinpss) + numpy.multiply(phinss, phimpss)

	# print("1", phimpss)
	# print("2",phinpss)
	# print("Dpss",Dpss)

	# Optimal Shrinkage.
	w = -2 * (numpy.divide(Dss, Dpss))
	for i in range(len(w)):
# See if this is correct with "isnan"
		if (w[i] == None):
			w[i] = 0

	# MSE estimate.
	# print("Dss", Dss)
	tmp = sum(numpy.divide(1, Dss))
	# print(tmp)
	MSE = tmp - numpy.sum(numpy.power(w, 2))
	# print("w^2", numpy.power(w, 2))
	# print("baf", numpy.sum(numpy.power(w, 2)))

	# RMSE estimate.
	RMSE = MSE / tmp

	# print("RMSE",RMSE)
	# print("MSE",MSE)
	# print("w",w)

	return w, MSE, RMSE

# Initializer for the this class' instance.
#def __init__(self):
	#print("OptShrink is created!")

def OptShrink_Main(Y, r):

	# Parsing inputs.
	m, n = numpy.array(Y).shape

	print(m)
	print(n)

	# print(Y)
	# Compute SVD.
	U,sY,V = numpy.linalg.svd(Y, full_matrices=False)
	# Optimal Shrinkage.
	sX, MSE, RMSE = optimalShrinkage(sY, m, n, r)

	# print(U)

	# Construct estimate.
	print("U", numpy.array(U))
	print("V", numpy.array(V))
	print("sX", numpy.array(sX))


	thing = numpy.array(U)[:,0]
	thing1 = numpy.array([numpy.array(V)[:,0]])
	print("U:][0:r + 1]", thing)
	print("V:][0:r + 1]", thing1)
	print("U:][0:r + 1]", thing.shape)
	print("V:][0:r + 1]", thing1.shape)

	print((numpy.array(U)[:,[0]] * numpy.diag(sX)).shape)
	Xhat = numpy.matmul((numpy.array(U)[:,[0]] * numpy.diag(sX)), numpy.array([numpy.array(V)[:,0]]))
	
	print("Xhat",Xhat)
	print("Xhat shape",Xhat.shape)
	return Xhat, sX, MSE, RMSE


