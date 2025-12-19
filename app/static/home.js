function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch("http://localhost:8000/user/login/", {
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
        fetch("http://localhost:8000/join_table/", {
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

// document.getElementById("username").value = "n";
// document.getElementById("password").value = "123";
// login();

// function register() {
//     fetch("http://localhost:8000/user/register")
// }