from django.db import models
from DoctorApplication.models import CustomUser
from uuid import uuid4
from django.utils.timezone import now

# Create your models here.


class PatientDetails(models.Model):
    patient_ID = models.UUIDField(default=uuid4,primary_key=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True,blank=True)
    weight = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    height = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    temperature = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    blood_pressure = models.CharField(max_length=50,null=True,blank=True)
    BMI = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    O2level = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    blood_sugar = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    symptoms = models.TextField(null=True,blank=True)
    date_visited = models.DateField(null=True,blank=True)
    date_treated = models.DateField(null=True,blank=True)

    class Meta:
        db_table = 'patient_details'

class PatientQueue(models.Model):
    patient = models.ForeignKey('PatientDetails',on_delete=models.CASCADE,related_name='queue_entries')
    queue_position = models.PositiveIntegerField()
    date_enqueued = models.DateField(default=now)
    time_enqueued = models.TimeField(default=now)

    class Meta:
        db_table = 'patient_queue'

class Medicines(models.Model):
    medicine_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    composition = models.TextField()
    company = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'medicines'

class Tests(models.Model):
    test_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    type_of_test = models.CharField(max_length=50)
    prep_condition = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'tests'

class Prescription(models.Model):
    prescription_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    patient = models.OneToOneField(PatientDetails, on_delete=models.CASCADE, related_name='prescriptions')
    date_generated = models.DateField(default=now)
    date_valid_upto = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'prescriptions'