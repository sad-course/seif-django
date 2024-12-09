const userIcon = document.getElementById("user-icon");
const menuDropdown =  document.getElementById("menu-dropdown")

// menu dropdown aparece ou desaparece ao clicar no icone
userIcon.addEventListener( 'click', () => {
    menuDropdown.classList.toggle("hidden");
})


