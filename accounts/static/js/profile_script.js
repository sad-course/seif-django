let btnModifyData = document.querySelector("#btnModifyPersonalData");
let btnModifyPassword = document.querySelector("#btnModifyPassword");

let popUpGroup = document.querySelector(".popup-group")

let popupPersonalDataDiv = document.querySelector("#popupPersonalData");
let popupPasswordDiv = document.querySelector("#popupPasswordReset");

let btnConfirmDataChanges = document.querySelector("#btnConfirmDataChanges");
let btnConfirmPasswordChange = document.querySelector("#btnConfirmPasswordChange");

btnModifyData.addEventListener("click",(event)=>{
    let items = popUpGroup.querySelectorAll(".block");

    let itemsArray = Array.from(items);
    itemsArray.map((item)=>{
        item.classList.remove("block");
        item.classList.add("hidden");
    })

    popupPersonalDataDiv.classList.remove("hidden");
    popupPersonalDataDiv.classList.add("block");


})

btnModifyPassword.addEventListener("click", (event)=>{
    let items = popUpGroup.querySelectorAll(".block");

    let itemsArray = Array.from(items);
    itemsArray.map((item)=>{
        item.classList.add("hidden");
    })

    popupPasswordDiv.classList.remove("hidden");
    popupPasswordDiv.classList.add("block");

})

btnConfirmDataChanges.addEventListener("click",(event)=>{
    element = popupPersonalDataDiv.querySelector(".badge-message");
    element.classList.remove("hidden");
    console.log(element);
})

btnConfirmPasswordChange.addEventListener("click",(event)=>{
    element = popupPasswordDiv.querySelector(".badge-message");
    element.classList.remove("hidden");
    console.log(element);
})
