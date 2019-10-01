
class SacRecord:
    def __init__(self, row):
        '''Initialize a record with LName,FName,Age,Dates[]'''

        self.Name = row[1]
        self.Age = row[2]
        self.dates = row[3:]

    def __repr__(self):
        return '{}, {}, {}'.format(
            self.Name, self.Age, str(self.dates))
