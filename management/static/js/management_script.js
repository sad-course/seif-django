const ul = document.querySelectorAll('li');
console.log(ul)

//função temporária
const url_atual = window.location.pathname;
ul.forEach((item) => {
    const selectedLink = item.querySelector('a');

    if (selectedLink.getAttribute('href') === url_atual) {
        item.classList.add('aside-select-item')
    }else{
        item.classList.remove('aside-select-item')
    }

 
})

//menu hamburguer

const hamburger = document.getElementById("hamburger-menu")
const aside = document.querySelector('aside')


hamburger.addEventListener( 'click', () => {
    aside.classList.toggle("hidden");
})