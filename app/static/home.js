// document.getElementById("username").value = "n";
// document.getElementById("password").value = "123";
// preLogin();

function preLogin() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    login(username, password);
}

function login(username, password) {
    fetch("http://localhost:8000/user/login", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'username': username,
            'password': password,
        })
    })
    .then(res => {
        if (res.status != 200) {
            throw new Error('Invalid credentials');
        }
        return res.json();
    })
    .then(data => {
        fetch("http://localhost:8000/join_table", {
            headers: { 'Authorization': `Bearer ${data.access_token}` }
        })
        .then(response => {
            return response.text();
        })
        .then(html => {
            document.open();
            document.writeln(html);
            document.close();
        })
    })
    .catch(error => {
        alert('Invalid credentials')
        console.error('Ошибка:', error);
    });
}

function showRegisterTable() {
    document.getElementById('register').classList.toggle('hidden');
}

function register() {
    const username = document.getElementById('username-reg').value;
    const password = document.getElementById('password-reg').value;
    const email = document.getElementById('email-reg').value;

    fetch("http://localhost:8000/user/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'username': username,
            'password': password,
            'email': email,
        })
    })
    .then(res => {
        if (res.status != 200) {
            throw new Error('Register error')
        }
        return res.json();
    })
    .then(data => {
        login(data.username, data.password);
    })
    .catch(error => {
        alert('Ошибка регистрации');
        console.log('Ошибка:', error);
    })
}