import pytest

DOG_EVENT_URL = "/dog_medical_event"
SECTOR_EVENT_URL = "/sector_medical_event"

@pytest.mark.django_db
def test_dog_medical_event_requires_login(client):
    resp = client.get(DOG_EVENT_URL)
    assert resp.status_code in (302, 401, 403)

@pytest.mark.django_db
def test_sector_medical_event_requires_login(client):
    resp = client.get(SECTOR_EVENT_URL)
    assert resp.status_code in (302, 401, 403)

@pytest.mark.django_db
def test_dog_medical_event_authenticated_get(client, django_user_model):
    user = django_user_model.objects.create_user("u", "u@test.com", "pw")
    client.force_login(user)
    resp = client.get(DOG_EVENT_URL)
    # Se a view tiver guards adicionais, pode redirecionar — mantemos tolerante
    assert resp.status_code in (200, 302)

@pytest.mark.django_db
def test_sector_medical_event_authenticated_get(client, django_user_model):
    user = django_user_model.objects.create_user("u", "u@test.com", "pw")
    client.force_login(user)
    resp = client.get(SECTOR_EVENT_URL)
    assert resp.status_code in (200, 302)
