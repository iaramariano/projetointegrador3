import pytest
from model_bakery import baker

@pytest.mark.django_db
def test_pet_create_requires_login(client):
    url = "/pet/create"  # route: "pet/create"
    resp = client.get(url)
    assert resp.status_code in (302, 401, 403)

@pytest.mark.django_db
def test_pet_create_authenticated_get(client, django_user_model):
    user = django_user_model.objects.create_user("u", "u@test.com", "pw")
    client.force_login(user)
    url = "/pet/create"
    resp = client.get(url)
    assert resp.status_code in (200, 302)  # se houver guard extra, pode redirecionar

@pytest.mark.django_db
def test_pet_update_requires_login(client):
    pet = baker.make("pets.PetsMod")
    url = f"/pet/update/{pet.pk}"  # route: "pet/update/<int:id_pet>"
    resp = client.get(url)
    assert resp.status_code in (302, 401, 403)

@pytest.mark.django_db
def test_pet_update_authenticated_get(client, django_user_model):
    user = django_user_model.objects.create_user("u", "u@test.com", "pw")
    client.force_login(user)
    pet = baker.make("pets.PetsMod")
    url = f"/pet/update/{pet.pk}"
    resp = client.get(url)
    assert resp.status_code in (200, 302)  # tolerante a middlewares/guards
