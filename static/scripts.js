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

        const nombreRegex = /^[a-zA-ZáéíóúÁÉÍÓÚüÜ]{2,24}$/;
        const apellidoRegex = /^[a-zA-ZáéíóúÁÉÍÓÚüÜ]{2,32}$/;
        const usuarioRegex = /^[a-zA-Z0-9]{4,16}$/;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const contraseñaRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,15}$/;

        const errorNombre = document.getElementById('error-name');
        const errorApellido = document.getElementById('error-surname');
        const errorUsuario = document.getElementById('error-userid');
        const errorEmail = document.getElementById('error-usermail');
        const errorPassword = document.getElementById('error-userpassword');
        const errorPasswordRepeat = document.getElementById('error-psw-repeat');

        const marcarError = (input, errorSpan, mensaje) => {
            if (errorSpan) {
                errorSpan.textContent = mensaje;
            }
            input.style.border = '1px solid red';
        };

        const limpiarError = (input, errorSpan) => {
            input.style.border = '';
            if (errorSpan) {
                errorSpan.textContent = '';
            }
        };

        const validarNombre = () => {
            if (nombreInput.value === '') {
                marcarError(nombreInput, errorNombre, 'El campo de nombre se encuentra vacío');
                return false;
            }
            if (!nombreRegex.test(nombreInput.value)) {
                marcarError(nombreInput, errorNombre, 'El nombre no cumple con las condiciones');
                return false;
            }
            limpiarError(nombreInput, errorNombre);
            return true;
        };

        const validarApellido = () => {
            if (apellidoInput.value === '') {
                marcarError(apellidoInput, errorApellido, 'El campo de apellido se encuentra vacío');
                return false;
            }
            if (!apellidoRegex.test(apellidoInput.value)) {
                marcarError(apellidoInput, errorApellido, 'El apellido no cumple con las condiciones');
                return false;
            }
            limpiarError(apellidoInput, errorApellido);
            return true;
        };

        const validarUsuario = () => {
            if (usuarioInput.value === '') {
                marcarError(usuarioInput, errorUsuario, 'El campo de usuario se encuentra vacío');
                return false;
            }
            if (!usuarioRegex.test(usuarioInput.value)) {
                marcarError(usuarioInput, errorUsuario, 'El usuario no cumple con las condiciones');
                return false;
            }
            limpiarError(usuarioInput, errorUsuario);
            return true;
        };

        const validarEmail = () => {
            if (emailInput.value === '') {
                marcarError(emailInput, errorEmail, 'El campo de email se encuentra vacío');
                return false;
            }
            if (!emailRegex.test(emailInput.value)) {
                marcarError(emailInput, errorEmail, 'El email no cumple con las condiciones');
                return false;
            }
            limpiarError(emailInput, errorEmail);
            return true;
        };

        const validarPassword = () => {
            if (passwordInput.value === '') {
                marcarError(passwordInput, errorPassword, 'El campo de contraseña se encuentra vacío');
                return false;
            }
            if (!contraseñaRegex.test(passwordInput.value)) {
                marcarError(passwordInput, errorPassword, 'La contraseña debe tener entre 8 y 15 caracteres, incluir mayúsculas, minúsculas y al menos un número');
                return false;
            }
            limpiarError(passwordInput, errorPassword);
            return true;
        };

        const validarPasswordRepeat = () => {
            if (passwordRepeatInput.value === '') {
                marcarError(passwordRepeatInput, errorPasswordRepeat, 'El campo de repetir contraseña se encuentra vacío');
                return false;
            }
            if (passwordInput.value !== passwordRepeatInput.value) {
                marcarError(passwordRepeatInput, errorPasswordRepeat, 'Las contraseñas no coinciden');
                return false;
            }
            limpiarError(passwordRepeatInput, errorPasswordRepeat);
            return true;
        };

        // Validación al salir de cada campo (on blur)
        nombreInput.addEventListener('blur', validarNombre);
        apellidoInput.addEventListener('blur', validarApellido);
        usuarioInput.addEventListener('blur', validarUsuario);
        emailInput.addEventListener('blur', validarEmail);
        passwordInput.addEventListener('blur', validarPassword);
        passwordRepeatInput.addEventListener('blur', validarPasswordRepeat);

        if (submitBtn) {
            submitBtn.addEventListener('click', () => {
                const esValido =
                    validarNombre() &&
                    validarApellido() &&
                    validarUsuario() &&
                    validarEmail() &&
                    validarPassword() &&
                    validarPasswordRepeat();

                if (!esValido) {
                    alert('Revisá los campos marcados en rojo: falta completar o corregir datos.');
                }
                // El navegador hará el submit normal del formulario
            });
        }
    }
});