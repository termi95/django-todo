const form = document.getElementById('add-form')

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const title = document.getElementById("tittle").value;
    const description = document.getElementById("description").value;
    const priority = document.getElementById("inputState").value;


    const data = {
        title: title,
        description: description,
        priority: priority.toLowerCase(),
    };
    try {
        const response = await fetch("/todos/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            refresh();
            form.reset();
        }
    } catch (err) {
        console.error("Wystąpił błąd sieci:", err);
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const trashIcons = document.querySelectorAll('.bi-trash');

    trashIcons.forEach(icon => {
        icon.addEventListener('click', async (event) => {
            const taskElement = event.target.closest('[task-id]');
            const taskId = taskElement.getAttribute('task-id');

            if (confirm('Are you sure you want to delete this task?')) {
                try {
                    const response = await fetch(`/todos/delete/${taskId}`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json',
                            "X-CSRFToken": getCookie("csrftoken"),
                        }
                    });

                    if (response.ok) {
                        taskElement.parentElement.remove();
                    }
                } catch (error) {
                    console.error('Error:', error);
                }
            }
        });
    });
});

function refresh() {
    const mainList = document.getElementById("mainList")
    fetch("/todos/task-list", {
        method: "GET"
    })
        .then(response => {
            return response.text();
        })
        .then(html => {
            mainList.innerHTML = html;
            addCheckboxEventListeners();
        })
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
document.addEventListener("click", function (event) {
    if (event.target.closest('[data-bs-toggle="modal"]')) {
        const button = event.target.closest('[data-bs-toggle="modal"]');
        const taskId = button.closest('[task-id]').getAttribute('task-id');

        fetch(`/todos/task/${taskId}`)
            .then(response => response.json())
            .then(task => {
                document.getElementById('modal-taskId').value = task.id;
                document.getElementById('modal-tittle').value = task.title;
                document.getElementById('modal-label').innerText = "Edit task - " + task.title;
                document.getElementById('modal-description').value = task.description;
                document.getElementById('modal-inputState').value = task.priority;
            })
            .catch(err => console.error("Błąd pobierania danych zadania:", err));
        modalSubmit()
    }
});

function modalSubmit() {
    const modal = document.getElementById('modal-form')
    
    modal.addEventListener("submit", async (e) => {
        e.preventDefault();
    
        const taskId = document.getElementById("modal-taskId").value;
        const title = document.getElementById("modal-tittle").value;
        const description = document.getElementById("modal-description").value;
        const priority = document.getElementById("modal-inputState").value;
    
        const data = {
            title: title,
            description: description,
            priority: priority.toLowerCase(),
        };
        try {
            const response = await fetch(`/todos/edit/${taskId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify(data),
            });
    
            if (response.ok) {
                refresh();
                document.getElementById('modal-close').click();
            }
        } catch (err) {
            console.error("Wystąpił błąd sieci:", err);
        }
    });   
}

function addCheckboxEventListeners() {
    document.querySelectorAll('.form-check-input').forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            const taskId = checkbox.value;
            const isCompleted = checkbox.checked;
            
            fetch(`/todos/done/${taskId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie("csrftoken"),
                },
                body: JSON.stringify({
                    completed: isCompleted
                })
            })
            .then(response => {
                if (response.ok) {
                    refresh();
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
}

refresh()