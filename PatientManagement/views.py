from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from DoctorApplication.models import CustomUser
from .models import PatientDetails, PatientQueue, Medicines, Tests, Prescription
import json
from datetime import datetime
@csrf_exempt
def register_patient(request):
    if request.method == 'POST':
        #data = json.loads(request.body)
        email = request.POST.get('email','')
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        date_of_birth = request.POST.get('date_of_birth','')
        date_of_birth = datetime.strptime(date_of_birth,"%d-%m-%Y")
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(email=email,first_name=first_name,last_name=last_name,date_of_birth=date_of_birth)
            user.set_password("password@123")
            user.save()
        
        weight = request.POST.get('weight','')
        height = request.POST.get('height','')
        temperature = request.POST.get('temperature','')
        blood_pressure = request.POST.get('blood_pressure','')
        BMI = request.POST.get('BMI','')
        O2level = request.POST.get('O2level','')
        blood_sugar = request.POST.get('blood_sugar','')
        symptoms = request.POST.get('symptoms','')
        date_visited = request.POST.get('date_visited','')
        
        date_visited = datetime.strptime(date_visited,"%d-%m-%Y")

        age = date_visited - date_of_birth
        patient = PatientDetails.objects.create(
            user=user,
            age = round(age.days/365,2),
            weight = weight,
            height = height,
            temperature = temperature,
            blood_pressure = blood_pressure,
            BMI = BMI,
            O2level = O2level,
            blood_sugar = blood_sugar,
            symptoms = symptoms,
            date_visited = date_visited
        )
        patient.save()
        #date_treated=request.POST.get('date_treated','')
        
        return JsonResponse({"message": "Patient registered successfully", "patient_id": str(patient.patient_ID)}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)


def enqueue_patient(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        patient = get_object_or_404(PatientDetails, patient_ID=data.get('patient_id'))
        PatientQueue.objects.create(
            patient=patient,
            queue_position=data.get('queue_position')
        )
        return JsonResponse({"message": "Patient added to queue"}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)


def dequeue_patient(request):
    if request.method == 'POST':
        queue_entry = PatientQueue.objects.order_by('queue_position').first()
        if queue_entry:
            queue_entry.delete()
            return JsonResponse({"message": "Patient dequeued", "patient_id": str(queue_entry.patient.patient_ID)}, status=200)
        return JsonResponse({"error": "Queue is empty"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)


def call_patient(request):
    if request.method == 'GET':
        queue_entry = PatientQueue.objects.order_by('queue_position').first()
        if queue_entry:
            return JsonResponse({"message": "Patient called", "patient_id": str(queue_entry.patient.patient_ID)}, status=200)
        return JsonResponse({"error": "Queue is empty"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)


def get_patient_details(request):
    if request.method == 'GET':
        patient_id = request.GET.get('patient_id')
        patient = get_object_or_404(PatientDetails, patient_ID=patient_id)
        patient_data = {
            "user_id": patient.user_id,
            "weight": patient.weight,
            "height": patient.height,
            "temperature": patient.temperature,
            "blood_pressure": patient.blood_pressure,
            "BMI": patient.BMI,
            "cholesterol": patient.cholesterol,
            "blood_sugar": patient.blood_sugar,
            "date_visited": patient.date_visited,
            "date_treated": patient.date_treated,
        }
        return JsonResponse(patient_data, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)


def prescribe(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        patient = get_object_or_404(PatientDetails, patient_ID=data.get('patient_id'))
        prescription = Prescription.objects.create(
            patient=patient,
            medicine=data.get('medicine'),
            dosage=data.get('dosage'),
            instructions=data.get('instructions')
        )
        return JsonResponse({"message": "Prescription added successfully", "prescription_id": str(prescription.prescription_ID)}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)