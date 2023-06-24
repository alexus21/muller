from django.shortcuts import render

from mullerMethod.documento.ppp import Muller
from django.contrib.auth.models import User
from django.contrib import messages


# Vista principal para la página de inicio
def index(request):
    if request.method == "POST":
        # Verifica si se ha hecho clic en el botón "signupButton"
        if "signupButton" in request.POST:
            username, email, password, status = signUpToSite(request)
            if status:
                return render(request, "muller.html",
                              context={"username": username, "email": email, "password": password})

        # Verifica si se ha hecho clic en el botón "loginButton"
        if "loginButton" in request.POST:
            username, email, password, status = loginToSite(request)
            if status:
                return render(request, "muller.html",
                              context={"username": username, "email": email, "password": password})

        # Verifica si se ha hecho clic en el botón "recoverPassButton"
        if "recoverPassButton" in request.POST:
            status = resetPassword(request)
            if status:
                return render(request, "index.html")

        # Verifica si se ha hecho clic en el botón "findRoots"
        if "findRoots" in request.POST:

            data = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 0.5, 0.1]]
            data = getMullerDataa(request)
            return render(request, 'index.html', {'data': data})


    return render(request, "index.html")


# Vista para la página muller.html
def muller(request, username, email, password):
    if request.method == "POST":
        # Verifica si se ha hecho clic en el botón "updateProfileButton"
        if "updateProfileButton" in request.POST:
            status = updateUserData(request)
            if status:
                return render(request, "index.html")

        # Verifica si se ha hecho clic en el botón "findRoots"
        if "findRoots" in request.POST:
            data = {
                "x0": [1, 2, 3],
                "x1": [4, 5, 6],
                "x2": [7, 8, 9],
                "e": [1, 0.5, 0.1]
            }
            data = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 0.5, 0.1]]
            return render(request, 'muller.html', {'data': data})



    return render(request, "muller.html", context={"username": username, "email": email, "password": password})


def iterations(request):
    return render(request, "iterations.html")


# Función para registrar un nuevo usuario
def signUpToSite(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    retypedPassword = request.POST.get("retypePassword")

    if checkIfUserExist(username, None) or checkIfUserExist(None, email):
        messages.error(request, "Nombre de usuario o correo electrónico ya registrado")
        return "", "", "", False

    if password != retypedPassword:
        messages.error(request, "Las contraseñas no coinciden")
        return "", "", "", False

    # Crea un nuevo objeto de usuario en la base de datos `auth_user` de Django
    data = User.objects.create_user(username=username, password=password, email=email, is_staff=False,
                                    is_superuser=False, is_active=True)
    data.save()
    # Devuelve el nombre de usuario, correo electrónico, contraseña y True para indicar
    # que el registro fue exitoso
    return username, email, password, True


# Función para iniciar sesión
def loginToSite(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = User.objects.filter(username=username)

    # Verifica si existe un usuario con el nombre de usuario proporcionado y si la contraseña es correcta
    if not user.exists():
        messages.error(request, "Usuario no registrado")
        return "", "", "", False

    if not user.first().check_password(password):
        messages.error(request, "Contraseña incorrecta")
        return "", "", "", False

    # Obtiene el correo electrónico del primer usuario coincidente
    email = user.first().email
    # Devuelve el nombre de usuario, correo electrónico, contraseña y True
    return username, email, password, True


# Función para actualizar los datos del usuario
def updateUserData(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    retypedPassword = request.POST.get("retypedPassword")

    # Obtiene el objeto myTable
    data = User.objects.get(email=email)

    # Restringe el cambio de datos para root
    if username != "root":
        # Actualiza los datos de usuario según las condiciones establecidas
        if username != "" and password != "" and retypedPassword != "":
            # Verifica si el nombre de usuario no está vacío, no existe un usuario con el mismo nombre de usuario
            # y la contraseña y la contraseña reingresada son iguales

            if password != retypedPassword:
                messages.error(request, "Las contraseñas no coinciden")
                return False

            if not checkIfUserExist(username, None):
                messages.error(request, "Nombre de usuario ya registrado")
                return False

            # Actualiza el nombre de usuario y la contraseña del objeto `data` con los nuevos valores
            data.username = username
            data.set_password(password)
            data.save()
            # Devuelve True para indicar que la actualización de datos fue exitosa
            return True

        # Si el nombre de usuario está vacío
        if username == "":
            # Verifica si la contraseña y la contraseña reingresada son iguales
            if password != retypedPassword:
                messages.error(request, "Las contraseñas no coinciden")
                return False

            # Actualiza solo la contraseña del objeto `data` con el nuevo valor
            data.set_password(password)
            data.save()
            # Devuelve True para indicar que la actualización de datos fue exitosa
            return True

        # Si la contraseña o la contraseña reingresada están vacías
        if password == "" or retypedPassword == "":
            # Verifica si se ha proporcionado un nombre de usuario no vacío
            # o si no existe un usuario con el mismo nombre de usuario
            if not checkIfUserExist(username, None):
                messages.error(request, "Nombre de usuario ya registrado")
                return False

            # Actualiza solo el nombre de usuario del objeto `data` con el nuevo valor
            data.username = username
            data.save()
            # Devuelve True para indicar que la actualización de datos fue exitosa
            return True

    return False


# Función para restablecer la contraseña
def resetPassword(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    retypedPassword = request.POST.get("retypedPassword")

    data = User.objects.get(email=email)

    # Verifica si existe un usuario con el correo electrónico proporcionado
    if User.objects.filter(email=email).exists():
        # Verifica si se han proporcionado contraseñas válidas
        if password != "" and retypedPassword != "":
            # Verifica si las contraseñas coinciden
            if password == retypedPassword:
                # Actualiza la contraseña del usuario con la nueva contraseña proporcionada
                data.set_password(password)
                data.save()
                # Devuelve True para indicar que la contraseña se restableció correctamente
                return True
    return False


def checkIfUserExist(username, email):
    # Verifica si el usuario existe o no en la base de datos
    if username and email:
        return User.objects.filter(username=username, email=email).exists()

    if username:
        return User.objects.filter(username=username).exists()

    if email:
        return User.objects.filter(email=email).exists()


def getMullerDataa(request):
        equation = request.POST.get("getEquation")
        x0 = float(request.POST.get("getX0"))
        x1 = float(request.POST.get("getX1"))
        x2 = float(request.POST.get("getX2"))
        marginError = float(request.POST.get("getMarginOfError"))

        return Muller(equation, x0, x1, x2, marginError).iteraciones()
