let resetForm = (formId) => {
    const form = document.getElementById(formId);
    form.reset();
}

document.getElementById('registerFormContent').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const jsonData = {};
    for (const [key, value] of formData.entries()) {
        jsonData[key] = value;
    }

    const response = await fetch('http://localhost:4000/api/register_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    });

    const data = await response.json();
    if (response.ok) {
        // Redirect to login page after successful registration
        window.location.href = 'login.html';
    } else {
        document.getElementById('feedbackMessage').innerText = data.description;
    }
});

// Show login form when "Login" link is clicked
document.getElementById('showLoginFormLink').addEventListener('click', function(event) {
    event.preventDefault();
    resetForm('registerFormContent');
    document.getElementById('registerForm').classList.add('hidden');
    document.getElementById('loginForm').classList.remove('hidden');
});
