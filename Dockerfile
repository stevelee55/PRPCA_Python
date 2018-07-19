From python:3.4
COPY dockertest.py dockertest.py
COPY demo_PRPCA.py demo_PRPCA.py
COPY HomographyTrans.py HomographyTrans.py
COPY improvedRobustPCA.py improvedRobustPCA.py
COPY OptShrink.py OptShrink.py
COPY pano2RGBMovie.py pano2RGBMovie.py
COPY PRPCA_RGB.py PRPCA_RGB.py
COPY adjustLS2_RGB.py adjustLS2_RGB.py
COPY ./Data/tennis ./Data/tennis
RUN pip installsdf numpy
RUN pip install matplotlib
RUN pip install opencv-python
RUN pip install opencv-contrib-python
RUN pip install scikit-image
RUN pip install imread
RUN pip install boto3
CMD ["python3.4", "demo_PRPCA.py"]