from django.db import models
from DoctorApplication.models import CustomUser
from uuid import uuid4
# Create your models here.


class PatientDetails(models.Model):
    patient_ID = models.UUIDField(default=uuid4,primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_details')
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    temperature = models.FloatField()
    blood_pressure = models.CharField(max_length=15)
    BMI = models.FloatField()
    O2_level = models.FloatField()
    symptoms = models.TextField()
    date_visited = models.DateField()
    date_treated = models.DateField(null=True, blank=True)
class Meta:
       db_table='Patient_details'
class PatientQueue(models.Model):
    patient_details = models.OneToOneField(PatientDetails, on_delete=models.CASCADE, related_name='queue')
    queue_position = models.IntegerField()
    date_enqueued = models.DateTimeField()
    time_expired = models.DateTimeField(null=True, blank=True)
class Meta:
       db_table='Patient_queue'    

    # def __str__(self):
    #     return f"Queue Position {self.queue_position} for Patient {self.patient_details.user.email}"

class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    patient_details = models.ForeignKey(PatientDetails, on_delete=models.CASCADE, related_name='prescriptions')
    date_generated = models.DateField()
    date_valid_upto = models.DateField()

    # def __str__(self):
    #     return f"Prescription {self.prescription_id} for Patient {self.patient_details.user.email}"
class Meta:
       db_table='Prescription'    

class Medicines(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    composition = models.TextField()
    company = models.CharField(max_length=100)

class Meta:
       db_table='medicines'

class Tests(models.Model):
    test_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    test_type = models.CharField(max_length=50)  # Example: "blood", "serum", etc.
    prep_condition = models.TextField()

class Meta:
       db_table='tests'


