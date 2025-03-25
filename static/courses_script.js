document.addEventListener("DOMContentLoaded", function () {
    const courseCards = document.querySelectorAll(".course-card");

    courseCards.forEach(card => {
        card.addEventListener("click", function () {
            const link = this.querySelector("a").getAttribute("href");
            window.location.href = link;
        });
    });
});
