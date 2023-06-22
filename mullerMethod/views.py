from django.shortcuts import render
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
                        return render(request, "muller.html", context={"username": username, "password": password})

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
    if request.method == "POST":
        if "updateProfile" in request.POST:
            oldUsername = request.POST.get("oldUsername")
            newUsername = request.POST.get("newUsername")
            password = request.POST.get("password")
            retypedPassword = request.POST.get("retypePassword")

            if newUsername != "":
                if password == retypedPassword:
                    if not checkIfUserDoNotExist(newUsername):
                        updateData(oldUsername, newUsername, password)
                        return render(request, "index.html")

        if "findRoots" in request.POST:
            equation = request.POST.get("getEquation")
            x0 = request.POST.get("getX0")
            x1 = request.POST.get("getX1")
            x2 = request.POST.get("getX2")
            marginError = request.POST.get("getMarginOfError")

    return render(request, "muller.html", context={"username": username, "password": password})


def saveToDatabase(username, password):
    # Guarda los datos de usuario en la base de datos.

    data = UserData(username=username, password=password)
    data.save()
    print("Saved")


def updateData(oldUsername, newUsername, password):
    # Actualiza los datos del usuario en la base de datos.
    # Crea el objeto myTable
    myTable = UserData.objects.get(username=oldUsername)

    # Actualiza los valores
    myTable.username = newUsername
    myTable.password = password

    # Los inserta
    myTable.save()
    print("Actualizado correctamente")


def checkIfUserDoNotExist(username):
    #Verifica si el usuario existe o no en la base de datos.
    return UserData.objects.filter(username=username).exists()
