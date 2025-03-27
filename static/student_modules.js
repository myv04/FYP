document.addEventListener("DOMContentLoaded", function () {
    const moduleCards = document.querySelectorAll(".module-card");

    moduleCards.forEach(card => {
        // Remove the click event on the whole module card
        card.style.cursor = "default"; // Ensures it doesn’t look clickable
    });
});
