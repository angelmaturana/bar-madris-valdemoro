# Prompt para generar un sitio

Usa esta plantilla FastAPI + Jinja para crear una web local de dos paginas.

## Datos del negocio

- Nombre:
- Tipo de negocio:
- Descripcion:
- Ciudad y provincia:
- Direccion:
- Telefono:
- Email:
- WhatsApp:
- Horario:
- Zonas donde trabaja:
- Servicios principales:
- Accion principal que quiero conseguir:
- Estilo visual:
- Colores:

## Reglas

- Mantén FastAPI + Jinja y el renderizado server-side.
- Mantén `/`, `/servicios`, `/robots.txt`, `/sitemap.xml`, `/health` y `/keepalive`.
- Modifica primero `app/content/site.json`.
- Usa `app/static/images/` para logo, favicon e imagen Open Graph.
- No uses React ni JavaScript para renderizar contenido esencial.
- No anadas base de datos, CMS ni subida de archivos.
- No inventes horarios, reseñas, precios, coordenadas, certificaciones o datos legales.
- Si falta un dato, omite esa seccion.
- Usa `PUBLIC_SITE_URL` para todas las URLs absolutas.
- Genera title, description, canonical, Open Graph, Twitter Cards y JSON-LD valido.
- Mantén el contenido principal visible en el HTML inicial.
- Comprueba que las paginas responden correctamente y ejecuta `pytest`.
- Mantén el arranque compatible con Render usando `$PORT`.
