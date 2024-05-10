let resetForm = (formId) => {
    const form = document.getElementById(formId);
    form.reset();
}

document.getElementById('loginFormContent').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const jsonData = {};
    for (const [key, value] of formData.entries()) {
        jsonData[key] = value;
    }

    const response = await fetch('http://localhost:4000/api/login_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    });

    const data = await response.json();
    if (response.ok) {
        // Redirect to index.html after successful login
        window.location.href = 'index.html';
    } else {
        document.getElementById('feedbackMessage').innerText = data.description;
    }
});

// Show registration form when "Sign up" link is clicked
document.getElementById('showRegisterFormLink').addEventListener('click', function(event) {
    event.preventDefault();
    resetForm('loginFormContent');
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('registerForm').classList.remove('hidden');
});
