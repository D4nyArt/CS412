# File: models.py
# Author: Daniel Arteaga Mercado (d4nyart@bu.edu), 10/30/2025
# Description: Django models for voter analytics application. Defines
# the Voter model with personal information, address, party affiliation,
# and voting history. Includes function to load voter data from CSV.

from django.db import models

# Create your models here.

class Voter(models.Model):
    """Represents a registered voter in Newton, MA.
    
    Stores voter registration information, address details, party
    affiliation, and participation history in five recent elections.
    """

    voter_id = models.TextField()
    last_name = models.TextField()
    first_name = models.TextField()
    street_num = models.TextField()
    street_name  = models.TextField()
    apt_num = models.TextField()
    zip_code = models.TextField()

    date_birth = models.DateField()
    date_registration = models.DateField()
    party = models.TextField()

    #WATCH OUT (At first glance it looks like an integer, but it can have alpha characters too)
    precinct_num = models.TextField()

    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    voter_score = models.IntegerField()

    def __str__(self):
        """Return string representation of voter with ID and full name."""
        return f"{self.voter_id}: {self.first_name} {self.last_name}"

def load_data():
    """Load voter data from CSV file into Django database.
    
    Reads newton_voters.csv and creates Voter objects for each valid record.
    Handles data type conversions including boolean election participation
    fields and strips whitespace from all text fields.
    """

    filename = '/home/dany/Downloads/newton_voters.csv'


    #Read file
    f = open(filename, 'r')

    #Discard headers
    f.readline()

    for line in f:
        fields = line.split(',')
       
        try:
            # create a new instance of Result object with this record from CSV
            voter = Voter(
                        voter_id = fields[0].strip(),
                        last_name = fields[1].strip(),
                        first_name = fields[2].strip(),
                        street_num = fields[3].strip(),
                        street_name  = fields[4].strip(),
                        apt_num = fields[5].strip(),
                        zip_code = fields[6].strip(),

                        date_birth = fields[7].strip(),
                        date_registration = fields[8].strip(),
                        party = fields[9].strip(),

                        precinct_num = fields[10].strip(),

                        v20state = fields[11].strip().upper() == 'TRUE',
                        v21town = fields[12].strip().upper() == 'TRUE',
                        v21primary = fields[13].strip().upper() == 'TRUE',
                        v22general = fields[14].strip().upper() == 'TRUE',
                        v23town = fields[15].strip().upper() == 'TRUE',

                        voter_score = int(fields[16].strip()),
                    )
 
            voter.save() # commit to database            
        except Exception as e:
            print(f"Skipped: {fields}")
            print(f"Error: {e}")
    
    print(f'Done. Created {Voter.objects.all().count()} Voters.')


            


