// Warraq Digital Archives - Client-Side Signup Validation (FR-5)
document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signup-form') || document.querySelector('.auth-card form');
    if (!signupForm) return;

    // Disable default browser tooltip validation to display unified inline errors
    signupForm.setAttribute('novalidate', 'true');

    const usernameInput = document.getElementById('id_username') || signupForm.querySelector('input[name="username"]');
    const emailInput = document.getElementById('id_email') || signupForm.querySelector('input[name="email"]');
    const password1Input = document.getElementById('id_password1') || signupForm.querySelector('input[name="password1"]');
    const password2Input = document.getElementById('id_password2') || signupForm.querySelector('input[name="password2"]');

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    function getErrorContainer(input) {
        const parent = input.closest('p') || input.parentElement;
        let errorEl = parent.querySelector('.client-error-message');
        if (!errorEl) {
            errorEl = document.createElement('div');
            errorEl.className = 'client-error-message';
            errorEl.style.color = '#dc3545';
            errorEl.style.fontSize = '12px';
            errorEl.style.marginTop = '4px';
            errorEl.style.fontFamily = 'Arial, sans-serif';
            input.insertAdjacentElement('afterend', errorEl);
        }
        return errorEl;
    }

    function showFieldError(input, message) {
        if (!input) return;
        input.style.borderColor = '#dc3545';
        const errorEl = getErrorContainer(input);
        errorEl.textContent = message;
        errorEl.style.display = 'block';
    }

    function clearFieldError(input) {
        if (!input) return;
        input.style.borderColor = '';
        const parent = input.closest('p') || input.parentElement;
        const errorEl = parent.querySelector('.client-error-message');
        if (errorEl) {
            errorEl.textContent = '';
            errorEl.style.display = 'none';
        }
    }

    // Real-time error clearing when user edits fields
    [usernameInput, emailInput, password1Input, password2Input].forEach(input => {
        if (input) {
            input.addEventListener('input', () => clearFieldError(input));
        }
    });

    signupForm.addEventListener('submit', (event) => {
        let isValid = true;
        let firstInvalidField = null;

        // Clear existing errors
        [usernameInput, emailInput, password1Input, password2Input].forEach(clearFieldError);

        // Validate Username
        if (usernameInput) {
            const usernameVal = usernameInput.value.trim();
            if (!usernameVal) {
                showFieldError(usernameInput, 'Username is required.');
                isValid = false;
                firstInvalidField = firstInvalidField || usernameInput;
            }
        }

        // Validate Email
        if (emailInput) {
            const emailVal = emailInput.value.trim();
            if (!emailVal) {
                showFieldError(emailInput, 'Email address is required.');
                isValid = false;
                firstInvalidField = firstInvalidField || emailInput;
            } else if (!emailPattern.test(emailVal)) {
                showFieldError(emailInput, 'Please enter a valid email address (e.g. user@example.com).');
                isValid = false;
                firstInvalidField = firstInvalidField || emailInput;
            }
        }

        // Validate Password
        if (password1Input) {
            if (!password1Input.value) {
                showFieldError(password1Input, 'Password is required.');
                isValid = false;
                firstInvalidField = firstInvalidField || password1Input;
            }
        }

        // Validate Password Confirmation
        if (password2Input) {
            if (!password2Input.value) {
                showFieldError(password2Input, 'Please confirm your password.');
                isValid = false;
                firstInvalidField = firstInvalidField || password2Input;
            } else if (password1Input && password1Input.value && password1Input.value !== password2Input.value) {
                showFieldError(password2Input, 'Passwords do not match.');
                isValid = false;
                firstInvalidField = firstInvalidField || password2Input;
            }
        }

        if (!isValid) {
            event.preventDefault();
            if (firstInvalidField) {
                firstInvalidField.focus();
            }
        }
    });
});
