from django.shortcuts import render,HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("<h1 style='text-align:center;'>This is staff home</h1>")
