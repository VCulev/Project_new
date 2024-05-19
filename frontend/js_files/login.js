const resetForm = formId => {
    document.getElementById(formId).reset();
}

document.getElementById('loginFormContent').addEventListener('submit', async event => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const jsonData = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('http://localhost:4000/api/login_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)
        });

        const data = await response.json();
        if (response.ok) {
            // Store the token in localStorage
            localStorage.setItem('token', data.token);
            localStorage.setItem('userId', data.user_id);

            // Redirect to index.html
            window.location.href = 'index.html';
        } else {
            document.getElementById('feedbackMessage').innerText = data.description;
        }
    } catch (error) {
        document.getElementById('feedbackMessage').innerText = 'Error logging in.';
    }
});

document.getElementById('showRegisterFormLink').addEventListener('click', event => {
    event.preventDefault();
    resetForm('loginFormContent');
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('registerForm').classList.remove('hidden');
});
