

function openUpdateModal(appointmentId) {
    fetch(`/appointment/update/${appointmentId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("updateModal").innerHTML = data;
            document.getElementById("updateModal").classList.add("active");

            // Force display to make sure modal shows up
            document.getElementById("updateModal").style.display = "flex";

            // Add event listener for closing the modal
            document.getElementById("closeUpdateModalBtn").onclick = function () {
                document.getElementById("updateModal").classList.remove("active");
                document.getElementById("updateModal").style.display = "none";
            };

            // Add event listener to close the modal when clicking outside of it
            window.onclick = function (event) {
                if (event.target == document.getElementById("updateModal")) {
                    document.getElementById("updateModal").classList.remove("active");
                    document.getElementById("updateModal").style.display = "none";
                }
            };
        })
        .catch(error => {
            console.error('Error loading modal:', error);
        });
}
