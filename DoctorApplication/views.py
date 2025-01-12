from django.shortcuts import render
from django.http import JsonResponse
from .models import CustomUser
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
# Create your views here.

def get_csrf(request):
    csrf_token = get_token(request)  
    return JsonResponse({"csrf":csrf_token},status=200)

@csrf_exempt
def signin(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request,email=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message":"success","data": {"user_type":user.user_type}},status=200)
        else:
            return JsonResponse({"message":"Invalid email or Password", "status":"error"},status=404)
    return render(request, "signin.html")