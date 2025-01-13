let btnModifyData = document.getElementById("btnModifyPersonalData");
let btnModifyPassword = document.getElementById("btnModifyPassword");

let popUpGroup = document.querySelector(".popup-group")

btnModifyData.addEventListener("click",(event)=>{
    let items = popUpGroup.querySelectorAll(".block");

    let itemsArray = Array.from(items);
    itemsArray.map((item)=>{
        item.classList.remove("block");
        item.classList.add("hidden");
    })
    let popupPersonalDataDiv = document.getElementById("popupPersonalData");

    popupPersonalDataDiv.classList.remove("hidden");
    popupPersonalDataDiv.classList.add("block");


})

btnModifyPassword.addEventListener("click", (event)=>{
    let items = popUpGroup.querySelectorAll(".block");

    let itemsArray = Array.from(items);
    itemsArray.map((item)=>{
        item.classList.add("hidden");
    })
    let popupPasswordDiv = document.getElementById("popupPasswordReset");

    popupPasswordDiv.classList.remove("hidden");
    popupPasswordDiv.classList.add("block");

})
