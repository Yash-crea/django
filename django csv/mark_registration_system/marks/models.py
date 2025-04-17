from django.db import models

class MarkEntry(models.Model):
    module_code = models.CharField(max_length=20)
    module_name = models.CharField(max_length=100)
    cw1 = models.DecimalField(max_digits=5, decimal_places=2)
    cw2 = models.DecimalField(max_digits=5, decimal_places=2)
    cw3 = models.DecimalField(max_digits=5, decimal_places=2)
    student_id = models.CharField(max_length=20)
    student_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    date_of_entry = models.DateField()

    def __str__(self):
        return f"{self.module_code} - {self.student_name}"
