document.addEventListener('DOMContentLoaded', () => {
    const loginBtn = document.getElementById('loginBtn');
    const logoutBtn = document.getElementById('logoutBtn');

    const token = localStorage.getItem('token');

    if (token) {
        loginBtn.style.display = 'none';
        logoutBtn.style.display = 'block';
    } else {
        loginBtn.style.display = 'block';
        logoutBtn.style.display = 'none';
    }

    logoutBtn.addEventListener('click', async () => {
        const token = localStorage.getItem('token');
        if (!token) return;

        try {
            const response = await fetch('http://localhost:4000/api/logout_user', {
                method: 'POST',
                headers: {
                    'Authorization': token
                }
            });

            if (!response.ok) {
                throw new Error('Failed to logout');
            }

            localStorage.removeItem('token');
            localStorage.removeItem('userId');
            location.href = 'login.html';
        } catch (error) {
            console.error('Error logging out:', error.message);
        }
    });
});
