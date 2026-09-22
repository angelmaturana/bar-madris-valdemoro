from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_is_server_rendered():
    response = client.get("/")
    assert response.status_code == 200
    assert "El bar de toda la vida" in response.text
    assert 'rel="canonical"' in response.text
    assert 'application/ld+json' in response.text


def test_home_has_about_and_location_sections():
    response = client.get("/")
    text = response.text
    assert "La historia de Bar Madris" in text
    assert "Cómo llegar a Bar Madris" in text
    assert "Ver en Google Maps" in text


def test_home_json_ld_has_local_seo():
    response = client.get("/")
    assert "openingHoursSpecification" in response.text
    assert "areaServed" in response.text
    assert "serviceType" in response.text
    assert "BarOrPub" in response.text


def test_home_has_local_keywords():
    response = client.get("/")
    text = response.text.lower()
    assert "valdemoro" in text
    assert "bar de tapas" in text
    assert "dónde ver el fútbol" in text or "fútbol en valdemoro" in text


def test_home_has_keywords_meta():
    response = client.get("/")
    assert 'name="keywords"' in response.text
    assert "valdemoro" in response.text.lower()


def test_menu_page_is_indexable():
    response = client.get("/carta")
    assert response.status_code == 200
    assert "Carta de Bar Madris" in response.text
    assert "Papas Bravas" in response.text


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
