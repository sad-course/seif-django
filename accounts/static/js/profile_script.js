function getCSRFToken() {

    // Esse utilitário acessas o csrftoken armazenado nos cookies do navegador.
    // Divide a string recebida e converte para lista com split(;), busca e
    // retorna o valor caso encontre.

    const cookieValue = document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
    return cookieValue;
}

let btnModifyData = document.querySelector("#btnModifyPersonalData");
let btnModifyPassword = document.querySelector("#btnModifyPassword");

let popUpGroup = document.querySelector(".popup-group");

let popupPersonalDataDiv = document.querySelector("#popupPersonalData");
let popupPasswordDiv = document.querySelector("#popupPasswordReset");

let btnConfirmDataChanges = document.querySelector("#btnConfirmDataChanges");
let btnConfirmPasswordChange = document.querySelector("#btnConfirmPasswordChange");

if (btnModifyData != null) {
    btnModifyData.addEventListener("click", (event) => {
        let items = popUpGroup.querySelectorAll(".block");
        let itemsArray = Array.from(items);
        itemsArray.map((item) => {
            item.classList.remove("block");
            item.classList.add("hidden");
        });

        popupPersonalDataDiv.classList.remove("hidden");
        popupPersonalDataDiv.classList.add("block");
    });
}

if (btnModifyPassword != null) {
    btnModifyPassword.addEventListener("click", (event) => {
        let items = popUpGroup.querySelectorAll(".block");
        let itemsArray = Array.from(items);
        itemsArray.map((item) => {
            item.classList.add("hidden");
        });

        popupPasswordDiv.classList.remove("hidden");
        popupPasswordDiv.classList.add("block");
    });
}

async function updateUserData(){
    const username = document.querySelector("input[name='name']").value
    const cpf = document.querySelector("input[name='cpf']").value
    const phone = document.querySelector("input[name='phone']").value

    const userData = {
        "name": username,
        "cpf": cpf,
        "phone": phone
    }

    try {
        let response = await fetch("/accounts/update/",{
            method: "PATCH",
            headers:{
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify(userData)
        })

        if (!response.ok){
            let errorData = await response.json();
            throw new Error(`Error ${response.status}: ${errorData.message || "Unknown error"}`);
        }

        let data = await response.json()
        console.log(data)
        // window.location.reload()

    } catch (error) {
        console.error("Error updating user:", error);
    }

}

if (btnConfirmDataChanges != null) {
    btnConfirmDataChanges.addEventListener("click", (event) => {
        updateUserData()
    });
}

if (btnConfirmPasswordChange != null) {
    btnConfirmPasswordChange.addEventListener("click", (event) => {
        let element = popupPasswordDiv.querySelector(".badge-message");
        if (element) {
            element.classList.remove("hidden");
        }
    });
}

let btnConfirmEmailRequest = document.querySelector("#btnConfirmEmailRequest");
if (btnConfirmEmailRequest != null) {
    btnConfirmEmailRequest.addEventListener("click", (event) => {
        let element = document.querySelector(".badge-message");
        if (element && element.classList.contains("hidden")) {
            element.classList.remove("hidden");
            setTimeout(function(){
                window.location.href="/accounts/reset_password/"
            },1000)
        }
    });
}


//forms do avatar no profile
document.getElementById('photo-upload').addEventListener('change', function() {
    document.getElementById('upload-form').submit()
})
