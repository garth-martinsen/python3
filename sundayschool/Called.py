class Called:
    def __init__(self, row):
        '''Initialize a record with name,org'''
      #  print(row)
        self.name = row[0].strip()
        self.org = row[1].strip()

    def __repr__(self):
        return '{}, {} \r'.format(
            self.name, self.org)
