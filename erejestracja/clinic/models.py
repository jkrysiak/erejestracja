from django.db import models

# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    telephone = models.CharField(max_length=12)
    address = models.CharField(max_length=100)
    birthday = models.DateField()

    def __str__(self):
       return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    telephone = models.CharField(max_length=12)
    address = models.CharField(max_length=100)
    birthday = models.DateField()
    specialization = models.CharField(max_length=50)
    npwz = models.CharField(max_length=10)

    def __str__(self):
       return self.name

class Appoitment(models.Model):
    doctorname = models.CharField(max_length=50)
    patientname = models.CharField(max_length=50)
    doctoremail = models.EmailField(max_length=50)
    patientemail = models.EmailField(max_length=50)
    appoitmentdate = models.DateField()
    appoitmenttime = models.TimeField()
    symptoms = models.CharField(max_length=100)
    exam = models.CharField(max_length=200)
    status = models.BooleanField()

    def __str__ (self):
        return self.patientname+" masz wizytę z "+self.doctorname+" "+str(self.appoitmentdate)