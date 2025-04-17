from django.db import models
from django.db import models

class Mark(models.Model):
    module_code = models.CharField(max_length=10)
    module_name = models.CharField(max_length=100)
    cw1 = models.IntegerField()
    cw2 = models.IntegerField()
    cw3 = models.IntegerField()
    student_id = models.CharField(max_length=10)
    student_name = models.CharField(max_length=100)
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date = models.DateField()

    def total_marks(self):
        return self.cw1 + self.cw2 + self.cw3

# Create your models here.
