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
        current_pos = 1
        if PatientQueue.objects.filter(date_enqueued=datetime.today).exists():
            current_pos = PatientQueue.objects.filter(date_enqueued=datetime.today).order_by('queue_position').last().queue_position +1
        
        queue = PatientQueue.objects.create(
            patient = PatientDetails.objects.get(patient_ID=request.POST.get('patient_ID')),
            queue_position = current_pos
        )
        queue.save()
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
    if request.method == 'POST':
        queue_entry = PatientQueue.objects.order_by('queue_position').first()

        if queue_entry:
            return JsonResponse({"message": "Patient called", "patient_id": str(queue_entry.patient.patient_ID)}, status=200)

        return JsonResponse({"error": "Queue is empty"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=400)


def get_patient_details(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')

        if not patient_id:
            return JsonResponse({"error": "patient_id is required"}, status=400)

        patient = get_object_or_404(PatientDetails, patient_ID=patient_id)

        patient_data = {
            "user_id": str(patient.user.user_id),
            "email": patient.user.email,
            "first_name": patient.user.first_name,
            "last_name": patient.user.last_name,
            "weight": patient.weight,
            "height": patient.height,
            "temperature": patient.temperature,
            "blood_pressure": patient.blood_pressure,
            "BMI": patient.BMI,
            "blood_sugar": patient.blood_sugar,
            "symptoms": patient.symptoms,
            "date_visited": patient.date_visited.strftime("%d-%m-%Y"),
            "date_treated": patient.date_treated.strftime("%d-%m-%Y") if patient.date_treated else None,
        }

        return JsonResponse(patient_data, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=400)


def prescribe(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        medicine = request.POST.get('medicine')
        dosage = request.POST.get('dosage')
        instructions = request.POST.get('instructions')

        if not patient_id or not medicine or not dosage or not instructions:
            return JsonResponse({"error": "All fields are required: patient_id, medicine, dosage, instructions"}, status=400)

        patient = get_object_or_404(PatientDetails, patient_ID=patient_id)

        prescription = Prescription.objects.create(
            patient=patient,
            medicine=medicine,
            dosage=dosage,
            instructions=instructions
        )

        return JsonResponse({"message": "Prescription added successfully", "prescription_id": str(prescription.prescription_ID)}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=400)