document.addEventListener('DOMContentLoaded', (event) => {
    const modal = document.getElementById("appointmentModal");
    const openModalButton = document.getElementById("openAppointmentModal");
    const closeModalButton = document.querySelector(".close");
    const cancelButton = document.querySelector(".cancel");

    // Check if elements exist before assigning event listeners
    if (openModalButton && modal) {
        // Open modal
        openModalButton.onclick = function() {
            modal.style.display = "block";
        }
    }

    if (closeModalButton && modal) {
        // Close modal
        closeModalButton.onclick = function() {
            modal.style.display = "none";
        }
    }

    if (cancelButton && modal) {
        // Cancel button closes modal
        cancelButton.onclick = function() {
            modal.style.display = "none";
        }
    }

    // Close modal if clicking outside the modal
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});

