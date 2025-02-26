//Links do aside coloridos de acordo com a URL
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

//Menu responsivo
const hamburger = document.getElementById("hamburger-menu")
const aside = document.querySelector('aside')

hamburger.addEventListener( 'click', () => {
    aside.classList.toggle("hidden");
})

//Manipulando modal de criar atividade
const createActivityButton = document.getElementById('add-activity-btn')
const closeActivityModal = document.getElementById('close-activity-modal')
const activityModal = document.getElementById('activity-modal')

createActivityButton.addEventListener( 'click', () => {
    activityModal.classList.toggle('hidden')
    aside.classList.toggle('hidden')

})

closeActivityModal.addEventListener('click', () => {
    console.log('oi')
    if (!activityModal.classList.contains('hidden')){
        activityModal.classList.add('hidden')
    }
})

//Envia o formulário de deletar a atividade com o id da atividade enviado pelo button
function deleteActivity(activityId) {
    document.getElementById('activity-id').value = activityId;
    document.getElementById('delete-activity-form').submit();
}
