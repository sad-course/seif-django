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

const createActivityButton = document.getElementById('add-activity-btn')
const activityModal = document.getElementById('activity-modal')

createActivityButton.addEventListener( 'click', () => {
    activityModal.classList.toggle('hidden')
    aside.classList.toggle('hidden')

})

const eventRequestForm = document.getElementById('request_event_form')

eventRequestForm.onsubmit((event) => {
    event.preventDefault()
})
const createEventForm = document.getElementById('create-event-form')
createEventForm.onsubmit((event) => {
    event.preventDefault()
})
