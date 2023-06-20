from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login(request):
    # Lógica para el inicio de sesión
    return render(request, 'login.html')

def signup(request):
    # Lógica para el registro de usuarios
    return render(request, 'signup.html')
