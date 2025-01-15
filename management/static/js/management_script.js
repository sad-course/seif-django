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

//botão não está funcionando corretamente
/*
const modal = document.getElementById('activity-modal');
    const openModalBtn = document.getElementById('add-activity-btn');
    const closeModalBtn = document.getElementById('close-modal-btn');

    openModalBtn.addEventListener('click', () => {
        modal.classList.remove('hidden');
    });

    closeModalBtn.addEventListener('click', () => {
        modal.classList.add('hidden');
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.classList.add('hidden');
        }
    });
*/
