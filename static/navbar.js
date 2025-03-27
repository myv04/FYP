// navbar.js
document.addEventListener("DOMContentLoaded", function () {
    const navLinks = document.querySelectorAll(".sidebar nav a");

    navLinks.forEach(link => {
        link.addEventListener("mouseenter", () => {
            link.style.transition = "0.3s ease";
            link.style.paddingLeft = "25px";
        });

        link.addEventListener("mouseleave", () => {
            link.style.transition = "0.3s ease";
            link.style.paddingLeft = "15px";
        });
    });
});
