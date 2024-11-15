document.getElementById("newPackageButton").onclick = function () {
    // Show the modal for adding a new package
    document.getElementById("newPackageModal").style.display = "block";
    clearForm();  // Clear the form for new entry
    // Reset the form action to point to the add route
    document.getElementById("packageForm").action = addPackageUrl;  // Use the variable passed from Django
}

document.querySelectorAll(".updateButton").forEach(button => {
    button.onclick = function () {
        const packageId = this.getAttribute("data-id");

        // Fetch the package data using AJAX
        fetch(`/packages/update/${packageId}`, { method: 'GET', headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(response => response.json())
            .then(data => {
                // Populate the form with the package data
                document.getElementById("package_name").value = data.name;
                document.getElementById("price").value = data.price;

                // Set the selected contents in the select box
                const contentsSelect = document.getElementById("contents");
                [...contentsSelect.options].forEach(option => {
                    option.selected = data.contents.includes(option.value);
                });

                document.getElementById("active").value = data.active;

                // Show the modal
                document.getElementById("newPackageModal").style.display = "block";

                // Change the form action to update
                document.getElementById("packageForm").action = `/packages/update/${packageId}`;
            })
            .catch(error => console.error('Error:', error));
    };
});

document.getElementById("closeModal").onclick = function () {
    document.getElementById("newPackageModal").style.display = "none";
}

document.getElementById("cancelModal").onclick = function () {
    document.getElementById("newPackageModal").style.display = "none";
}

window.onclick = function (event) {
    if (event.target == document.getElementById("newPackageModal")) {
        document.getElementById("newPackageModal").style.display = "none";
    }
}

function clearForm() {
    // Clear the form values for new entry
    document.getElementById("package_name").value = '';
    document.getElementById("price").value = '0.00';
    const contentsSelect = document.getElementById("contents");
    [...contentsSelect.options].forEach(option => option.selected = false);
    document.getElementById("active").selectedIndex = 0;
}

function showAlert(message, type) {
    const alertBox = document.getElementById('alertMessage');
    const alertText = document.getElementById('alertText');
    alertText.textContent = message;
    alertBox.className = `fixed top-4 right-4 px-4 py-2 rounded shadow ${type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'}`;
    alertBox.classList.remove('hidden');

    // Auto-hide after 3 seconds
    setTimeout(() => {
        alertBox.classList.add('hidden');
    }, 3000);
}

// Close the alert manually
document.querySelector('.close-alert').onclick = function () {
    document.getElementById('alertMessage').classList.add('hidden');
};
