class Called:
    def __init__(self, row):
        '''Initialize a record with LName,FName,Age,Dates[]'''
        print(row)
        self.name = row[0].strip()
        self.org = row[1].strip()

    def __repr__(self):
        return '{}, {} \r'.format(
            self.name, self.org)
