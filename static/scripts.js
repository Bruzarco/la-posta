// Dropdown de categorías
document.addEventListener('DOMContentLoaded', () => {
    const dropdownHeader = document.querySelector('.dropdownHeader');
    const dropdownCont = document.querySelector('.dropdownCont');

    if (dropdownHeader && dropdownCont) {
        dropdownCont.style.setProperty('position', 'absolute', 'important');
        dropdownCont.style.setProperty('left', '0', 'important');
        dropdownCont.style.setProperty('top', '100%', 'important');
        dropdownCont.style.setProperty('background-color', 'rgb(225, 247, 245)', 'important');
        dropdownCont.style.setProperty('min-width', 'max-content', 'important');
        dropdownCont.style.setProperty('z-index', '99999', 'important');
        dropdownHeader.style.setProperty('position', 'relative', 'important');

        dropdownCont.style.setProperty('display', 'none', 'important');

        const showDropdown = () => {
            dropdownCont.style.setProperty('display', 'flex', 'important');
        };

        const hideDropdown = () => {
            dropdownCont.style.setProperty('display', 'none', 'important');
        };

        dropdownHeader.addEventListener('mouseenter', showDropdown);
        dropdownHeader.addEventListener('mouseleave', hideDropdown);
    }

    // Validación de formulario de login
    const loginForm = document.querySelector('form[data-form="login"]');
    if (loginForm) {
        const submitBtn = loginForm.querySelector('.formSubmit');
        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('contrasena');

        const validateEmail = (email) => {
            return email.match(
                /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            );
        };

        if (submitBtn && emailInput && passwordInput) {
            submitBtn.addEventListener('click', (event) => {
                event.preventDefault();

                emailInput.style.border = '';
                passwordInput.style.border = '';

                if (emailInput.value === '') {
                    alert('El campo de email se encuentra vacío');
                    emailInput.style.border = '1px solid red';
                    return;
                }

                if (passwordInput.value === '') {
                    alert('El campo de contraseña se encuentra vacío');
                    passwordInput.style.border = '1px solid red';
                    return;
                }

                if (!validateEmail(emailInput.value)) {
                    alert('El email no cumple con las condiciones');
                    emailInput.style.border = '1px solid red';
                    return;
                }

                // Si todo está ok, dejamos que el backend procese el login
                loginForm.submit();
            });
        }
    }

    // Validación de formulario de registro
    const signupForm = document.querySelector('form[data-form="signup"]');
    if (signupForm) {
        const submitBtn = document.getElementById('submit');
        const nombreInput = document.getElementById('name');
        const apellidoInput = document.getElementById('surname');
        const usuarioInput = document.getElementById('userid');
        const emailInput = document.getElementById('usermail');
        const passwordInput = document.getElementById('userpassword');
        const passwordRepeatInput = document.getElementById('psw-repeat');

        if (submitBtn && nombreInput && apellidoInput && usuarioInput && emailInput && passwordInput && passwordRepeatInput) {
            submitBtn.addEventListener('click', (event) => {
                event.preventDefault();

                const nombreRegex = /^[a-zA-ZáéíóúÁÉÍÓÚüÜ]{2,24}$/;
                const apellidoRegex = /^[a-zA-ZáéíóúÁÉÍÓÚüÜ]{2,32}$/;
                const usuarioRegex = /^[a-zA-Z0-9]{4,16}$/;
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                const contraseñaRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$/;

                // reset bordes
                nombreInput.style.border = '';
                apellidoInput.style.border = '';
                usuarioInput.style.border = '';
                emailInput.style.border = '';
                passwordInput.style.border = '';
                passwordRepeatInput.style.border = '';

                if (nombreInput.value === '') {
                    alert('El campo de nombre se encuentra vacío');
                    nombreInput.style.border = '1px solid red';
                    return;
                }
                if (apellidoInput.value === '') {
                    alert('El campo de apellido se encuentra vacío');
                    apellidoInput.style.border = '1px solid red';
                    return;
                }
                if (usuarioInput.value === '') {
                    alert('El campo de usuario se encuentra vacío');
                    usuarioInput.style.border = '1px solid red';
                    return;
                }
                if (emailInput.value === '') {
                    alert('El campo de email se encuentra vacío');
                    emailInput.style.border = '1px solid red';
                    return;
                }
                if (passwordInput.value === '') {
                    alert('El campo de contraseña se encuentra vacío');
                    passwordInput.style.border = '1px solid red';
                    return;
                }
                if (passwordRepeatInput.value === '') {
                    alert('El campo de repetir contraseña se encuentra vacío');
                    passwordRepeatInput.style.border = '1px solid red';
                    return;
                }

                if (!nombreRegex.test(nombreInput.value)) {
                    alert('El nombre no cumple con las condiciones');
                    nombreInput.style.border = '1px solid red';
                    return;
                }
                if (!apellidoRegex.test(apellidoInput.value)) {
                    alert('El apellido no cumple con las condiciones');
                    apellidoInput.style.border = '1px solid red';
                    return;
                }
                if (!usuarioRegex.test(usuarioInput.value)) {
                    alert('El usuario no cumple con las condiciones');
                    usuarioInput.style.border = '1px solid red';
                    return;
                }
                if (!emailRegex.test(emailInput.value)) {
                    alert('El email no cumple con las condiciones');
                    emailInput.style.border = '1px solid red';
                    return;
                }
                if (!contraseñaRegex.test(passwordInput.value)) {
                    alert('La contraseña no cumple con las condiciones');
                    passwordInput.style.border = '1px solid red';
                    return;
                }
                if (passwordInput.value !== passwordRepeatInput.value) {
                    alert('Las contraseñas no coinciden');
                    passwordRepeatInput.style.border = '1px solid red';
                    return;
                }

                // Si todo está ok, dejamos que el backend procese el registro
                signupForm.submit();
            });
        }
    }
});