
function openEditModal(fieldId) {
    let modal = document.getElementById("editModal");
    let input = document.getElementById("editInput");

    if (modal && input) {
        modal.style.display = "block";
        input.value = document.getElementById(fieldId).textContent;
        input.setAttribute("data-field", fieldId);
    }
}

function closeEditModal() {
    document.getElementById("editModal").style.display = "none";
}


function saveEdit() {
    let input = document.getElementById("editInput");
    let fieldId = input.getAttribute("data-field");

    if (fieldId) {
        document.getElementById(fieldId).textContent = input.value;
    }

    closeEditModal();
}


window.onclick = function(event) {
    let modal = document.getElementById("editModal");
    if (event.target == modal) {
        closeEditModal();
    }
};
