// script.js
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("loginForm");
    const username = document.getElementById("username");
    const password = document.getElementById("password");
    const flashMessages = document.querySelectorAll(".flash");

    // Auto-hide flash messages after 3 seconds
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.display = "none";
        }, 3000);
    });

    // Form validation
    form.addEventListener("submit", function (event) {
        if (username.value.trim() === "" || password.value.trim() === "") {
            event.preventDefault(); // Prevent form submission
            alert("Both fields are required!");
        }
    });
});
