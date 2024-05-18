const resetForm = formId => {
    document.getElementById(formId).reset();
}

document.getElementById('registerFormContent').addEventListener('submit', async event => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const jsonData = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('http://localhost:4000/api/register_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)
        });

        const data = await response.json();
        if (response.ok) {
            window.location.href = 'login.html';
        } else {
            document.getElementById('feedbackMessage').innerText = data.description;
        }
    } catch (error) {
        document.getElementById('feedbackMessage').innerText = 'Error registering.';
    }
});

document.getElementById('showLoginFormLink').addEventListener('click', event => {
    event.preventDefault();
    resetForm('registerFormContent');
    document.getElementById('registerForm').classList.add('hidden');
    document.getElementById('loginForm').classList.remove('hidden');
});
