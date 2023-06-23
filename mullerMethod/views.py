from django.shortcuts import render
from .models import UserData
from django.contrib.auth.models import User


def index(request):
    if request.method == "POST":
        if "signup" in request.POST:
            username, email, password, status = signUpToSite(request)
            if status:
                return render(request, "muller.html", context={"username": username, "email": email, "password": password})

        if "login" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = User.objects.filter(username=username)

            if user.exists() and user.first().check_password(password):
                email = user.first().email
                return render(request, "muller.html", context={"username": username, "password": password, "email": email})

        if "recoverPassButton" in request.POST:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            retypedPassword = request.POST.get("retypedPassword")

            if username != "" or email != "" or password != "" or retypedPassword != "":
                if password == retypedPassword:
                    resetPassword(username, email, password)
                    return render(request, "index.html")

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


def signUpToSite(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    retypedPassword = request.POST.get("retypePassword")

    if username != "" or email != "" or password != "" or retypedPassword != "":
        if password == retypedPassword:
            if not checkIfUserDoNotExist(username, email):
                # Guarda los datos de usuario en la base de datos auth_user de Django.
                data = User.objects.create_user(username=username, password=password, email=email, is_staff=False, is_superuser=False, is_active=True)
                data.save()
                return username, email, password, True


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


def resetPassword(username, email, password):
    # Actualiza los datos del usuario en la base de datos.
    # Crea el objeto myTable
    user = User.objects.get(email=email)

    # Actualiza clave
    user.username = username
    user.password = password

    # Los inserta
    user.save()


def checkIfUserDoNotExist(username, email):
    #Verifica si el usuario existe o no en la base de datos.
    return User.objects.filter(username=username).exists() or User.objects.filter(email=email)
