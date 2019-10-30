
class SacRecord:
    def __init__(self, row):
        '''Initialize a record with LName,FName,Age,Dates[]'''

        self.name = row[1]
        self.age = row[2]
        self.attendance = row[3:]

    def __repr__(self):
        return '{}, {}, {}'.format(
            self.name, self.age, str(self.attendance))
