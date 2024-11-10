from django.db import models
from django.db.models import Max, Min

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
    state = models.BooleanField()
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
                    last_name = fields[1].strip(),
                    first_name = fields[2].strip(),
                    
                    address_number = int(fields[3].strip()),
                    address_street = fields[4].strip(),
                    address_apt = fields[5].strip(),
                    address_zip = fields[6].strip(),
                    dob = fields[7].strip(),
                    dor = fields[8].strip(),
                    party = fields[9].strip(),
                    precinct = fields[10].strip(),
                    state = get_bool(fields[11].strip()),
                    v21town = get_bool(fields[12].strip()),
                    primary = get_bool(fields[13].strip()),
                    general = get_bool(fields[14].strip()),
                    v23town = get_bool(fields[15].strip()),
                    voter_score = int(fields[16].strip())
                    )
            result.save()
            print(f'Created: {result}')
          
        except:
            print(f'Exception: {fields}')
        
    