#file: ~/Programming/Python/VoltgeDivider
import os

class VoltageDivider:
   '''class VoltageDivider will design voltage dividers
for each stage of a mult-cell Battery. It requires the values and wattage
of the resisters to be used, the zener diode specs, the target voltage to be
sampled at the A2D, the number and voltage of the cells that make up the battery.
   '''
   data=[]
   myResistors = [10,15,22,30,39,47,68,75,100,150,220,270,330,360,470,510,680,1000,2000,2200,3300,4700,5100,6800,10000,15000,22000,30000,47000,51000,68000,100000,220000,300000,470000,680000,1000000]

   def initialize(self):
      print('Enter input complete filename path:')
      fn = input()               #reads input file complete path.
      fh = open(fn)
      print(fh.readline())       #prints which input file was opened, no data yet.
      self.batterySpecs(4.2,6)
      self.zenerSpecs(3.3,0.5)
      self.a2dSpecs(10,3.3)
      self.resistorSet(self.myResistors, 0.250)
      self.getSpecs()
      self.computeFractions()
      self.createDictd()
      self.computeDividers()
      self.slotDividers()
      self.designStages()
      self.getDesign()

   def inputValue(s):
      return float(s.split(":")[0])

   def createDictd(self):
      self.dictd = {0.0:[],0.1:[],0.2:[],0.3:[],0.4:[],0.5:[],0.6:[],0.7:[],0.8:[],0.9:[], 1.0:[]}
      
   def resistorSet(self, rs, watt):
      self.resistorSet=rs
      self.resistorWattage = watt

   def batterySpecs(self, cv, nc):
      self.stageVoltages=[]
      self.cellVoltage=cv
      self.numCells=nc
      for i in range(0,nc+1):
         self.stageVoltages.append(float('{:3.1f}'.format(i*self.cellVoltage)))

   def frmtf(self, num, w, p):
      spec = '{:' + str(w) + '.' + str(p) +'f}'
      return float(spec.format(num))

   def zenerSpecs( self, zv,zw):
      self.zenerVoltage=zv
      self.zenerWattage=zw
      self.ziLimitMa=self.frmtf(1000*zw/zv, 3,0)

   def a2dSpecs(self, bits, vl):
      self.a2dBits=bits
      self.a2dCounts=pow(2,bits)-1
      self.a2dVoltage=vl
      self.targetVoltage=vl/2.0

   def getSpecs(self):
      print("Battery: " + str(self.numCells) + "  cells at: " + str(self.cellVoltage) + " volts at each stage \n stageVoltages: "+ str(self.stageVoltages))
      print("Resistor wattage: " + str(self.resistorWattage) + " watts \n Resistor Set: " + str(self.resistorSet) )
      print("A2D bits: " + str(self.a2dBits) + " A2dCounts: " + str(self.a2dCounts) + " Aref Voltage: " + str(self.a2dVoltage) + " TargetVoltage at a2d when charged: " + str(self.targetVoltage) + " volts")
      print("Zener diode capped at: " + str(self.zenerVoltage) + " volts  Power Limit: " + str(self.zenerWattage) + " watts  Current Limit: " + str(self.ziLimitMa) + " milliAmps" )    

   def computeFractions(self):
      self.fractions=[]
      for voltage in self.stageVoltages[1:len(self.stageVoltages)]:
         if(voltage == 0):
            self.fractions.append(0.0)
         else:            
            self.fractions.append(self.targetVoltage /voltage)

   def myUnion(self, lst):
      lst2=[]
      for i in lst:
         lst2.append(i)
      for i in lst:
         lst2.append(i)
      return lst2

   def slotDividers(self):
      '''place the divider fractions in dictionary keyed on bins: 0.0, 0.1, ..., 0.9, 1.0 '''
      for d in self.dividers:
         f=d.fract
         slot = float('{:2.1f}'.format(f))
         self.dictd.get(slot).append(d)

   def fractToSlot(self,f):
      '''Given a float,n, where 0 < n < 1.0, return a float with one decimal place precision ie: 0.0, 0.1, 0.2, ..., 0.8, 0.9, 1.0'''
      return float('{:2.1f}'.format(f))         

   def computeDividers(self):
      '''Given resistor set, create a List of pairs of resistors,(tuples of 2) for all unique combinations '''
      dividers = []
      r=self.resistorSet
      r2 = self.myUnion(r)  #List with r repeated, so r2 is twice the length of r
      for i in range(0,len(self.resistorSet)):
         # slide r along r2 for all of r
         self.addDividers(dividers, zip(r, r2[i:]))
      self.dividers=dividers

   def addDividers(self, dvdrs, pairs):
      for p in pairs:
         dvdrs.append(rset(self, p[0],p[1]))

   def selectDivider(self, stage):
      '''Using stageVoltage, resistor sizing, fraction desired, select a pair of resistors that will meet the constraints for power, zener.'''
      rxmin = self.minRx(self.stageVoltages[stage] - self.targetVoltage)
      rymin = self.minRy(self.targetVoltage)
      print('stage: {}, minRx: {}, minRy: {}'.format(stage, rxmin,rymin))
      fract = self.targetVoltage/self.stageVoltages[stage]
      if (fract < 1.0):
         slot=self.fractToSlot(fract)
         lst = self.dictd.get(slot)                         #get only resister sets from bin holding the desired fract.
         cans = list(filter(lambda x: x.rx > rxmin, lst))   # filter out rsets with rx smaller than rxmin ohms
         cans = list(filter(lambda x: x.ry > rymin, cans))  # filter out rsets with ry smaller than rymin ohms
         cans.sort(key = lambda x: abs(x.fract - fract))    # sort by the diff from desired fract.
         can = cans[0]                                      # take the first candidate which has the smallest difference from fract and meets rqts.
