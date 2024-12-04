const form = document.getElementById('add-form')

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const title = document.getElementById("tittle").value;
    const description = document.getElementById("description").value;
    const priority = document.getElementById("inputState").value;
    const category = document.getElementById("category").value;


    const data = {
        title: title,
        description: description,
        priority: priority.toLowerCase(),
        category: category,
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
            const result = await response.json();
            console.log("Zadanie zostało dodane:", result);
            alert("Zadanie zostało dodane!");
            form.reset();
        } else {
            const error = await response.json();
            console.error("Błąd podczas dodawania zadania:", error);
            alert("Nie udało się dodać zadania!");
        }
    } catch (err) {
        console.error("Wystąpił błąd sieci:", err);
        alert("Wystąpił błąd podczas wysyłania danych.");
    }
});

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