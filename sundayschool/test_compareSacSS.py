import unittest
from unittest.mock import Mock, patch
from compareSacSS import CompareSacSS
from pathlib import Path


class TestSacSS (unittest.TestCase):

    def setUp(self):
        # print('setUp ' + str(self))
        self.csss = CompareSacSS()

    def tearDown(self):
        # print('tearDown ' + str(self))
        pass

    @patch('compareSacSS.CompareSacSS.readSac')
    @patch('compareSacSS.CompareSacSS.readSS')
    @patch('compareSacSS.CompareSacSS.readCallings')
    def test_read_input_files(self, mock_calls, mock_ss, mock_sac):
        # print('test_read_input_files')
        self.csss.read_input_files()    # triggers calls of mock methods.
        # ensure that the three methods were called in read_input_files().
        mock_sac.assert_called_once_with(CompareSacSS.sacCsv)
        mock_ss.assert_called_once_with(CompareSacSS.ssCsv)
        mock_calls.assert_called_once()

    def test_readSac(self):
        # print('test_readSac')

        filename = Path(CompareSacSS.sacCsv)
        self.assertTrue(filename.exists())

        self.csss.readSac(CompareSacSS.sacCsv)

        self.assertTrue(len(self.csss.sac_roll) > 10) # ~650


    def test_readSS(self):
        # print('test_readSS')
        filename = Path(CompareSacSS.ssCsv)
        self.assertTrue(filename.exists()) 

        self.csss.readSS(CompareSacSS.ssCsv) 

        self.assertTrue(len(self.csss.ss_roll) > 0)


    def test_readCallings(self):
        # print('test_readCallings')
        
        filename = Path(CompareSacSS.callCsv)
        self.assertTrue(filename.exists())
        
        self.csss.readCallings(CompareSacSS.callCsv)
        self.assertTrue(len( self.csss.call_roll) > 0) 


    def test_captureDatesLimitSacList(self):
        dates = ['13-Oct', '20-Oct', '27-Oct', '3-Nov', '10-Nov', '17-Nov',
              '24-Nov', '1-Dec', '8-Dec', '15-Dec', '22-Dec', '29-Dec']
        csss = CompareSacSS()

        csss.readSac('testSac.csv')
        
        csss.captureDatesLimitSacList()
        
        self.assertEqual(csss.attendance, dates)
        # print(len(self.csss.sac_roll))
        #print('length: {}'.format(len(csss.sac_roll)) )
        self.assertTrue(len(csss.sac_roll) > 100)
           
    @patch('compareSacSS.CompareSacSS.adltNamesAttendedSac')
    @patch('compareSacSS.CompareSacSS.adultNamesAttendedSS')
    def test_MissedSS(self, mock_ssAdults, mock_sacAdults):
        # print('test_missedSS')
        mock_ssAdults.returns({'Boops, Betty'})
        mock_sacAdults.returns({'Brooks, Garth','Boops, Betty','Gable, Clark'})
        self.csss.called = {'Gable, Clark'}
        
        # test week 1, which is a SS Week
        self.csss.missedSS(1)

        mock_sacAdults.assert_called_with(1)
        mock_ssAdults.assert_called_with(1)
        ln = len(self.csss.skipped)
        #print('numberSkipped: {}'.format(ln))
        self.assertTrue(1, ln)
   
    

if __name__ == '__main__':
    unittest.main()
