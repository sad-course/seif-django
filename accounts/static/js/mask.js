let cpfInputField = document.querySelector("#cpf")
let phoneInputField = document.querySelector("#phone")

if (cpfInputField != null){
    cpfInputField.addEventListener("keydown", (event) => {

        if(event.keyCode != 8){
            let cpfInputValue = event.target.value;

            if (cpfInputValue.match(/[a-zA-Z]/gm)){
                cpfInputValue = cpfInputValue.replace(/[a-zA-Z]/gm, '')
            }

            if (cpfInputValue.length == 3 || cpfInputValue.length == 7){
                cpfInputValue += ".";
            }else{
                if(cpfInputValue.length == 11){
                    cpfInputValue += "-";
                }
            }
            cpfInputField.value = cpfInputValue;
        }
    })
}

if (phoneInputField != null){
    phoneInputField.addEventListener("keydown", (event) => {
        if(event.keyCode != 8){
            let phoneInputValue = event.target.value;

            if (phoneInputValue.length == 0){
                phoneInputValue += "(";
            }else{
                if (phoneInputValue.length == 3){
                    phoneInputValue += ")";
                }
                if(phoneInputValue.length == 9){
                    phoneInputValue += "-";
                }
            }
            phoneInputField.value = phoneInputValue;
        }
    })

}

function validateInputs(){
    let cpfRegex= /^(\d{3}\.){2}(\d{3})(\-\d{2})/gm
    let phoneRegexSpecialChar = /(\(|\)|\-)/gm
    let phoneNumbers = /(\d{11})/gm
    let cpfValue = cpfInputField.value;
    let phoneValue = phoneInputField.value;

    if (!cpfRegex.test(cpfValue) && cpfValue != ""){
        alert("Número de cpf inválido")
    }
    if (phoneValue != ""){
        phoneValue = phoneValue.replace(phoneRegexSpecialChar, "");
        if (!phoneNumbers.test(phoneValue)){
            alert("O número de telefone é inválido.")
        }
    }

}
