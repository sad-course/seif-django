const ul = document.querySelectorAll('ul li');
console.log(ul)

//função temporária
const url_atual = window.location.pathname;
ul.forEach((item) => {
    item.addEventListener('click', () => {
        const selectedLink = item.querySelector(a);
        console.log(item)
        if (selectedLink.getAtribute('href') === url_atual) {
            item.classList.add('aside-select-item')
        }else{
            console.log(selectedLink)
        }
    })

})
