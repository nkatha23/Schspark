

document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector(".hamburger");
    const mobileMenu = document.querySelector(".mobile-menu");

    if (hamburger && mobileMenu) {
        hamburger.addEventListener("click", function() {
            mobileMenu.classList.toggle("active");
            // Toggle hamburger icon between ☰ and ✕
            if (mobileMenu.classList.contains("active")) {
                hamburger.innerHTML = "✕";
            } else {
                hamburger.innerHTML = "☰";
            }
        });
    } else {
        console.error("Hamburger menu or mobile menu not found!");
    }
});