document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("loginForm");
    const username = document.getElementById("username");
    const password = document.getElementById("password");
    const flashMessages = document.querySelectorAll(".flash");
  
    // Auto-hide flash messages
    flashMessages.forEach(msg => {
      setTimeout(() => {
        msg.style.opacity = "0";
        msg.style.transform = "translateY(-10px)";
        msg.style.transition = "opacity 0.5s ease, transform 0.5s ease";
        setTimeout(() => msg.style.display = "none", 500);
      }, 3000);
    });
  
    // Simple form validation
    form.addEventListener("submit", function (event) {
      if (username.value.trim() === "" || password.value.trim() === "") {
        event.preventDefault();
        alert("Both fields are required!");
      }
    });
  
    
    const togglePassword = document.getElementById("togglePassword");
    if (togglePassword) {
      togglePassword.addEventListener("click", () => {
        const inputType = password.getAttribute("type") === "password" ? "text" : "password";
        password.setAttribute("type", inputType);
        togglePassword.classList.toggle("active");
      });
    }
  });
  