# Prompt para generar un sitio

Usa esta plantilla FastAPI + Jinja para crear una web local de dos paginas.

## Datos del negocio

Nombre: Bar Madris (Real Café Madris)
Tipo de negocio: Bar de tapas / Cafetería
Descripcion: Un bar de toda la vida y lugar mítico de Valdemoro muy popular por su buen ambiente, sus raciones, sus sabrosas tapas y desayunos. Cuenta con asientos al aire libre y es accesible. Ademas cuando hay partidos de futbol importantes es el bar con mas ambiente de todo valdemoro.
Ciudad y provincia: Valdemoro, Madrid (Comunidad de Madrid)
Direccion: Calle de la Guardia Civil, 5, 28341 Valdemoro, Madrid
Telefono: +34 918 08 00 07
Horario: Lunes a viernes: 06:30/07:00 a 00:00  Sábados y domingos: 08:00 a 00:00
Zonas donde trabaja: Local físico en Valdemoro (zona Parque de las Víctimas del Terrorismo / Guardia Civil)
Servicios principales: Desayunos, cafés, cañas, tapas, raciones variadas y servicio en terraza.
- Accion principal que quiero conseguir: Presencia y posicionamiento
- Estilo visual: Que se un diseño limpio moderno y actual. Analizando las imagenes logo.png y bar-madris-valdemoro.png decidiras el estilo exacto
- Colores: Fondo oscuro y Analizando las imagenes logo.png y bar-madris-valdemoro.png decidiras los colores.

## Reglas

- Mantén FastAPI + Jinja y el renderizado server-side.
- Mantén `/`, `/carta`, `/robots.txt`, `/sitemap.xml`, `/health` y `/keepalive`.
- Analiza primero `app/content/site.json` que es de un bar de tapas . Sabiendo que es de un Bar que debe tener la ruta /carta. La pagina "/carta" tendra el contenido que hay en "carta.pdf"
- Usa `app/static/images/` para logo de la web, y usa la imagen del bar bar-madris-valdemoro.png en la home en la seccion "hero", la imagen puede ir de fondo oscurecida y que se vean bien los textos que van dentro de esta seccion. 
- La /carta sera una pagina con la carta del bar. El contenido de la pagina /carta sera leida del fichero carta.json. carta.json se lee una sola vez al iniciar el servidor.
- Haz los contenidos para que tenga un excelente SEO y GEO para las IAs, para que sea encontrado como Bar en Valdemoro, Tapas en Valdemoro, donde ver el futbol en valdemoro, el mejor bar de Valdemoro y lo que creas conveniente para que sea encontrado en google y en IAs.
- Debes rehacer el favicon y la imagen Open Graph og-image.svg, debes rehacerlos acorde a la web.
- No uses React ni JavaScript para renderizar contenido esencial.
- No anadas base de datos, CMS ni subida de archivos.
- No inventes horarios, reseñas, precios, coordenadas, certificaciones o datos legales.
- Si falta un dato, omite esa seccion.
- Usa `PUBLIC_SITE_URL` para todas las URLs absolutas.
- Genera title, description, canonical, Open Graph, Twitter Cards y JSON-LD valido.
- Mantén el contenido principal visible en el HTML inicial.
- Comprueba que las paginas responden correctamente y ejecuta `pytest`.
- Mantén el arranque compatible con Render usando `$PORT`.
