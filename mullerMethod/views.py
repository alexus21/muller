from django.shortcuts import render
from .models import UserData
import re
from django.contrib import messages


def index(request):

    if request.method == "POST":
        if "signup" in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')

            if checkUsernameLen(username):
                messages.error(request, "El nombre de usuario es demasiado corto")

            if checkIfUsernameIsEmpty(username):
                messages.error(request, "El nombre de usuario no puede estar vacío")

            if checkIfUsernameHasSymbols(username):
                messages.error(request, "El nombre de usuario no debe contener caracteres especiales")

            else:
                messages.success(request, "Registro completado")

        if "login" in request.POST:
            print("Login")

    return render(request, 'index.html')

def checkIfUsernameIsEmpty(username):
    return username == ""


def checkUsernameLen(username):
    return len(username) < 5


def checkIfUsernameHasSymbols(username):
    pattern = "^[a-zA-Z0-9]+$"
    return not re.match(pattern, username)
