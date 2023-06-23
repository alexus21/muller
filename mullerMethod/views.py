from django.shortcuts import render
from mullerMethod.muller_algorithm import getMullerData
from django.contrib.auth.models import User


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
            getMullerData(request)

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
            getMullerData(request)

    return render(request, "muller.html", context={"username": username, "email": email, "password": password})


# Función para registrar un nuevo usuario
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


# Función para iniciar sesión
def loginToSite(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = User.objects.filter(username=username)

    if user.exists() and user.first().check_password(password):
        email = user.first().email
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
        if username != "" and password != "" and retypedPassword != "":
            if username != "" or checkIfUserDoNotExist(username, "") and password == retypedPassword:
                data.username = username
                data.set_password(password)
                data.save()
                return True

        if username == "":
            if password == retypedPassword:
                data.set_password(password)
                data.save()
                return True

        if password == "" or retypedPassword == "":
            if username != "" or checkIfUserDoNotExist(username, ""):
                data.username = username
                data.save()
                return True
    return False


# Función para restablecer la contraseña
def resetPassword(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    retypedPassword = request.POST.get("retypedPassword")

    data = User.objects.get(email=email)

    if User.objects.filter(email=email).exists():
        if password != "" and retypedPassword != "":
            if password == retypedPassword:
                data.set_password(password)
                data.save()
                return True
    return False


# Función para verificar si el usuario existe
def checkIfUserDoNotExist(username, email):
    # Verifica si el usuario existe o no en la base de datos
    if username and email:
        return User.objects.filter(username=username).exists() or User.objects.filter(email=email)

    if username and email == "":
        return User.objects.filter(username=username).exists()

    if username == "" and email:
        return User.objects.filter(email=email).exists()
