async function registerUser() {
    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;
    const response = await fetch('http://127.0.0.1:5000/api/create_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username:username, password:password })
    });
    const data = await response.json();
    document.getElementById('message').textContent = data.message;
}

async function loginUser() {
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const response = await fetch('http://127.0.0.1:5000/api/user_login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username:username, password:password  })
    });
    const data = await response.json();
    document.getElementById('loginMessage').textContent = data.message;
    
    if(data.message === '登录成功') {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'success-alert';
        alertDiv.innerHTML = `
            <svg class="checkmark" viewBox="0 0 52 52">
                <path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
            </svg>
            <span>登录成功！欢迎回来</span>
        `;
        document.body.appendChild(alertDiv);
        setTimeout(() => {
            alertDiv.style.opacity = '0';
            setTimeout(() => {
                alertDiv.remove();
                window.location.href = 'config.html';
            }, 1000);
        }, 2000);
    }
}

async function resetPassword() {
    const username = document.getElementById('resetUsername').value;
    const password = document.getElementById('resetPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        document.getElementById('message').textContent = '两次输入的密码不一致，请重新输入。';
        return;
    }

    const response = await fetch('http://127.0.0.1:5000/api/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username:username, password:password  })
    });
    const data = await response.json();
    document.getElementById('message').textContent = data.message;
}

async function logout() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/user_logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        if(data.message === '登出成功') {
            window.location.href = 'login.html';
        }
    } catch (error) {
        console.error('登出失败:', error);
    }
}
    