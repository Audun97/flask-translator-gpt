const outputLanguageSelect = document.getElementById("output_language");
const formalPronounsContainer = document.getElementById("formal_pronouns_container");

function updateFormalPronounsVisibility() {
    if (outputLanguageSelect.value === "German") {
        formalPronounsContainer.style.display = "block";
    } else {
        formalPronounsContainer.style.display = "none";
    }
}

outputLanguageSelect.addEventListener("change", updateFormalPronounsVisibility);
updateFormalPronounsVisibility();