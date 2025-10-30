import io
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture(autouse=True)
def _media_root_tmp(tmp_path, settings):
    """
    Usa uma pasta de mídia temporária em cada sessão de testes
    """
    media = tmp_path / "media"
    media.mkdir(parents=True, exist_ok=True)
    settings.MEDIA_ROOT = media
    return media

@pytest.fixture(autouse=True)
def _static_root_tmp(tmp_path, settings):
    """
    Garante um STATIC_ROOT válido e existente nos testes,
    evitando o warning 'No directory at: .../staticfiles/'.
    """
    static = tmp_path / "staticfiles"
    static.mkdir(parents=True, exist_ok=True)
    settings.STATIC_ROOT = static
    settings.STATICFILES_DIRS = []
    return static

@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="tester",
        email="tester@example.com",
        password="pw123456",
    )

@pytest.fixture
def superuser(django_user_model):
    return django_user_model.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="pw123456",
    )

@pytest.fixture
def image_file():
    """
    Retorna um SimpleUploadedFile PNG válido para campos ImageField/FileField.
    """
    # PNG mínimo válido (1x1 pixel)
    png_bytes = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\x9cc``\x00\x00"
        b"\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    f = io.BytesIO(png_bytes)
    return SimpleUploadedFile("test.png", f.getvalue(), content_type="image/png")
