import csv
from SacRecord import SacRecord
from Called import Called


class CompareSacSS:

    sacCsv = '2019 Aloha 2 Sacrament Attendance - QTR4.csv'
    ssCsv = 'SSAttend - SSQtr4.csv'
    callCsv = 'Callings - Callings.csv'

    def __init__(self):
        self.sac_roll = list()                      # records for sac mtg
        self.ss_roll = list()
        self.call_roll = list()
        self.attendance = list()                    # dates in the qtr
        self.skipped = dict()                           # dictionary wk:missedSS
        self.called=set()
        self.read_input_files()


    def read_input_files(self):
        self.readSac(self.sacCsv)
        self.readSS(self.ssCsv)
        self.readCallings(self.callCsv)
       

    def condition_rolls(self):
        self.captureDatesLimitSacList()
        self.namesCalled()

    def readSac(self,csvfile):
        with open(csvfile, newline='') as sacfile:
            sacs = csv.reader(sacfile)
            for row in sacs:
                self.sac_roll.append(SacRecord(row))
    
    def readSS(self,csvfile):
        with open(csvfile, newline='') as ssfile:
            rss = csv.reader(ssfile, dialect='excel')
            for row in rss:
                self.ss_roll.append(SacRecord(row))
            # remove header
            self.ss_roll = self.ss_roll[1:]

    def readCallings(self,csvfile):
        with open(csvfile, newline='') as callfile:
            rcall = csv.reader(callfile, dialect='excel')
            for row in rcall:
                self.call_roll.append(Called(row))

    def captureDatesLimitSacList(self):
        '''Capture dates; cutoff list after last member name'''
        # get header record and save dates to self.attendance
        self.attendance = self.sac_roll[0].attendance
        # co is index after the last member record.
        co = self._cutoff('Member Count of Standard Role')
        # remove row for header and rows for formulas for counting 
        # in spreadsheet.
        self.sac_roll = self.sac_roll[1:co]

    def adltNamesAttendedSac(self, wk):
        '''
        adultsAttendingSac takes wk as an int, will return
        a list of all members over age 17 who attended Sac on that date
        '''

        adltAttendedSac = set()
        for m in self.sac_roll:
            # the '1' indicates they were pesent
            if int(m.age) >  18 and m.attendance[wk]  == '1':
                # print(m)
                adltAttendedSac.add(m.name)
        return adltAttendedSac

    def adultNamesAttendedSS(self, wk):
        adltAttendedSS = set()
        for m in self.ss_roll:
            if m.attendance[wk] == '1':        # the '1' indicates they were present
                # print(m)
                adltAttendedSS.add(m.name)
        return adltAttendedSS

    def namesCalled(self):
        '''Saves a set of the names of adults with callings during SS'''
        for n in self.call_roll:
            self.called.add(n.name)

    def _cutoff(self, str):
        i = 0
        for m in self.sac_roll:
            if m.name == str:
                return i
            i = i+1

    def findSkipped(self):
        for w in range(len(self.attendance)):
            self.missedSS(w)


    def missedSS(self, wk):
        ''' Stores dict (key=wk, value=list of names) in self.skipped
        for adults attending sacrament mtg,
        who do not have call_roll and who did not attend SS'''
        # print('running missedSS')
        sacAdults = self.adltNamesAttendedSac(wk)
        ssAdults = self.adultNamesAttendedSS(wk)
        candidates = (sacAdults - self.called)
        self.skipped.update({wk : (candidates - ssAdults)})

    def showMissed(self):
        # print('running missedSS')
        for s in self.skipped:
            if s%2 == 1:
                print('\n\033[1m wk: {} date: {} count: {} \033[0m'.format(s, self.attendance[s], len(self.skipped[s])))
                for l in self.skipped[s]:
                    if s%2 ==1:
                        print('\t{0:30}'.format(l))

    def showCallings(self):
        print('Members who have Callings during SS')
        print('\033[1m     {0:30} {1:16}'.format(self.call_roll[0].name, self.call_roll[0].org))
        for c in self.call_roll[1:]:
            print('\033[0m     {0:30} {1:16} '.format(c.name, c.org))
