from django.shortcuts import render
from .models import UserData

# Validacion de datos:
import re

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login(request):
    # Lógica para el inicio de sesión
    return render(request, 'login.html')

from django.shortcuts import render
from .models import UserData

def signup(request):
    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        retypedPassword = request.POST["retypePassword"]

        print(checkUsername(username))

        if password == retypedPassword:
            datauser = UserData()
            datauser.username = username
            datauser.password = password
            datauser.save()

    return render(request, 'signup.html')

def checkUsername(username):
    if checkIfUsernameIsEmpty(username):
        return "El nombre de usuario no puede estar vacio"

    if checkUsernameLen(username):
        return "El nombre de usuario debe ser minimo de 5 letras"

    if checkIfUsernameHasSymbols(username):
        return "El nombre de usuario no puede contener símbolos"



def checkIfUsernameIsEmpty(username):
    return username == ""

def checkUsernameLen(username):
    return len(username) < 5

def checkIfUsernameHasSymbols(username):
    pattern = "^[a-zA-Z0-9]+$"
    re.match(pattern, username)
