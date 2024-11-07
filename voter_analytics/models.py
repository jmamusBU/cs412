from django.db import models

# Create your models here.

class Voter(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    address_number = models.IntegerField()
    address_street = models.TextField()
    address_apt = models.TextField()
    address_zip = models.IntegerField()
    dob = models.DateField()
    dor = models.DateField()
    party = models.TextField()
    precinct = models.TextField()
    state = models.TextField()
    v21town = models.BooleanField()
    primary = models.BooleanField()
    general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    Voter.objects.all().delete()
    
    filename = '/Users/joseamusategui/Desktop/django/newton_voters.csv'
    
    f = open(filename)
    headers = f.readline()
    def get_bool(s):
        if s == "FALSE":
            return False
        else:
            return True
    
    for line in f:
        try:
            fields = line.split(',')
            
            result = Voter(
                    last_name = fields[1],
                    first_name = fields[2],
                    
                    address_number = int(fields[3]),
                    address_street = fields[4],
                    address_apt = fields[5],
                    address_zip = fields[6],
                    dob = fields[7],
                    dor = fields[8],
                    party = fields[9],
                    precinct = fields[10],
                    state = get_bool(fields[11]),
                    v21town = get_bool(fields[12]),
                    primary = get_bool(fields[13]),
                    general = get_bool(fields[14]),
                    v23town = get_bool(fields[15]),
                    voter_score = fields[16]
                    )
            result.save()
            print(f'Created: {result}')
          
        except:
            print(f'Exception: {fields}')
        
    