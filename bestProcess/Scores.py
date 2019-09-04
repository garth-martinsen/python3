''' Scores class allows the capture of the ground digit, the detected digit, the result which contains n dictionaries with key=candidate digit and value=score for templated fit of each candidate digit.'''


class Scores:
  def __init__(self, grnd):
     self.ground=grnd
     self.detected = -1
     self.item=0
     self.result = [{},{},{}]

  def addscore(self, count, digit, score):
     self.result[count].update({ digit: score})

  '''clarity indicates the scores normalized by the winning score. So the resulting dict will have a 1 for its score and all other scores will be a fraction f, where   0 < f < 1. If the f's are all less than 0.5 then the process yielded a pretty good clarity in detecting the winning digit. '''

  def clarity(self):
     clardicts = [{}, {},{}]
     for i in range(len(self.result)):
        if len( self.result[i])< 1 :
           continue
        else:
           hi = max( self.result[i].values())
           for k,v in self.result[i].items():
              clardicts[i].update({k: v/hi})
     self.clardicts = clardicts

  def __str__(self):
     return 'ground: {:d} detected: {:d} {} '.format(self.ground, self.detected, self.results() )

  def results(self):
     bykey   = lambda x: x[0]
     byvalue = lambda x: x[1]
     s='\nresult:\n'
     for i in range(3):
       s= s + str(sorted(self.result[i].items(), key=bykey)) + '\n' 
     return s 

  def detect(self):
      v=''
      cnt = len(self.result)
      for d in range(cnt):
          h = max(self.result[d].values())
          for x, y in self.result[d].items():
              if y==h:
                  v= v+ str(x)
      self.detected=int(v)
