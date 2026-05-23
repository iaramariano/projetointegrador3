document.getElementById('id_procedure').addEventListener('change', function () {
    
    const procedureId = this.value;

    fetch(`/medical/event/pets-by-procedure/?procedure_id=${procedureId}`)
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
      });
  });

