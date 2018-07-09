import numpy

def adjustLS2(L, S2, M):
	X = S2
	for j in range(len(M[0][0])):
		# Going through the width.
		for k in range(len(M[0])):
		# Going through the height.
			for z in range(len(M)):
				if (M[z][k][j] == 0):
					X[z][k][j] = float('NaN')

	# This should be h * w.
	Delta = numpy.nanmedian(X, 2)
	for h in range(len(Delta)):
		for w in range(len(Delta[0])):
			if (Delta[h][w] == float('NaN')):
				Delta[h][w] = 0

	# 35 is magic number here.
	Delta = numpy.tile(Delta, (1,1,35))

	# Adjust Components.
	L = L + Delta
	S2 = S2 - Delta * M

	return L, S2



def adjustLS2_RGB_Main(L, S2, M):
	L = numpy.array(L)
	ny, nx, nt = L.shape

	L_1 = reshape(L[:][:][1])
	L_1 = reshape(L[:][:][1])
	L_1 = reshape(L[:][:][1])







# function [L, S2] = adjustLS2(L,S2,M)


# % Compute per-pixel adjustment
# X = S2;
# X(~M) = nan;
# Delta = nanmedian(X,3);
# Delta(~any(M,3)) = 0;
# Delta = repmat(Delta,[1, 1, size(M,3)]);

# % Adjust components
# L = L + Delta;
# S2 = S2 - Delta .* M;