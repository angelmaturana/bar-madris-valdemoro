from typing import Any


def absolute_url(site_url: str, path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return f"{site_url}{path if path.startswith('/') else '/' + path}"


WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def _day_indices(day_range: str) -> list[str]:
    """Convierte algo como 'Monday-Friday' o 'Saturday' en lista de días."""
    parts = [d.strip() for d in day_range.split(",")]
    days: list[str] = []
    for part in parts:
        if "-" in part:
            start, end = part.split("-", 1)
            i = WEEKDAYS.index(start.strip().strip("[]"))
            j = WEEKDAYS.index(end.strip().strip("[]"))
            days.extend(WEEKDAYS[i : j + 1])
        else:
            days.append(part.strip())
    return days


def opening_hours_specification(spec: list[dict[str, Any]]) -> list[dict[str, Any]] | None:
    """Genera openingHoursSpecification a partir de un listado estructurado."""
    out: list[dict[str, Any]] = []
    for item in spec:
        days = item.get("day")
        if isinstance(days, str):
            day_list = _day_indices(days)
        elif isinstance(days, list):
            day_list = []
            for d in days:
                if isinstance(d, str) and "-" in d:
                    day_list.extend(_day_indices(d))
                else:
                    day_list.append(d)
        else:
            day_list = []
        for day in day_list:
            entry: dict[str, Any] = {"@type": "OpeningHoursSpecification", "dayOfWeek": day}
            if item.get("open"):
                entry["opens"] = item["open"]
            if item.get("close"):
                entry["closes"] = item["close"]
            out.append(entry)
    return out or None


def business_schema(site: dict[str, Any], site_url: str) -> dict[str, Any]:
    schema: dict[str, Any] = {
        "@type": site.get("business_type", "LocalBusiness"),
        "@id": f"{site_url}#business",
        "name": site["name"],
        "alternateName": site.get("alternate_name"),
        "description": site["description"],
        "url": site_url,
        "serviceType": "bar, cafetería, tapas, desayunos, raciones",
        "priceRange": "moderado",
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
        schema["areaServed"] = [{"@type": "Place", "name": area, "address": {"addressLocality": area, "addressRegion": "Madrid", "addressCountry": "ES"}} for area in site["service_area"]]
    if site.get("map_url"):
        schema["hasMap"] = {"@type": "Map", "url": site["map_url"]}
    if site.get("opening_hours_specification"):
        spec = opening_hours_specification(site["opening_hours_specification"])
        if spec:
            schema["openingHoursSpecification"] = spec
    elif site.get("opening_hours"):
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

