from django.urls import path
from . import views

urlpatterns = [
    path('register_patient',views.register_patient,name='register_patient'),
    path('enqueue_patient', views.enqueue_patient, name='enqueue_patient'),
    path('dequeue_patient', views.dequeue_patient, name='dequeue_patient'),
    path('call_patient', views.call_patient, name='call_patient'),
    path('get_patient_details', views.get_patient_details, name='get_patient_details'),
    path('prescribe', views.prescribe, name='prescribe'),  
]