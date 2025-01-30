from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from DoctorApplication.models import CustomUser
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import PatientDetails, PatientQueue, Medicines, Tests, Prescription
import json

from datetime import datetime



@csrf_exempt
def register_patient(request):
    if request.method == 'POST':
        # Get the fields from the request
        email = request.POST.get('email', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        date_of_birth = request.POST.get('date_of_birth', '')
        
        # Validate input fields
        if not email or not first_name or not last_name or not date_of_birth:
            return JsonResponse({"error": "Email, First Name, Last Name, and Date of Birth are required fields."}, status=400)

        try:
            date_of_birth = datetime.strptime(date_of_birth, "%d-%m-%Y")
        except ValueError:
            return JsonResponse({"error": "Invalid Date of Birth format. Please use dd-mm-yyyy."}, status=400)

        # Handle user creation or fetching
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth
            )
            user.set_password("password@123")
            user.save()

        # Get other fields from the request and handle any missing/invalid data
        try:
            weight = float(request.POST.get('weight', '0'))
            height = float(request.POST.get('height', '0'))
            temperature = float(request.POST.get('temperature', '0'))
            blood_pressure = request.POST.get('blood_pressure', '')
            BMI = float(request.POST.get('BMI', '0'))
            O2level = float(request.POST.get('O2level', '0'))
            blood_sugar = float(request.POST.get('blood_sugar', '0'))
            symptoms = request.POST.get('symptoms', '')
            date_visited = request.POST.get('date_visited', '')

            # Validate date_visited
            if not date_visited:
                return JsonResponse({"error": "Date of visit is required."}, status=400)

            date_visited = datetime.strptime(date_visited, "%d-%m-%Y")
        except ValueError:
            return JsonResponse({"error": "Invalid number format. Please ensure numeric fields like weight, height, etc., are correct."}, status=400)

        # Calculate age based on date_visited and date_of_birth
        age = (date_visited - date_of_birth).days / 365.25

        # Create the PatientDetails record
        patient = PatientDetails.objects.create(
            user=user,
            age=round(age, 2),
            weight=weight,
            height=height,
            temperature=temperature,
            blood_pressure=blood_pressure,
            BMI=BMI,
            O2level=O2level,
            blood_sugar=blood_sugar,
            symptoms=symptoms,
            date_visited=date_visited
        )
        patient.save()

        # Return success response
        return JsonResponse({"message": "Patient registered successfully", "patient_id": str(patient.patient_ID)}, status=200)
    
    # Handle invalid method
    return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)

@csrf_exempt
def enqueue_patient(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_ID')
        
        if not patient_id:
            return JsonResponse({"error": "Patient ID is required"}, status=400)

        patient = get_object_or_404(PatientDetails, patient_ID=patient_id)

        today = now().date()  # Get the current date in a timezone-aware way

        # Get the last queue position for today's date
        last_queue_entry = PatientQueue.objects.filter(date_enqueued=today).order_by('queue_position').last()
        
        # If no entry exists, start from 1; otherwise, increment
        current_pos = 1 if not last_queue_entry else last_queue_entry.queue_position + 1

        queue_entry = PatientQueue.objects.create(
            patient=patient,
            queue_position=current_pos,
            date_enqueued=today
        )

        return JsonResponse({"message": "Patient enqueued successfully", "queue_position": queue_entry.queue_position}, status=200)
    
    return JsonResponse({"error": "Invalid request method"}, status=400)



@csrf_exempt
def dequeue_patient(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_ID')

        if not patient_id:
            return JsonResponse({"error": "Patient ID is required"}, status=400)

        patient_queue_entry = PatientQueue.objects.filter(patient__patient_ID=patient_id).first()

        if not patient_queue_entry:
            return JsonResponse({"error": "Patient not found in queue"}, status=404)

        patient_queue_entry.delete()

        return JsonResponse({"message": "Patient dequeued successfully"}, status=200)
    
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