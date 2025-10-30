import pytest
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from model_bakery import baker

@pytest.mark.django_db
def test_pet_str_returns_name():
    pet = baker.make("pets.PetsMod", name="Rex")
    assert str(pet) == "Rex"

@pytest.mark.django_db
def test_pet_birth_cannot_be_future():
    pet = baker.prepare("pets.PetsMod", birth=date.today() + timedelta(days=1))
    with pytest.raises(ValidationError):
        pet.full_clean()  # exige que o modelo tenha validação em clean()/clean_fields()
