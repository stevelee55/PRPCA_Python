import numpy
import cv2
import matplotlib.pyplot as plt


def pano2RGBMovie_Main(frame, Mask, height, width, num_of_frames, moviesize):
	import pdb; pdb.set_trace()
	movie_frames = numpy.zeros((moviesize[1], moviesize[2], 3, num_of_frames))

	for i in range(num_of_frames):
		# May or may not have to add 1 to the height times width. I can't add it because it's too large by 1 to be reshaped into height by width.
		Mask_frame = numpy.reshape(numpy.array(Mask)[0 : height * width, i], (height, width), order="F")
		indicesOfValuesMatchingGivenConditions = numpy.where(Mask_frame)
		indices = numpy.array(numpy.where(numpy.array(Mask_frame) > (numpy.amax(Mask_frame[:]) / 2))).transpose()
		# May be needed.
		# indices = indices.transpose()
		minimumValues = numpy.argmin(numpy.matmul(indices, numpy.array([[1,1],[-1,-1],[1,-1],[-1,1]]).transpose()), axis=0)
		corners = indices[minimumValues,:]
		print(corners)
		fixedPoints_temp = numpy.array([[0,0],[height - 1,0],[height - 1,width - 1],[0, width - 1]])
		movedPoints_temp = numpy.array([corners[0,:], corners[3,:], corners[1,:], corners[2,:]])
		fixedPoints = numpy.array([fixedPoints_temp[:,1], fixedPoints_temp[:,0]], numpy.float32)
		movingPoints = numpy.array([movedPoints_temp[:,1], movedPoints_temp[:,0]], numpy.float32)
		import pdb; pdb.set_trace()
		tform = cv2.getPerspectiveTransform(movingPoints.transpose(),fixedPoints.transpose())
		image = cv2.warpPerspective(frame[:,:,:,0], tform, (width, height))

		plt.imshow(image)
		plt.show()


# movie = zeros(moviesize(1), moviesize(2), 3, num_of_frames);

# for i = 1 : num_of_frames

#     Mask_frame = reshape(Mask(1 : height * width,i), height, width);
#     [I, J] = find(Mask_frame > max(Mask_frame(:)) / 2);
#     IJ = [I,J];
#     [~,idx] = min(IJ * [1 1; -1 -1; 1 -1; -1 1].');
#     corners = IJ(idx,:);
    
#     fixedPoints_temp = [1 1;height 1;height width; 1 width];
#     movedPoints_temp = [corners(1,:);corners(4,:);corners(2,:);corners(3,:)];
#     fixedPoints      = [fixedPoints_temp(:,2) fixedPoints_temp(:,1)];
#     movingPoints     = [movedPoints_temp(:,2) movedPoints_temp(:,1)];
#     TFORM            = fitgeotrans(movingPoints,fixedPoints,'projective');
    
    
#     R = imref2d([height width],[1 width],[1 height]);
#     imgTransformed = imwarp(frame(:,:,:,i),R,TFORM,'OutputView',R);
#     movie(:,:,1,i) = imresize(imgTransformed(:,:,1), [moviesize(1) moviesize(2)]);
#     movie(:,:,2,i) = imresize(imgTransformed(:,:,2), [moviesize(1) moviesize(2)]);
#     movie(:,:,3,i) = imresize(imgTransformed(:,:,3), [moviesize(1) moviesize(2)]);
# end