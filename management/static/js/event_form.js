
var bannerInput = document.querySelector("#id_banner")

bannerInput.addEventListener("input", (event)=>{
    const file = event.target.files[0];

    if (file) {
        let eventBannerImg = document.querySelector("#eventBanner")
        const reader = new FileReader();
        reader.onload = function(e) {
            eventBannerImg.src = e.target.result;
        };

        reader.readAsDataURL(file);

    }
})


// Definição de um elemento em Tagify
var input = document.querySelector('#id_tags');
tagify = new Tagify(input, {
    enforceWhitelist : false,
    delimiters       : ",",
    whitelist        : [],
    callbacks        : {
        add    : console.log,  // callback when adding a tag
        remove : console.log   // callback when removing a tag
    }
})

async function updateWhitelist() {
    try {
        let response = await fetch('/management/tags');  // Replace with actual API endpoint
        let data = await response.json();

        // Assuming API returns a list of tags, update the whitelist
        tagify.settings.whitelist = data;

        // Re-render dropdown suggestions
        // tagify.dropdown.hide();
        // tagify.dropdown.show();
    } catch (error) {
        console.error("Error fetching whitelist data:", error);
    }
}

// Fetch and update whitelist after initializing Tagify
updateWhitelist();
