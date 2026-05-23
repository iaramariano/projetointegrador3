document.getElementById('id_species').addEventListener('change', function () {
    
    const species = this.value;

    fetch(`/medical/event/pets-by-species/?species=${species}`)
      .then(response => response.json())
      .then(pets => {
        const petSelect = document.getElementById('id_pet');
        
        // limpa as opções atuais
        petSelect.innerHTML = '<option value="">---------</option>';
        
        // adiciona os pets filtrados
        pets.forEach(pet => {
          const option = document.createElement('option');
          option.value = pet.id;
          option.textContent = pet.name;
          petSelect.appendChild(option);
        });
        petGroup = document.getElementById('id_pet_group')
        petGroup.style.display = 'block';
      });
  });

document.getElementById('id_pet').addEventListener('change', function () {

    const name = this.value;
    
    if (name == "")
      document.getElementById('btn_visularizar').disabled = true;
    else
      document.getElementById('btn_visularizar').disabled = false;

});


