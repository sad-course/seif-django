let btnModifyData = document.getElementById("btnModifyPersonalData");
let btnModifyPassword = document.getElementById("btnModifyPassword");

let popUpGroup = document.querySelector(".popup-group")

btnModifyData.addEventListener("click",(event)=>{
    let items = popUpGroup.querySelectorAll(".block");

    let itemsArray = Array.from(items);
    console.log(itemsArray);
    itemsArray.map((item)=>{
        item.classList.add("hidden");
    })
    let popupPersonalDataDiv = document.getElementById("popupPersonalData");
    console.log(popupPersonalDataDiv);
    
    popupPersonalDataDiv.classList.remove("hidden");
    popupPersonalDataDiv.classList.add("block");


})

btnModifyPassword.addEventListener("click", (event)=>{
    let items = popUpGroup.querySelectorAll(".block");

    let itemsArray = Array.from(items);
    console.log(itemsArray);
    itemsArray.map((item)=>{
        item.classList.add("hidden");
    })
    let popupPasswordDiv = document.getElementById("popupPasswordReset");
    console.log(popupPasswordDiv);
    
    popupPasswordDiv.classList.remove("hidden");
    popupPersonalDataDiv.classList.add("block");

})