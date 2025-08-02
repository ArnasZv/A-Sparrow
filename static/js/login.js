document.getElementById("login-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const loginData = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };

    try {
        const response = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(loginData)
        });

        const result = await response.json();

        const messageDiv = document.getElementById("login-message");
        messageDiv.textContent = result.message;

        if (response.ok) {
            messageDiv.style.color = "green";
            // Wait 3 seconds then redirect to homepage
            setTimeout(() => {
                window.location.href = "/";
            }, 2000);
        } else {
            messageDiv.style.color = "red";
        }

    } catch (error) {
        console.error("Login error:", error);
    }
});