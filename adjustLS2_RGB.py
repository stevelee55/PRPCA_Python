import numpy
import math
import matplotlib.pyplot as plt

def adjustLS2(L, S2, M):

	#import pdb; pdb.set_trace()

	X = S2
	for j in range(len(M[0][0])):
		# Going through the width.
		for k in range(len(M[0])):
		# Going through the height.
			for z in range(len(M)):
				if (M[z][k][j] == 0):
					X[z][k][j] = float('NaN')

	#import pdb; pdb.set_trace()

	# This should be h * w.
	Delta = numpy.nanmedian(X, 2)
	for h in range(len(M)):
		for w in range(len(M[0])):
			if (not any(M[h][w])):
				Delta[h][w] = 0

	#import pdb; pdb.set_trace()

	# 35 is magic number here.
	Delta = numpy.tile(Delta, (len(L[0][0]),1,1))

	print("adjust :D")

	#import pdb; pdb.set_trace()

	# Adjust Components.
	for frameNumber in range(len(L[0][0])):
		L[:,:, frameNumber] = L[:,:,frameNumber] + Delta[frameNumber]
		S2[:,:, frameNumber] = S2[:,:, frameNumber] - Delta[frameNumber] * M[:,:,frameNumber]

	#import pdb; pdb.set_trace()

	return L, S2



def adjustLS2_RGB_Main(L, S2, M):
	L = numpy.array(L)
	ny, nx, notUse, nt = L.shape

	L_1 = numpy.reshape(L[:,:,0,:], (ny, nx, nt),order="F")
	L_2 = numpy.reshape(L[:,:,1,:], (ny, nx, nt),order="F")
	L_3 = numpy.reshape(L[:,:,2,:], (ny, nx, nt),order="F")

	# plt.imshow(L_1[:,:,0])
	# plt.show()

	S_1 = numpy.reshape(S2[:,:,0,:], (ny, nx, nt),order="F")
	S_2 = numpy.reshape(S2[:,:,1,:], (ny, nx, nt),order="F")
	S_3 = numpy.reshape(S2[:,:,2,:], (ny, nx, nt),order="F")

	M_1 = numpy.reshape(M[:,:,0,:], (ny, nx, nt),order="F")
	M_2 = numpy.reshape(M[:,:,1,:], (ny, nx, nt),order="F")
	M_3 = numpy.reshape(M[:,:,2,:], (ny, nx, nt),order="F")

	L_FINAL = numpy.array([[[[0.0 for i in range(nt)] for j in range(notUse)] for k in range(nx)] for z in range(ny)])
	S2_FINAL = numpy.array([[[[0.0 for i in range(nt)] for j in range(notUse)] for k in range(nx)] for z in range(ny)])

	L_tmp, S2_tmp = adjustLS2(L_1,S_1,M_1)

	L_FINAL[:,:,0,:] = L_tmp
	S2_FINAL[:,:,0,:] = S2_tmp

	L_tmp, S2_tmp = adjustLS2(L_2,S_2,M_2)
	L_FINAL[:,:,1,:] = L_tmp
	S2_FINAL[:,:,1,:] = S2_tmp

	L_tmp, S2_tmp = adjustLS2(L_3,S_3,M_3)
	L_FINAL[:,:,2,:] = L_tmp
	S2_FINAL[:,:,2,:] = S2_tmp

	return L_FINAL, S2_FINAL


# [ny, nx, ~, nt] = size(L);

# for 

# L_1 = reshape(L(:,:,1,:),ny, nx, nt);
# L_2 = reshape(L(:,:,2,:),ny, nx, nt);
# L_3 = reshape(L(:,:,3,:),ny, nx, nt);

# S_1 = reshape(S2(:,:,1,:),ny, nx, nt);
# S_2 = reshape(S2(:,:,2,:),ny, nx, nt);
# S_3 = reshape(S2(:,:,3,:),ny, nx, nt);

# M_1 = reshape(M(:,:,1,:),ny, nx, nt);
# M_2 = reshape(M(:,:,2,:),ny, nx, nt);
# M_3 = reshape(M(:,:,3,:),ny, nx, nt);

# [L_tmp, S2_tmp] = adjustLS2(L_1,S_1,M_1);

# L_FINAL(:,:,1,:) = L_tmp;
# S2_FINAL(:,:,1,:) = S2_tmp;

# [L_tmp, S2_tmp] = adjustLS2(L_2,S_2,M_2);

# L_FINAL(:,:,2,:) = L_tmp;
# S2_FINAL(:,:,2,:) = S2_tmp;

# [L_tmp, S2_tmp] = adjustLS2(L_3,S_3,M_3);

# L_FINAL(:,:,3,:) = L_tmp;
# S2_FINAL(:,:,3,:) = S2_tmp;


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