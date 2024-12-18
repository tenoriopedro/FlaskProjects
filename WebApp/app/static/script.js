const menuToggle = document.querySelector('.menuToggle');
const filter = document.querySelector('.filter');

menuToggle.onclick = () => {
    filter.classList.toggle('active');
}