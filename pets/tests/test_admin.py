import pytest
from django.urls import reverse
from model_bakery import baker

@pytest.mark.django_db
def test_admin_changelist_pets(superuser, client):
    from pets.models import PetsMod

    # Garante que há pelo menos 1 registro
    baker.make(PetsMod, name="Doggo")

    client.force_login(superuser)
    app_label = PetsMod._meta.app_label
    model_name = PetsMod._meta.model_name
    url = reverse(f"admin:{app_label}_{model_name}_changelist")

    resp = client.get(url)
    assert resp.status_code == 200

    body = resp.content
    # Form de changelist é consistente
    assert b'id="changelist-form"' in body or b'class="change-list"' in body
    # Checkbox de seleção em massa é um bom sinal de que a lista está renderizada
    assert b'name="_selected_action"' in body or b'class="action-select"' in body
