import time

start = time.time()

import argparse
import cv2
import itertools
import os

import numpy as np
np.set_printoptions(precision=2)

import openface

fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join(fileDir, '..', 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')


class openface_lib:
    def __init__(self):
        self.image = "./images/examples/{lennon*,clapton*}"
        self.networkModel = os.path.join(openfaceModelDir, 'nn4.small2.v1.t7')
        self.dlibFacePredictor = os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat")
        self.imgDim = 96
		
        self.start = time.time()
        self.align = openface.AlignDlib(self.dlibFacePredictor)  # dlib model
        self.net = openface.TorchNeuralNet(self.networkModel, self.imgDim)  # openface model


    def getRep(self,imgPath):

        bgrImg = cv2.imread(imgPath)
        if bgrImg is None:
            raise Exception("Unable to load image: {}".format(imgPath))
        rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)


        start = time.time()
        bb = align.getLargestFaceBoundingBox(rgbImg)
        if bb is None:
            raise Exception("Unable to find a face: {}".format(imgPath))

        start = time.time()
        alignedFace = align.align(args.imgDim, rgbImg, bb,
                              landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        if alignedFace is None:
            raise Exception("Unable to align image: {}".format(imgPath))

        start = time.time()
        rep = net.forward(alignedFace)

        return rep

    def compare(self,orig_img,know_img):

        for (img1, img2) in itertools.combinations(self.imgs, 2):
            start = time.time()
            d = self.getRep(img1) - self.getRep(img2)
            print("Comparing {} with {}.".format(img1, img2))
            print("  + Squared l2 distance between representations: {:0.3f}".format(np.dot(d, d)))
            print("took {} seconds.".format(time.time() - start))
            return np.dot(d, d)

if __name__ == "__main__":
	openface_lib = openface_lib()
	openface_lib.compare()
