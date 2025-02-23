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

var eventID = document.querySelector("input[name='event_id']").value
var subscriptionEditBtn = document.querySelector("#subscriptionEditBtn")
var subscriptionDeleteBtn = document.querySelector("#subscriptionDeleteBtn")


async function deleteSubscription(){
    try {
        let response = await fetch("/event/subcription/",{
            method: "DELETE",
            headers:{
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify({"event_id": eventID})
        })

        if (!response.ok){
            let errorData = await response.json();
            throw new Error(`Error ${response.status}: ${errorData.message || "Unknown error"}`);
        }

        let data = await response.json()
        window.location.reload()

    } catch (error) {
        console.error("Error deleting subscription:", error);
    }

}

if (subscriptionDeleteBtn != null){
    subscriptionDeleteBtn.addEventListener("click", () => {
        deleteSubscription()
    })
}
