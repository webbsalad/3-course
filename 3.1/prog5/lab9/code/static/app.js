const API_BASE_URL = "http://localhost:5000";

document.getElementById("register-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("register-username").value;
    const password = document.getElementById("register-password").value;

    const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    if (response.ok) {
        alert("Регистрация успешна! Токен сохранен.");
        localStorage.setItem("token", data.token);
        showUserInfo();
    } else {
        alert(data.error || "Ошибка регистрации.");
    }
});

document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    if (response.ok) {
        alert("Вход выполнен! Токен сохранен.");
        localStorage.setItem("token", data.token);
        showUserInfo();
    } else {
        alert(data.error || "Ошибка входа.");
    }
});

async function showUserInfo() {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Вы не авторизованы.");
        return;
    }

    const response = await fetch(`${API_BASE_URL}/users/1/bonus`, {
        method: "GET",
        headers: { Authorization: `Bearer ${token}` },
    });

    const data = await response.json();
    if (response.ok) {
        document.getElementById("bonus-info").innerHTML = `
            <p>Уровень: ${data.name}</p>
            <p>Кэшбэк: ${data.cashback_percentage}%</p>
        `;
        document.getElementById("user-info").style.display = "block";
    } else {
        alert(data.error || "Ошибка получения информации.");
    }
}

document.getElementById("transaction-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("token");
    const amount = document.getElementById("transaction-amount").value;

    const response = await fetch(`${API_BASE_URL}/users/1/transactions`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ amount: parseFloat(amount) }),
    });

    const data = await response.json();
    if (response.ok) {
        alert("Транзакция добавлена!");
        showUserInfo();
    } else {
        alert(data.error || "Ошибка добавления транзакции.");
    }
});
