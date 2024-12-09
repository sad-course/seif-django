const userIcon = document.getElementById("user-icon");
const menuDropdown =  document.getElementById("menu-dropdown")

// ao passar o mouse pelo ícone do usuário o menu aparece
userIcon.addEventListener( 'mouseover', () => {
    menuDropdown.classList.remove("hidden");
})

//os dois eventos no menu servem para mente-lo ativo quando o mouse sair do icone
//do usuário, e o menu só desaparece quando o mouse sair dele.
menuDropdown.addEventListener( 'mouseover', () => {
    menuDropdown.classList.remove("hidden");
})
menuDropdown.addEventListener( 'mouseout', () => {
    menuDropdown.classList.add("hidden");
})


