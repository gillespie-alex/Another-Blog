// script.js
document.getElementById('myForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the actual form submission

    var message = document.getElementById('successMessage');
    message.classList.remove('hidden');
    message.style.opacity = 1;

    // Hide the message after 2 seconds
    setTimeout(function() {
        message.style.opacity = 0;
        message.addEventListener('transitionend', function() {
            message.classList.add('hidden');
        }, { once: true });
    }, 2000);
});
