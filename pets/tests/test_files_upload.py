import pytest
from model_bakery import baker

@pytest.mark.django_db
def test_pet_accepts_image_upload(image_file, settings):
    # Ajuste os nomes dos campos conforme o seu modelo (ex.: front_photo/side_photo/size_photo)
    pet = baker.make("pets.PetsMod", front_photo=image_file)
    pet.refresh_from_db()
    assert pet.front_photo.name  # caminho salvo
