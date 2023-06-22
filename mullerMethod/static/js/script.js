document.addEventListener("DOMContentLoaded", function (){
    //Botones de la navbar
    const btnLoginNav = document.querySelector("[data-login-btn-nav]");
    const btnSignupNav = document.querySelector("[data-signup-btn-nav]");

    //For signup
    const btnSignup = document.querySelector("[data-signup-button]");
    const inputUsername = document.querySelector("[data-username-signup]")
    const inputPassword = document.querySelector("[data-password-signup]");
    const inputRetypedPassword = document.querySelector("[data-retyped-password-signup]");

    //For login
    const btnLogin = document.querySelector("[data-login-button]");

    //Nombre de usuario a mostrar en la navbar
    const loggedUsername = document.querySelector("[data-username-logged]");

    const enableButton = () => {
        btnSignup.disabled = false;
    };

    const disableButton = () => {
        btnSignup.disabled = true;
    }

    btnSignup.addEventListener("click", function (){
        event.preventDefault();

        // Datos del formulario
        const username = inputUsername.value;
        const password = inputPassword.value;
        const retypedPassword = inputRetypedPassword.value;

        // Regex para validar nombre de usuario
        const availableChars = "~`!@#$%^&*()+={[}]|\\:;\"'<,>.?-";
        const dash = /-/;
        const regex = new RegExp(`[${availableChars}]`);

        if(!username){
            alert("El nombre de usuario es requerido");
            disableButton();
            return;
        }

        if(username.length < 5){
            alert("El nombre de usuario es muy corto");
            disableButton();
            return;
        }

        if(regex.test(username) || dash.test(username)){
            alert("El nombre de usuario no debe contener caracteres especiales");
            disableButton();
            return;
        }

        if(!password || !retypedPassword){
            alert("La clave es requerida");
            disableButton();
            return;
        }

        if(password.length < 5 || retypedPassword.length < 5){
            alert("La clave es demasiado corta");
            disableButton();
            return;
        }

        if(password  !== retypedPassword){
            alert("Las claves no son iguales");
            disableButton();
            return;
        }

        alert("Registrado correctamente");
        btnSignupNav.classList.add("d-none");
        btnLoginNav.classList.add("d-none");
        loggedUsername.textContent = "Bienvenido, " + username;

        inputUsername.value = "";
        inputPassword.value = "";
        inputRetypedPassword.value = "";
    });

    inputUsername.addEventListener("input", enableButton);
    inputPassword.addEventListener("input", enableButton);
    inputRetypedPassword.addEventListener("input", enableButton);
});
