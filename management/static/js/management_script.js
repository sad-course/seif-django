const ul = document.querySelectorAll('li');

const path = window.location.pathname;
ul.forEach((item) => {
    const selectedLink = item.querySelector('a');

    if (selectedLink.getAttribute('href') === path) {
        item.classList.add('aside-select-item')
    }else{
        item.classList.remove('aside-select-item')
    }
 
})

const hamburger = document.getElementById("hamburger-menu")
const aside = document.querySelector('aside')


hamburger.addEventListener( 'click', () => {
    aside.classList.toggle("hidden");
})