from typing import Any


def absolute_url(site_url: str, path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return f"{site_url}{path if path.startswith('/') else '/' + path}"


def business_schema(site: dict[str, Any], site_url: str) -> dict[str, Any]:
    schema: dict[str, Any] = {
        "@type": site.get("business_type", "LocalBusiness"),
        "@id": f"{site_url}#business",
        "name": site["name"],
        "description": site["description"],
        "url": site_url,
    }
    for key in ("logo", "image"):
        if site.get(key):
            schema[key] = absolute_url(site_url, site[key])
    for key in ("phone", "email"):
        if site.get(key):
            schema[key] = site[key]
    address = site.get("address")
    if address:
        schema["address"] = {
            "@type": "PostalAddress",
            "streetAddress": address.get("street"),
            "addressLocality": address.get("city"),
            "addressRegion": address.get("region"),
            "postalCode": address.get("postal_code"),
            "addressCountry": address.get("country", "ES"),
        }
    if site.get("service_area"):
        schema["areaServed"] = [{"@type": "City", "name": area} for area in site["service_area"]]
    if site.get("map_url"):
        schema["hasMap"] = site["map_url"]
    if site.get("opening_hours"):
        schema["openingHours"] = site["opening_hours"]
    if site.get("amenities"):
        schema["amenityFeature"] = [{"@type": "LocationFeatureSpecification", "name": item, "value": True} for item in site["amenities"]]
    if site.get("social"):
        schema["sameAs"] = site["social"]
    return schema


def page_schema(site: dict[str, Any], site_url: str, canonical_url: str, title: str, description: str, page_type: str = "WebPage") -> dict[str, Any]:
    return {
        "@context": "https://schema.org",
        "@graph": [
            business_schema(site, site_url),
            {
                "@type": page_type,
                "@id": f"{canonical_url}#webpage",
                "url": canonical_url,
                "name": title,
                "description": description,
                "inLanguage": site.get("language", "es"),
                "about": {"@id": f"{site_url}#business"},
            },
        ],
    }


def faq_schema(faqs: list[dict[str, str]]) -> dict[str, Any] | None:
    if not faqs:
        return None
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {"@type": "Answer", "text": item["answer"]},
            }
            for item in faqs
        ],
    }
