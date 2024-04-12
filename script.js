
var navbarToggler = document.querySelector('.navbar-toggler');
var navbarCollapse = document.querySelector('.navbar-collapse');

navbarToggler.addEventListener('click', function () {
    navbarCollapse.classList.toggle('show');
});
const profiles = document.querySelectorAll('.profile');
const quotes = document.querySelectorAll('.quote');
let currentIndex = 0;

function showNextProfile() {
    profiles[currentIndex].classList.remove('active');
    quotes[currentIndex].classList.remove('active');
    currentIndex = (currentIndex + 1) % profiles.length;
    profiles[currentIndex].classList.add('active');
    quotes[currentIndex].classList.add('active');
}

setInterval(showNextProfile, 4000);