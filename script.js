document.getElementById('signupForm').onsubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);

    const response = await fetch('/signup', {
        method: 'POST',
        body: formData,
    });

    const result = await response.json();
    alert(result.message);
    if (result.success) {
        window.location.href = 'signin.html'; // Redirect to sign-in after successful signup
    }
};

document.getElementById('signinForm').onsubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);

    const response = await fetch('/signin', {
        method: 'POST',
        body: formData,
    });

    const result = await response.json();
    alert(result.message);
    if (result.success) {
        window.location.href = 'index.html'; // Redirect to main page after sign-in
    }
};

// Display username after sign-in
document.addEventListener("DOMContentLoaded", () => {
    const userGreeting = document.getElementById("user-greeting");
    const username = sessionStorage.getItem("username");

    if (username) {
        userGreeting.innerHTML = `<span>Welcome, ${username}</span>`;
    }
});
