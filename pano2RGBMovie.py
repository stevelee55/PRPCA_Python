import numpy

def pano2RGBMovie_Main(frame, Mask, height, width, num_of_frames, moviesize):
	movie = numpy.zeros(moviesize[0], moviesize[1], 3 num_of_frames)

	for i in range(num_of_frames):
		Mask_frame = reshape(Mask[0 : height * width + 1, i], height, width, order="F")
		



movie = zeros(moviesize(1), moviesize(2), 3, num_of_frames);

for i = 1 : num_of_frames

    Mask_frame = reshape(Mask(1 : height * width,i), height, width);
    [I, J] = find(Mask_frame > max(Mask_frame(:)) / 2);
    IJ = [I,J];
    [~,idx] = min(IJ * [1 1; -1 -1; 1 -1; -1 1].');
    corners = IJ(idx,:);
    
    fixedPoints_temp = [1 1;height 1;height width; 1 width];
    movedPoints_temp = [corners(1,:);corners(4,:);corners(2,:);corners(3,:)];
    fixedPoints      = [fixedPoints_temp(:,2) fixedPoints_temp(:,1)];
    movingPoints     = [movedPoints_temp(:,2) movedPoints_temp(:,1)];
    TFORM            = fitgeotrans(movingPoints,fixedPoints,'projective');
    
    
    R = imref2d([height width],[1 width],[1 height]);
    imgTransformed = imwarp(frame(:,:,:,i),R,TFORM,'OutputView',R);
    movie(:,:,1,i) = imresize(imgTransformed(:,:,1), [moviesize(1) moviesize(2)]);
    movie(:,:,2,i) = imresize(imgTransformed(:,:,2), [moviesize(1) moviesize(2)]);
    movie(:,:,3,i) = imresize(imgTransformed(:,:,3), [moviesize(1) moviesize(2)]);
end