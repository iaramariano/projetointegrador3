function createHiddenInput(name, value) {
  const input = document.createElement('input');
  input.type = 'hidden';
  input.name = name;
  input.value = value;
  return input;
}

function joinBirth() {
  const birthMonthEl = document.getElementById('birth_month');
  const birthYearEl = document.getElementById('birth_year');

  if (!birthMonthEl || !birthYearEl) {
    return null;
  }

  const birthMonth = birthMonthEl.value;
  const birthYear = birthYearEl.value;
  if (!birthMonth || !birthYear) {
    return null;
  }

  return createHiddenInput('birth', birthYear + '-' + birthMonth + '-01');
}

function joinVaccine() {
  const vaccineMonthEl = document.getElementById('vaccine_month');
  const vaccineYearEl = document.getElementById('vaccine_year');

  if (!vaccineMonthEl || !vaccineYearEl) {
    return null;
  }

  const vaccineMonth = vaccineMonthEl.value;
  const vaccineYear = vaccineYearEl.value;
  if (!vaccineMonth || !vaccineYear) {
    return null;
  }

  return createHiddenInput('vaccine', vaccineYear + '-' + vaccineMonth + '-01');
}

function joinVermifuge() {
  const vermifugeMonthEl = document.getElementById('vermifuge_month');
  const vermifugeYearEl = document.getElementById('vermifuge_year');

  if (!vermifugeMonthEl || !vermifugeYearEl) {
    return null;
  }

  const vermifugeMonth = vermifugeMonthEl.value;
  const vermifugeYear = vermifugeYearEl.value;
  if (!vermifugeMonth || !vermifugeYear) {
    return null;
  }

  return createHiddenInput('vermifuge', vermifugeYear + '-' + vermifugeMonth + '-01');
}

function submitForm(event) {
  const form = document.getElementById('dog_register');
  if (!form) {
    return;
  }

  const birthInput = joinBirth();
  const vaccineInput = joinVaccine();
  const vermifugeInput = joinVermifuge();
  const needsScriptSubmit = birthInput || vaccineInput || vermifugeInput;

  if (!needsScriptSubmit) {
    return;
  }

  event.preventDefault();
  if (birthInput) form.appendChild(birthInput);
  if (vaccineInput) form.appendChild(vaccineInput);
  if (vermifugeInput) form.appendChild(vermifugeInput);
  form.submit();
}

function previewImage(event, previewId) {
  const input = event.target;
  const preview = document.getElementById(previewId);

  if (input.files && input.files[0]) {
    const reader = new FileReader();

    reader.onload = function(e) {
      preview.src = e.target.result;
      preview.style.display = 'block';
    };

    reader.readAsDataURL(input.files[0]);
  }
}

const dogRegisterForm = document.getElementById('dog_register');
if (dogRegisterForm) {
  dogRegisterForm.addEventListener('submit', submitForm);
}