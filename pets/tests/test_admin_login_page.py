def test_admin_login_page_accessible(client):
    resp = client.get("/admin/login/")
    # Deve responder 200 com o formulário de login
    assert resp.status_code == 200
    assert b"username" in resp.content or b"usu\xc3\xa1rio" in resp.content
