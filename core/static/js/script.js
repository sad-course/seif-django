const userIcon = document.getElementById("user-icon");
const menuDropdown =  document.getElementById("menu-dropdown")

// menu dropdown aparece ou desaparece ao clicar no icone
userIcon.addEventListener( 'click', () => {
    menuDropdown.classList.toggle("hidden");
})

//menu hamburger responsivo

const hamburger = document.getElementById("hamburger-menu")
const menuResponsive = document.getElementById("menu-responsive")


hamburger.addEventListener( 'click', () => {
    menuResponsive.classList.toggle("hidden");
})
