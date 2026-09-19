from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_is_server_rendered():
    response = client.get("/")
    assert response.status_code == 200
    assert "Reformas bien hechas" in response.text
    assert 'rel="canonical"' in response.text
    assert 'application/ld+json' in response.text


def test_services_page_is_indexable():
    response = client.get("/servicios")
    assert response.status_code == 200
    assert "Servicios de reformas" in response.text
    assert "Reformas de cocina" in response.text


def test_sitemap_contains_public_pages():
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert "http://testserver/" in response.text
    assert "http://testserver/servicios" in response.text


def test_robots_points_to_sitemap():
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert "Sitemap: http://testserver/sitemap.xml" in response.text
    assert "Disallow: /health" in response.text


def test_health_endpoint():
    assert client.get("/health").json() == {"status": "healthy"}


def test_missing_page_returns_rendered_404():
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert "Esta pagina no existe" in response.text
