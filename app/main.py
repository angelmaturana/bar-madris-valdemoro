import json
from pathlib import Path
from xml.etree import ElementTree

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import load_site, public_site_url
from .seo import absolute_url, faq_schema, page_schema


BASE_DIR = Path(__file__).resolve().parent
site_data = load_site()
carta_path = BASE_DIR / "content" / "carta.json"
with carta_path.open(encoding="utf-8") as file:
    carta_data = json.load(file)
menu_sections = []
for section_name, section in carta_data["secciones"].items():
    groups = []
    if isinstance(section, list):
        groups.append((None, section))
    else:
        for group_name, items in section.items():
            if isinstance(items, list):
                groups.append((group_name, items))
    menu_sections.append({"name": section_name, "note": section.get("nota") if isinstance(section, dict) else None, "groups": groups})
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
templates.env.globals["absolute_url"] = absolute_url

app = FastAPI(title=site_data["site"]["name"], docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


def page_context(request: Request, path: str, title: str, description: str, page_type: str = "WebPage") -> dict:
    site = site_data["site"]
    site_url = public_site_url(str(request.url))
    canonical_url = absolute_url(site_url, path)
    structured_data = page_schema(site, site_url, canonical_url, title, description, page_type)
    return {
        "site": site,
        "theme": site_data["theme"],
        "seo": site_data["seo"],
        "site_url": site_url,
        "canonical_url": canonical_url,
        "page_title": title,
        "page_description": description,
        "structured_data": structured_data,
    }


@app.get("/", name="home")
async def home(request: Request):
    home_data = site_data["home"]
    context = page_context(
        request,
        "/",
        site_data["seo"]["title"],
        site_data["seo"]["description"],
    )
    context.update({"request": request, "home": home_data})
    faq = faq_schema(home_data.get("faqs", []))
    if faq:
        context["structured_data"]["@graph"].append(faq)
    return templates.TemplateResponse(request=request, name="home.html", context=context)


@app.get("/carta", name="menu")
async def menu(request: Request):
    context = page_context(
        request,
        "/carta",
        "Carta de Bar Madris | Tapas, raciones y desayunos",
        "Consulta la carta de Bar Madris en Valdemoro: tapas, raciones, cervezas, vinos, cafés y desayunos.",
        "Menu",
    )
    context.update({"request": request, "carta": carta_data, "menu_sections": menu_sections})
    return templates.TemplateResponse(request=request, name="services.html", context=context)


@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots(request: Request):
    site_url = public_site_url(str(request.url))
    return PlainTextResponse("\n".join([
        "User-agent: *",
        "Allow: /",
        "Disallow: /health",
        "Disallow: /keepalive",
        "Disallow: /docs",
        "Disallow: /redoc",
        f"Sitemap: {site_url}/sitemap.xml",
        "",
    ]))


@app.get("/sitemap.xml")
async def sitemap(request: Request):
    site_url = public_site_url(str(request.url))
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    root = ElementTree.Element(f"{{{namespace}}}urlset")
    for path in ("/", "/carta"):
        entry = ElementTree.SubElement(root, f"{{{namespace}}}url")
        ElementTree.SubElement(entry, f"{{{namespace}}}loc").text = absolute_url(site_url, path)
    ElementTree.register_namespace("", namespace)
    return Response(ElementTree.tostring(root, encoding="utf-8", xml_declaration=True), media_type="application/xml")


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/keepalive", response_class=PlainTextResponse)
async def keepalive():
    return PlainTextResponse("OK")


@app.exception_handler(404)
async def not_found(request: Request, exc):
    context = page_context(request, str(request.url.path), "Pagina no encontrada", "La pagina solicitada no existe.")
    context["request"] = request
    return templates.TemplateResponse(request=request, name="404.html", context=context, status_code=404)
