// Получаем данные из скрытого элемента
const roomData = document.getElementById("room-data");
const username = roomData.getAttribute("data-username");

let currentId = null;

const ws = new WebSocket(`ws://localhost:8000/ws/table/?username=${username}`);

fetch('http://localhost:8000/task/', {
    method: 'GET'
})
.then(res => res.json())
.then(data => {
    const tasks = document.getElementById('tasks');

    for (let i = 0; i < data.length; i++) {
        const task = document.createElement('div');
        task.className = 'task';
        task.dataset.id = data[i].id;

        const titleContainer = document.createElement('div');
        titleContainer.className = 'title-container';
        
        const title = document.createElement('span');
        title.className = 'task-title';
        title.textContent = data[i].title;
        
        const description = document.createElement('div');
        description.className = 'task-description';
        description.textContent = data[i].description || 'Описание отсутствует';
        description.style.display = 'none';
        
        title.addEventListener('mouseenter', () => {
            description.style.display = 'block';
        });
        
        title.addEventListener('mouseleave', () => {
            description.style.display = 'none';
        });
        
        const buttonsContainer = document.createElement('div');
        buttonsContainer.className = 'task-buttons';
        
        const edit_button = document.createElement('button');
        edit_button.className = 'inside-button edit-button';
        edit_button.textContent = 'Edit';
        edit_button.onclick = () => showEditTaskTable(data[i].id, data[i].title, data[i].description);
        
        const delete_button = document.createElement('button');
        delete_button.className = 'inside-button delete-button';
        delete_button.textContent = 'Delete';
        delete_button.onclick = () => showDeleteTaskTable(data[i].id);
        
        titleContainer.appendChild(title);
        titleContainer.appendChild(description);
        
        buttonsContainer.appendChild(edit_button);
        buttonsContainer.appendChild(delete_button);
        
        task.appendChild(titleContainer);
        task.appendChild(buttonsContainer);
        
        tasks.appendChild(task);
    }
});

ws.onopen = () => {
    console.log("Соединение установлено");
};

ws.onclose = () => {
    console.log("Соединение закрыто");
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('message: ', data);
    let task = null;

    switch(data.type) {
        case 'ADD':
            const tasks = document.getElementById("tasks");
            task = document.createElement('div');
            task.className = 'task';
            task.dataset.id = data.id;

            const titleContainer = document.createElement('div');
            titleContainer.className = 'title-container';
            
            const title = document.createElement('span');
            title.className = 'task-title';
            title.textContent = data.title;
            
            const description = document.createElement('div');
            description.className = 'task-description';
            description.textContent = data.description || 'Описание отсутствует';
            description.style.display = 'none';
            
            title.addEventListener('mouseenter', () => {
                description.style.display = 'block';
            });
            
            title.addEventListener('mouseleave', () => {
                description.style.display = 'none';
            });
            
            const buttonsContainer = document.createElement('div');
            buttonsContainer.className = 'task-buttons';
            
            const edit_button = document.createElement('button');
            edit_button.className = 'inside-button edit-button';
            edit_button.textContent = 'Edit';
            edit_button.onclick = () => showEditTaskTable(data.id, data.title, data.description);
            
            const delete_button = document.createElement('button');
            delete_button.className = 'inside-button delete-button';
            delete_button.textContent = 'Delete';
            delete_button.onclick = () => showDeleteTaskTable(data.id);
            
            titleContainer.appendChild(title);
            titleContainer.appendChild(description);
            
            buttonsContainer.appendChild(edit_button);
            buttonsContainer.appendChild(delete_button);
            
            task.appendChild(titleContainer);
            task.appendChild(buttonsContainer);
            
            tasks.appendChild(task);
            break;
        case 'PUT':
            task = document.querySelector(`[data-id='${data.id}']`).querySelectorAll('div');
            title_container = task[0];
            button_container = task[1];
            title_container.querySelector('.task-title').textContent = data.title;
            title_container.querySelector('.task-description').textContent = data.description;
            button_container.querySelector('.edit-button').onclick = () => showEditTaskTable(data.id, data.title, data.description);
            button_container.querySelector('.delete-button').onclick = () => showDeleteTaskTable(data.id);
            break;
        case 'DELETE':
            task = document.querySelector(`[data-id='${data.id}']`);
            task.remove();
            break;
    }
};

function showAddTaskTable() {
    add_task_field = document.getElementById("add-task");
    add_task_field.classList.toggle("hidden");
}

function showEditTaskTable(id, title, description) {
    edit_task_field = document.getElementById("edit-task");
    edit_task_field.querySelector('#edit-title').value = title;
    edit_task_field.querySelector('#edit-description').value = description;
    edit_task_field.classList.toggle("hidden");

    currentId = id;
}

function showDeleteTaskTable(id) {
    console.log("id: ", id)
    if (confirm('Подтвердить удаление?')) {
        deleteTask(id);
    }
}

function addTask() {
    const title = document.getElementById("add-title").value;
    if (title === "") {
        alert('Поле Название не может быть пустым')
        return;
    }
    const description = document.getElementById("add-description").value;

    fetch("http://localhost:8000/task/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'title': title,
            'description': description,
        })
    })
    .then(res => {
        if (res.status != 200) {
            throw new Error('Invalid title or description')
        }
        return res.json()
    })
    .then(data => {
        ws.send(JSON.stringify({
            'type': 'ADD',
            'id': data.id,
            'title': data.title,
            'description': data.description,
        }))
    })
    .catch(error => {
        alert('Некорректное имя поля')
        console.error('Ошибка:', error);
    })

    showAddTaskTable();
}

function editTask() {
    const title = document.getElementById("edit-title").value;
    if (title === "") {
        alert('Поле Название не может быть пустым')
        return;
    }
    const description = document.getElementById("edit-description").value;

    fetch("http://localhost:8000/task/", {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'id': currentId,
            'title': title,
            'description': description,
        })
    })
    .then(res => {
        if (res.status != 200) {
            throw new Error('Edit task error')
        }
        return res.json()
    })
    .then(data => {
        ws.send(JSON.stringify({
            'type': 'PUT',
            'id': data.id,
            'title': data.title,
            'description': data.description,
        }))
    })
    .catch(error => {
        console.error('Ошибка:', error);
    })
    
    showEditTaskTable();
}

function deleteTask(id) {
    fetch(`http://localhost:8000/task/?task_id=${id}`, {
        method: 'DELETE'
    })
    .then(res => {
        if (res.status != 200) {
            throw new Error('Task not exist')
        }
        return res.json()
    })
    .then(data => {
        ws.send(JSON.stringify({
            'type': 'DELETE',
            'id': data.id
        }))
    })
    .catch(error => {
        console.error('Ошибка:', error);
    })
}