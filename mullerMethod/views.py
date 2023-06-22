from django.shortcuts import render, redirect
from .models import UserData


def index(request):
    if request.method == "POST":
        if "signup" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            retypedPassword = request.POST.get("retypePassword")

            if username != "":
                print(username)
                if password == retypedPassword:
                    print(password)
                    if not checkIfUserDoNotExist(username):
                        saveToDatabase(username, password)
                    else:
                        print("Este usuario ya existe")
                else:
                    print("Las claves no son iguales")
            else:
                print("El nombre de usuario es requerido")

        if "login" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")

            if UserData.objects.filter(username=username).exists() and UserData.objects.filter(password=password):
                return render(request, "muller.html", context={"username": username, "password": password})

        if "findRoots" in request.POST:
            equation = request.POST.get("getEquation")
            x0 = request.POST.get("getX0")
            x1 = request.POST.get("getX1")
            x2 = request.POST.get("getX2")
            marginError = request.POST.get("getMarginOfError")

    return render(request, "index.html")


def muller(request, username, password):
    if "findRoots" in request.POST:
        equation = request.POST.get("getEquation")
        x0 = request.POST.get("getX0")
        x1 = request.POST.get("getX1")
        x2 = request.POST.get("getX2")
        marginError = request.POST.get("getMarginOfError")

    return render(request, "muller.html")


def saveToDatabase(username, password):
    data = UserData(username=username, password=password)
    data.save()
    print("Saved")


def checkIfUserDoNotExist(username):
    return UserData.objects.filter(username=username).exists()