#         print(can)
         return can
      else:
         return None

   def minRx(self,volts):
      ''' For design voltages, Given the resistor wattage, voltage drop across rx of the voltage divider and zener current limit, the largest of two r values is returned as minimum rx'''
      rw= pow(volts,2)/self.resistorWattage             #prevent rx destruction
      rz= volts/(self.ziLimitMa/1000.0)                 #prevent zener destruction
      return max(rw,rz)

   def minRy(self,volts):
      ''' For design voltages, Given the resistor wattage, voltage drop across ry of the voltage divider, return minRyt, so that ry > vy*vy/rw'''
      return volts*volts/self.resistorWattage
 
   def designStages(self):
      self.design =[]
      for s in range(1,self.numCells+1): 
         sv = self.cellVoltage*s
         can = self.selectDivider(s) 
         d =vrset(can,sv)
         self.design.append(d)
    

   def getDesign(self):
      for d in self.design:
        print(d)

# rset sorters
   def byRy(self,e):
      return e.ry

   def byRx(self,e):
      return e.rx
   
   def byFract(self,e):
      return e.fract

   def byRxp(self,e):
      return e.prx

class vrset:
   def __init__(self, rset, sv):
      vd=rset.vd
      self.rx=rset.rx
      self.ry=rset.ry
      self.fract=rset.fract
      self.goalFract = vd.targetVoltage/sv
      ziLimit = vd.zenerWattage/vd.zenerVoltage                           # Allowable limit for zener current, which is never reached because rx resistor wattage is limiting factor.
      vxLimit = pow( self.rx * vd.resistorWattage, 0.5)                   # limit to allowable voltage drop in Rx, after which Rx self destructs.
      self.prx = pow((1-self.fract)*sv,2.0)/self.rx                       # at design voltages.
      self.pry = pow(self.fract*sv,2.0)/self.ry                           # at design voltages.
      self.inputVoltageLimit = vxLimit/(1-self.fract)                     # limit to input Voltage for VoltageDivider. 
      self.ziAtMaxVoltage = vxLimit/self.rx - vd.zenerVoltage/self.ry     # zener overflow current at input Voltage Limit: iz = ix - iy
      if(self.ziAtMaxVoltage<0.0):
        self.ziAtMaxVoltage = 0.0

   def __repr__(self):
     return '\nrx: {}, ry: {}, f: {}, gf: {:5.4f}, prx: {}, pry: {}, vilim: {}, zim: {}'.format(self.rx,self.ry,self.fract,self.goalFract,  self.prx,self.pry,self.inputVoltageLimit, self.ziAtMaxVoltage)

class rset:
   def __init__(self, vd, x, y):
      self.rx=x
      self.ry=y
      self.fract=vd.frmtf(y/(x+y), 5,4)
      self.vd=vd

   def __repr__(self):
      return('rx: {}, ry: {}, fract: {}'.format(self.rx, self.ry, self.fract))

# f = open("myfile.txt", "w")   #create for writing
# f.write("Now the file has this line!")
#  print('Enter your name:')
#  x = input()
