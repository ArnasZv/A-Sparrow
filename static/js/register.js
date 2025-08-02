document.getElementById("register-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const userData = {
        username: document.getElementById("name").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
        created_date: new Date().toISOString().slice(0, 10),
    };

    try {
        const response = await fetch("/api/users/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(userData),
        });

        if (response.ok) {
            const data = await response.json();
            window.location.href = data.redirect_url;  // ✅ Use redirect from backend
        } else {
            const errorMessage = await response.text();
            console.error("Registration failed:", errorMessage);
        }
    } catch (error) {
        console.error("Error during register:", error);
    }
});