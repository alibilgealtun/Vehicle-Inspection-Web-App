// Tab navigation logic
document.querySelectorAll('.tab-content').forEach(function (tabContent) {
    tabContent.classList.remove('active');
});

document.querySelector('#tab1').classList.add('active');

document.querySelectorAll('.border-b a').forEach(function (tabLink) {
    tabLink.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelectorAll('.tab-content').forEach(function (tabContent) {
            tabContent.classList.remove('active');
        });

        document.querySelector(this.getAttribute('href')).classList.add('active');

        document.querySelectorAll('.border-b a').forEach(function (tabLink) {
            tabLink.classList.remove('border-l', 'border-t', 'border-r', 'rounded-t', 'text-blue-700');
            tabLink.classList.add('text-blue-500', 'hover:text-blue-700');
        });

        this.classList.add('border-l', 'border-t', 'border-r', 'rounded-t', 'text-blue-700');
        this.classList.remove('text-blue-500', 'hover:text-blue-700');
    });
});
