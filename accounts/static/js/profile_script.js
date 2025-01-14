try {
    let btnModifyData = document.querySelector("#btnModifyPersonalData");
    let btnModifyPassword = document.querySelector("#btnModifyPassword");

    let popUpGroup = document.querySelector(".popup-group");

    let popupPersonalDataDiv = document.querySelector("#popupPersonalData");
    let popupPasswordDiv = document.querySelector("#popupPasswordReset");

    let btnConfirmDataChanges = document.querySelector("#btnConfirmDataChanges");
    let btnConfirmPasswordChange = document.querySelector("#btnConfirmPasswordChange");

    if (btnModifyData) {
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

    if (btnModifyPassword) {
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

    if (btnConfirmDataChanges) {
        btnConfirmDataChanges.addEventListener("click", (event) => {
            let element = popupPersonalDataDiv.querySelector(".badge-message");
            if (element) {
                element.classList.remove("hidden");
            }
        });
    }

    if (btnConfirmPasswordChange) {
        btnConfirmPasswordChange.addEventListener("click", (event) => {
            let element = popupPasswordDiv.querySelector(".badge-message");
            if (element) {
                element.classList.remove("hidden");
            }
        });
    }

    let btnConfirmEmailRequest = document.querySelector("#btnConfirmEmailRequest");
    if (btnConfirmEmailRequest) {
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
} catch (e) {
    console.error('Erro ao adicionar event listeners:', e);
}
