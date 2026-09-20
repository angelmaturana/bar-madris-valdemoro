from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_is_server_rendered():
    response = client.get("/")
    assert response.status_code == 200
    assert "El bar de toda la vida" in response.text
    assert 'rel="canonical"' in response.text
    assert 'application/ld+json' in response.text


def test_menu_page_is_indexable():
    response = client.get("/carta")
    assert response.status_code == 200
    assert "Carta de Bar Madris" in response.text
    assert "Patatas Bravas 3 Salsas" in response.text


def test_sitemap_contains_public_pages():
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert "http://testserver/" in response.text
    assert "http://testserver/carta" in response.text


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
    assert "Esta página no existe" in response.text
