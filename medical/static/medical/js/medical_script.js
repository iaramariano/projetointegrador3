function mandatorySection(){
    const mandatory_section = document.getElementById("mandatory-section");
    const mandatory_check = document.getElementById("id_mandatory");

    if (mandatory_check.checked)
        mandatory_section.classList.remove('d-none');
    else
        mandatory_section.classList.add('d-none');
}