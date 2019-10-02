import unittest
from unittest.mock import patch
from Study import Study
from os import path

class TestStudy(unittest.TestCase):
   '''   
   def __init__(self):
   def loadReferences(self):
   def getImg(self):
   def loadImg(self, path):
   def process(self, erd, dlt):
   def chooseBest(self, img, refDigits, erd, dlt):
   def varyTimes(self):
   def createSubPlot(self, i, name, img):
   def testAll(self):

   '''
   #-----------just starting------------------------------------------

   def setUp(self):
      self.study = Study()

   def test_loadReferences(self):
      self.assertTrue(path.exists(self.study.ref_file))  
      self.assertEqual("<class 'numpy.ndarray'>", str(type(self.study.references)))
      '''
      with patch('self.study.np.load') as mocked_load:
          self.study.loadReferences() 
          mocked_load.assert_called_once_with(self.study.ref_file, allow_pickle=True)   
      '''
   def test_loadimg(self):
      self.assertTrue(path.exists(self.study.imgpath))  
      self.assertEqual("<class 'numpy.ndarray'>", str(type(self.study.img)))
      '''with patch('self.study.cv.imread') as mocked_read:
         self.study.loadimg(self.study.imgpath)
         mocked_read.assert_called_once_with(self.study.imgpath)
      '''


if __name__ == '__main__':
      unittest.main()          


