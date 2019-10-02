import cv2 as cv
import numpy as np
from imutils import contours
import time
import matplotlib.pyplot as plt
import re
from Scores import Scores


class Study:
    '''Class used to perfect the cv2 operations to detect digits [0-9]
       used to comprise numbers from 0-120 inches of depth''' 
    def __init__(self):
        print('__init__')
        self.rsz = (80, 100)
        self.ref_file = '/Users/garth/Programming/python3/ocr/refs.npy'
        self.imgpath = '/Users/garth/imgs/image10.jpg'
        self.references = self.loadReferences()
        self.img = self.getImg()
        self.fig = plt.figure(figsize=(10, 10))
        self.subplots = (3, 6)
        self.number = 0

    def loadReferences(self):
        return np.load(self.ref_file, allow_pickle=True)

    def getImg(self):
        return cv.imread(self.imgpath)

    def loadImg(self, path):
        print('imgpath: {:s}'.format(path))
        return cv.imread(path)

    def process(self, erd, dlt):
        print('entered process(...)')
        start = time.perf_counter()
        imgc = cv.imread(self.imgpath)
        low, rez = cv.threshold(imgc, 30, 255, cv.THRESH_BINARY)
        rez = cv.cvtColor(rez, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(rez, (7, 7), 0)
        r, rezinvt = cv.threshold(blur, 230, 255, cv.THRESH_BINARY_INV)
        kernel = np.ones((5, 5), np.uint8)
        for i in range(erd):
            rezinvt = cv.erode(rezinvt, kernel)
        for i in range(dlt):
            rezinvt = cv.dilate(rezinvt, kernel)
            # self.createSubPlot(13, 'img', rezinvt)
        cnt, hier = cv.findContours(rezinvt, cv.RETR_EXTERNAL,
                                    cv.CHAIN_APPROX_SIMPLE)
        cnt = contours.sort_contours(cnt, method="left-to-right")[0]
        num = 0
        locs = ''
        # first 13 imgs are of the reference digits. 
        i = 14  

        for c in cnt:
            x, y, w, h = cv.boundingRect(c)
            if w > 100 and h > 100:
                # note the order: y,x for roi clipping
                iroi = rezinvt[y:y + h, x:x + w]  
                iroi = cv.resize(iroi, self.rsz)
                digit = self.chooseBest(iroi, self.references, erd, dlt)
                locs = locs + str(digit)
                num = num + 1
                # cv.imshow('iroi',iroi )
                #    self.createSubPlot(i, 'img' + str(num), iroi)
                cv.waitKey(9)
                i = i + 1
        print('img contours count: {:3d}'.format(num))
        lap = time.perf_counter()
        print(
              'imgProcess processing time: {:4.2f} seconds'.format(lap - start)
             )
        self.fig.show()
        return locs

    def chooseBest(self, img, refDigits, erd, dlt):
        '''
        Given the reference digits and the single digit from the input img, 
        choose the best candidate.
        '''
        start = time.perf_counter()
        # initialize a list of template matching scores

        high = -9999999.99
        d = -1
        # loop over the reference digit name and digit ROI
        for (digit, digitROI) in refDigits.all().items():
            # apply correlation-based template matching, take the
            result = cv.matchTemplate(img, digitROI, cv.TM_CCOEFF)
            (_, score, _, _) = cv.minMaxLoc(result)
            scores = Scores(self.number)
            scores.result[scores.cnt][digit] = score
            # print('score: {:10.1f}'.format(score) )
            if score > high and score > 0:
                high = score
                d = digit
            #   print('digit :{:02d}, score: {:0.2f}'.format(digit, score))
            # scores.append(score)
            lap = time.perf_counter()
        #  print('chooseBest processing time: {:4.2f}'.format(lap-start))
        scores.cnt = scores.cnt + 1
        print('number: {:3d}  erd: {:2d} dlt: {:2d} digit: {:3d} score: {:10.1f} time: {:4.2f}'.format(self.number, erd,
                                                                                                       dlt, d, high,
                                                                                                       (lap - start)))
        print('scores: '.format(scores))
        return d

    def varyTimes(self):
        for erd in range(5):
            for dlt in range(20):
                self.process(erd, dlt)

    def createSubPlot(self, i, name, img):
        ax = self.fig.add_subplot(self.subplots[0], self.subplots[1], i)
        ax.text(20, 10, name, color='red', fontsize=12, )
        ax.imshow(img)

    def testAll(self):
        imdir = '/Users/garth/imgs/cmimgs/'
        import os
        files = os.listdir(imdir)
        for f in files:
            if f.startswith('cm'):
                self.number = int(re.sub(r'\D', "", f))
                self.imgpath = imdir + f
                # print('file: {:s} number: {:3d} '.format(imdir + f, self.number) )
                self.process(0, 9)
