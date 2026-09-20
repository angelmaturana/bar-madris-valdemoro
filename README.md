# Bar Madris · Web local

Starter minimo para crear webs locales de dos paginas, renderizadas en servidor y preparadas para SEO y Render.

## Incluye

- FastAPI + Jinja2.
- Pagina de inicio y carta del bar en `/carta`.
- Contenido del negocio centralizado en `app/content/site.json` y la carta en `app/content/carta.json`.
- SEO por pagina: title, description, canonical, Open Graph y Twitter Cards.
- JSON-LD para el negocio, la pagina y las FAQ.
- `robots.txt`, `sitemap.xml`, favicon y pagina 404.
- `/health` para Render y `/keepalive` para monitorizacion externa.
- Tests de las rutas principales.
- `PROMPT.md` para pedir a una IA la personalizacion de un sitio.

## Inicio local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Abre `http://localhost:8000`.

## Contenido

1. Edita `app/content/site.json` con los datos del local.
2. Edita `app/content/carta.json` para actualizar la carta.
3. Sustituye los recursos de `app/static/images/` si es necesario.
4. Define `PUBLIC_SITE_URL` en Render.
5. Ejecuta `pytest`.

La aplicacion no inventa datos: los campos ausentes deben omitirse del contenido y del marcado estructurado.

## Render

`render.yaml` ya define el servicio web y el health check. El comando usa el puerto que Render proporciona:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Configura `PUBLIC_SITE_URL` con el dominio publico definitivo. Se usa para canonical, sitemap, Open Graph y JSON-LD.

Para evitar dependencia de un hilo interno, se recomienda usar un monitor externo que consulte `/health`. `/keepalive` queda disponible para ese uso, pero esta desactivado de los robots de buscadores.

## Estructura

```text
app/
  main.py                 Rutas y renderizado
  config.py               Carga de configuracion y URL publica
  seo.py                  Generacion de JSON-LD
  content/site.json       Datos editables del sitio
  templates/              Paginas y parciales Jinja
  static/                 CSS e imagenes estaticas
render.yaml               Configuracion de Render
PROMPT.md                 Prompt de personalizacion
 tests/                   Validaciones HTTP
```
