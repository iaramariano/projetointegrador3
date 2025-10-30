import pytest
from model_bakery import baker

@pytest.mark.django_db
def test_home_accessible(client):
    url = "/"  # route: ""
    resp = client.get(url)
    # home pode exigir login em algum momento, então aceitamos 200 ou 302
    assert resp.status_code in (200, 302)

@pytest.mark.django_db
def test_petlist_accessible(client):
    url = "/petlist"  # route: "petlist" (sem barra final conforme URL MAP)
    resp = client.get(url)
    assert resp.status_code in (200, 302)

@pytest.mark.django_db
def test_pet_view_accessible(client):
    pet = baker.make("pets.PetsMod")
    url = f"/pet/view/{pet.pk}"  # route: "pet/view/<int:id_pet>"
    resp = client.get(url)
    assert resp.status_code in (200, 302, 404)  # 404 se a view validar owner/estado etc.
