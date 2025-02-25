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

var eventID = document.querySelector("input[name='event_id']").value;
var subscriptionEditBtn = document.querySelector("#subscriptionEditBtn");
var subscriptionDeleteBtn = document.querySelector("#subscriptionDeleteBtn");
var routeURL = `/event/subcription/${eventID}/`

async function deleteSubscription(){
    try {
        let response = await fetch(routeURL,{
            method: "DELETE",
            headers:{
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
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

async function updateSubscription(){
    const selectedActivities = Array.from(document.querySelectorAll('input[name="selected_activities"]:checked'))
                                .map(option => option.value);
    try {
        let response = await fetch(routeURL,{
            method: "PATCH",
            headers:{
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify({
                "selected_activities": selectedActivities,
            })
        })

        if (!response.ok){
            let errorData = await response.json();
            throw new Error(`Error ${response.status}: ${errorData.message || "Unknown error"}`);
        }else{
            let data = await response.json();
            window.location.href = "/accounts/my_events/";
        }


    } catch (error) {
        console.error("Error updating subscription:", error);
    }

}

if (subscriptionDeleteBtn != null){
    subscriptionDeleteBtn.addEventListener("click", () => {
        deleteSubscription();
    });
};

if (subscriptionEditBtn != null){
    subscriptionEditBtn.addEventListener("click", () => {
        updateSubscription();
    });
};
