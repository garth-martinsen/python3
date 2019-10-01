import csv
from SacRecord import SacRecord


class CompareSacSS:

    def __init__(self):
        self.sac_attend = list()
        self.ss_attend = list()
        self.callings = list()

    def readSac(self):
        with open('SacAttend.csv', newline='') as sacfile:
            rsac = csv.reader(sacfile, dialect='excel')
            for row in rsac:
                self.sac_attend.append(SacRecord(row))

    def readSS(self):
        with open('SSAttend.csv', newline='') as ssfile:
            rss = csv.reader(ssfile, dialect='excel')
            for row in rss:
                self.ss_attend.append(SacRecord(rss.__next_()))

    '''

    def readCallings(self):
        with open('Callings.csv', newline='') as callfile:
            rcall = csv.reader(callfile, dialect='excel')



    def subtractCallings(self):
        pass

    def findMissingFromSS(self):
        pass
'''
