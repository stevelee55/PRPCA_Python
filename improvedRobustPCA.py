import math
import numpy
from OptShrink import OptShrink_Main

class improvedRobustPCA(object):
	# Soft thresholding
	def soft(self, X, lamb):
		print("ADSFADSFADF :D")
		print(numpy.sign(X))
		print(abs(X))
		print(abs(X) - lamb)
		print(numpy.maximum((abs(X) - lamb), 0))
		Y = numpy.sign(X) * numpy.maximum((abs(X) - lamb), 0)
		print("Y", Y)
		return Y

	# Function that parses struct field
	def parseField(self, stats, field, default):
		# Value to return from the function.
		val = None
		# Checking if the field/key exists in the "stats" struct.
		# "hasattr" already exists in python.
		if hasattr(stats, field):
			val = getattr(stats, field)
		else:
			val = default
		return val

	# Parsing inputs.
	def parseInputs(self, Y, opts):
		# Checking to see if opts and var exists and then creating something.
		# opts = struct
		# I think isRGB is boolearn return type so I changed the third paramter from
		# 1 to "True".
		A = self.parseField(opts, "A", 1)
		M = self.parseField(opts, "M", 1)
		T = self.parseField(opts, "T", 1)
		AtransArray = numpy.array(A)
		AtransArray = AtransArray.transpose()
		# print("A * Y", A * Y)
		L0 = self.parseField(opts, "L0", A * Y)
		S0 = self.parseField(opts, "S0", numpy.zeros(numpy.array(L0).shape))
		accel = self.parseField(opts, "accel", True)
		tau = 0.5000  # self.parseField(opts, "tau", 1) / ((1 + accel) * norm)
		delta = self.parseField(opts, "delta", 1 * 10 ** -6)
		maxIters = self.parseField(opts, "maxIters", 1000)
		flag = self.parseField(opts, "flag", True)

		return A, M, T, L0, S0, accel, tau, delta, maxIters, flag

	# Initializer for the this class' instance.
	def __init__(self):
		print("improvedRobustPCA is created!")

	def improvedRobustPCA_Main(self, Y, r, lambdaS, opts):

		# Parsing inputs.
		A, M, T, L0, S0, accel, tau, delta, maxIters, flag = self.parseInputs(Y, opts)

		# Init stats.
		nIters = 0
		deltaL = []
		deltaS = []
		time = []

		# Output.
		# iterFmt = print()

		# Robust PCA.
		t = 0.0
		L = numpy.array(L0)
		S = numpy.array(S0)
		Llast = numpy.array(L0)
		Slast = numpy.array(S0)

		# print("L",L)
		# print("S",S)
		# print("Llast",Llast)
		# print("Slat",Slast)

		done = False

		while not done:
			nIters = nIters + 1

			if accel:
				#import pdb; pdb.set_trace()

				# Accelerated proximal gradient step.
				tlast = t
				t = 0.5 * (1 + math.sqrt(1 + 4 * t**2))
				# print("t", t)
				Lbar = L + ((tlast - 1.0) / t) * (L - Llast)
				# print("Lbar",Lbar)
				Sbar = S + ((tlast - 1.0) / t) * (S - Slast)
				# print("Lbar",Sbar)
				Llast = L
				Slast = S

				# AtransArray = numpy.array(A)
				# AtransArray = AtransArray.transpose()
				# Replaced A' with 1 because that's the output.
				Z = A * (M * ((A * (Lbar + Sbar)) - Y))
				# print("Z", Z)
				# print("Lbar - tau * Z", Lbar - tau * Z)
				# print("r", r)
				L, sX, MSE, RMSE = OptShrink_Main(Lbar - tau * Z, r)
				print("L",L)
				print("MSE", MSE)
				print("RMSE", RMSE)
				TtransArray = numpy.array(T)
				TtransArray = TtransArray.transpose()
				S = TtransArray * self.soft(T * (Sbar - tau * Z), tau * lambdaS)
				print("S",S)

			if (nIters >= 2):  # or ((deltaL(nIters) < delta) and ()
				done = True
			print("Iteration #:", nIters)
		   #import pdb; pdb.set_trace()
		return L, S
