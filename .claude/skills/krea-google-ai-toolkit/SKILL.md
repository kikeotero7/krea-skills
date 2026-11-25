---
name: "krea-google-ai-toolkit"
description: "Usar en proyectos de KREAVANCE (webs, apps, logos, branding, marca personal, foto, vídeo, agentes IA) para elegir y preparar las herramientas IA de Google."
---

# Kit IA de Google — KREAVANCE

Objetivo: que cada proyecto de cliente salga con calidad máxima combinando lo que construye Claude (código, webs, apps, artifacts, Figma/Canva) con las herramientas IA de Google (gratis o con límite gratuito).

Importante: estas herramientas son apps web de Google con la cuenta del usuario. Claude NO las ejecuta por API. Claude elige la herramienta, redacta prompts listos para pegar, y después integra lo que el usuario trae (o las maneja con el navegador integrado si el usuario tiene la sesión de Google abierta y lo pide).

## 1. Mapa rápido por tipo de proyecto

| Proyecto | Herramientas | Uso |
|---|---|---|
| Web / landing | Stitch → Claude; Nano Banana; Veo | Stitch para explorar 2-3 direcciones de pantalla; Claude construye la versión final en código; imágenes hero con Nano Banana; vídeo de fondo con Veo |
| App | Stitch; AI Studio; Jules | Pantallas en Stitch, prototipo rápido en AI Studio, Jules para tests/bugs del repo |
| Logo / identidad | Mixboard; Flow (ex Whisk); GenType; Nano Banana | Moodboard en Mixboard, mezcla de referencias en Flow, tipografía a medida en GenType; vectorizar y cerrar en Figma/Canva |
| Marca personal / redes | Pomelli; Sparkify; Flow Music | Pomelli lee la web del cliente y genera posts con su identidad; Sparkify para reels cortos; Flow Music para jingles/fondos |
| Fotografía | Nano Banana; Mixboard | Mejorar fotos reales del cliente (fondo, luz, limpieza), mockups de producto, variaciones de escena |
| Vídeo | Veo; Flow; Sparkify | Clips cinematográficos (Veo), escenas compuestas (Flow), explicativos animados (Sparkify) |
| Agentes IA / automatización | Opal; AI Studio | Opal para flujos sin código con Gemini (alternativa a n8n/Make); AI Studio para prototipar agentes/chatbots |
| Desarrollo | Antigravity; Jules | Alternativa a Claude Code/Cursor; Jules en segundo plano sobre GitHub |
| Entrega y formación al cliente | Gemini Notebook; Learn Your Way | Dossier → resumen, infografía o pódcast; manual de uso → ruta de aprendizaje |

## 2. Fichas

- Antigravity — antigravity.google — editor de código con IA. Límite gratis.
- Stitch — stitch.withgoogle.com — texto → diseño de pantalla app/web.
- Flow (antes Whisk, fusionada 30/04/2026) — labs.google/fx/tools/flow — combina imágenes de referencia; también vídeo.
- Pomelli — labs.google/pomelli — aprende marca desde una URL y crea contenido para redes.
- Opal — opal.google — automatizaciones encadenadas sin código.
- Google AI Studio — aistudio.google.com — apps por conversación; aquí vive Nano Banana. Límite gratis.
- Gemini Notebook (antes NotebookLM) — notebook.google.com — resumen, infografía, pódcast. Límite gratis.
- Mixboard — labs.google/mixboard — tablero de imágenes IA combinables. Límite gratis.
- Nano Banana — en AI Studio — generación y edición de imagen. Límite gratis.
- Veo — gemini.google.com — generación de vídeo. Límite gratis.
- Flow Music — labs.google/fx/tools/music-fx — canciones IA. Límite gratis.
- Jules — jules.google — agente de código asíncrono. Límite gratis.
- Learn Your Way — learnyourway.withgoogle.com — rutas de aprendizaje. Gratis.
- GenType — labs.google/gentype — alfabeto completo a partir de un estilo. Gratis.
- Sparkify — sparkify.withgoogle.com — idea → vídeo corto animado. Gratis.
- Fuera de la lista: Gemini Omni (vídeo, sin versión gratis).

## 3. Flujo de trabajo estándar

1. Brief del cliente: sector, público, tono, colores, referencias, entregables.
2. Claude propone qué herramientas usar (tabla del punto 1) y por qué, en 3-5 líneas.
3. Claude entrega un bloque de prompts listos para pegar, uno por herramienta, en inglés si mejora el resultado y con la versión en español al lado.
4. El usuario ejecuta y sube los resultados al chat (o Claude usa el navegador integrado si se le pide y hay sesión).
5. Claude integra: optimiza imágenes (WebP/AVIF, tamaños responsive), comprime vídeo (MP4 H.264 + WebM, poster), vectoriza/limpia logos, monta la web/app y la publica como enlace para revisar (subdominio de kreavance.es en los proyectos nuevos; los ya publicados siguen en kreadigitalstudio.es hasta migrarlos).
6. Entrega al cliente: dossier en Docs/Slides + opcional pódcast o infografía con Gemini Notebook.

## 4. Plantillas de prompt

- Stitch: "[Tipo de pantalla] para [negocio] dirigido a [público]. Estilo [adjetivos], paleta [hex], tipografía [serif/sans]. Secciones: [lista]. Móvil primero. CTA principal: [acción]."
- Nano Banana (foto): "Fotografía editorial de [sujeto] en [escena], luz [natural suave/estudio], objetivo 50mm, profundidad de campo baja, paleta [colores de marca], sin texto, 4K."
- Nano Banana (edición): "Mantén al sujeto idéntico; cambia el fondo a [escena]; iguala la luz; elimina [elemento]."
- Veo: "Plano [tipo] de [acción], cámara [movimiento lento], ambiente [luz/hora], estética [cinematográfica/minimal], 8 s, sin texto en pantalla, apto para hero web en bucle."
- GenType: "Alfabeto inspirado en [concepto], trazo [grosor], [geométrico/orgánico], para marca de [sector]."
- Pomelli: URL de la web del cliente + "campaña de [objetivo] para [red], 6 piezas, tono [x]."
- Opal: describir disparador → pasos → salida (ej. "cuando llega un formulario, resume la petición, clasifica el lead y redacta respuesta").

## 5. Reglas

- Google renombra y mueve estas herramientas a menudo: antes de recomendar una, verificar nombre y URL con una búsqueda rápida.
- Revisar los términos de uso comercial de cada herramienta antes de entregar a un cliente; las imágenes y vídeos de Google llevan marca SynthID.
- No generar imágenes de personas reales del cliente sin su consentimiento, ni imitar marcas, logos o personajes de terceros.
- Los logos finales se entregan en vector (SVG/PDF) y revisados a mano; la IA es para explorar, no para el archivo final.
- Avisar del límite gratuito cuando el volumen del proyecto pueda superarlo.