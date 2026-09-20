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
- **Keepalive interno opcional**: un cliente HTTP que pinguea tu propia URL para evitar que Render suspenda el servicio por inactividad. Se activa con `KEEPALIVE_URL`.
- Tests de las rutas principales.
- `PROMPT.md` para pedir a una IA la personalizacion de un sitio.

## Inicio local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000