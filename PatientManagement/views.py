from django.shortcuts import render,HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("<h1 style='text-align:center;'>This is patient home</h1>")