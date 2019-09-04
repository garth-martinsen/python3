import unittest
from Scores import Scores

class TestScores(unittest.TestCase):
   
   def test_detect(self):
      scores=Scores(102)
      self.load(scores)
      scores.detect()
      self.assertEqual(scores.detected, 102)

   def test_clarity(self):
      scores=Scores(102)
      a = list('102')
      self.load(scores)
      scores.clarity()
      s= len(scores.clardicts)
      for d in range(s):
         self.assertEqual(1.0, max(scores.clardicts[d].values()))
         for x,y in scores.clardicts[d].items():
            if y==1.0:
               self.assertEqual(a[d],str(x)) 

   def test_addscore(self):
     scores=Scores(102)
     scores.addscore(0, 1, 1000001)
     scores.addscore(1, 0, 1000001)
     scores.addscore(2, 2, 1000001)
     self.assertEqual(scores.result[0][1], 1000001)
     self.assertEqual(scores.result[1][0], 1000001)
     self.assertEqual(scores.result[2][2], 1000001)

   def load(self,scores):
      scores.addscore(0, 0, 100001)
      scores.addscore(0, 1, 1000001)
      scores.addscore(1, 0, 1000001)
      scores.addscore(1, 1, 100001)
      scores.addscore(2, 0, 100001)
      scores.addscore(2, 1, 100001)
      scores.addscore(2, 2, 1000001)
      scores.clarity()


if __name__ == '__main__':
      unittest.main()          

