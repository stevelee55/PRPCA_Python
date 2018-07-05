# def adjustLS2_RGB_Main(L, S2, M):
# 	L = numpy.array(L)
# 	ny, nx, nt = L.shape

# 	L_1 = reshape(L[:][:][1])
# 	L_1 = reshape(L[:][:][1])
# 	L_1 = reshape(L[:][:][1])







# function [L, S2] = adjustLS2(L,S2,M)
# %
# % Syntax: [L, S2] = adjustLS2(L,S2,M);
# %
# %  L: (ny x nx x nt) background
# % S2: (ny x nx x nt) foreground
# %  M: (ny x nx x nt) frame masks
# %

# % Compute per-pixel adjustment
# X = S2;
# X(~M) = nan;
# Delta = nanmedian(X,3);
# Delta(~any(M,3)) = 0;
# Delta = repmat(Delta,[1, 1, size(M,3)]);

# % Adjust components
# L = L + Delta;
# S2 = S2 - Delta .* M;