---
name: krea-apps
description: Estándar y forma de trabajar de KREA Digital Studio para proyectos de clientes (apps de gestión, presupuestos, fichajes, reservas, paneles, y también webs y portafolios). Usar SIEMPRE que se cree o mejore una app, una web o un portafolio: toda app se entrega instalable en móvil y ordenador, con los mismos datos sincronizados en la nube, acceso privado, PDF y envío por WhatsApp/correo, demo aparte, y todo proyecto termina con portafolio web y PDF con el © de KREA Digital Studio.
---

# Apps de clientes · estándar KREA

Una app de KREA no es una página: el cliente la usa **a diario en el móvil (≈80 %)** y **se sienta al ordenador para el trabajo largo (≈20 %)**. Todo lo de abajo viene incluido desde la primera versión, sin que Kike tenga que pedirlo.

## 1. Mismo enlace, móvil y ordenador, mismos datos

- **App instalable (PWA)** con `manifest.webmanifest`, iconos 192/512 (y maskable), `apple-touch-icon` y botón **«Instalar en este equipo / en el móvil»** dentro de la app (con instrucciones para iPhone).
- **Diseño adaptado**: en ordenador, menú lateral; en móvil, barra de pestañas abajo y botón «+» grande. Comprobar a 390 px de ancho sin desplazamiento lateral.
- **Datos en la nube desde el día 1**, nunca solo en el navegador. Por defecto **Supabase**:
  - Región **UE** (París o Fráncfort) y plan gratuito.
  - **Auth con correo y contraseña** del cliente (la misma en todos sus dispositivos).
  - Tablas con **RLS por `user_id`**: cada usuario solo ve lo suyo.
  - Sincronización: guardar al cambiar (con *debounce*), refrescar al volver a la app y con *realtime*; copia local para consultar sin cobertura y reintento al volver la conexión.
- Solo si el cliente no quiere nube: datos en el dispositivo, avisándole **por escrito** de que no se pasan entre móvil y ordenador.

## 2. Montar Supabase

- Si el conector **Supabase** está conectado en claude.ai, Claude crea el proyecto, las tablas, las políticas RLS y las Edge Functions él mismo.
- Si no, Kike crea el proyecto en https://supabase.com (nombre `krea-<proyecto>`, región UE) y pasa a Claude **Project URL** y **anon public key**. Esas dos se pueden poner en el código.
- **Nunca** pedir, pegar ni subir la `service_role` ni la contraseña de la base de datos.
- Claves de terceros (Claude API, etc.) solo como **secretos de Edge Functions**, nunca en el código del navegador.
- **Patrón probado (SGM):** tabla `<app>_state (user_id, data jsonb, rev)` con RLS por `auth.uid()`; tabla `<app>_allowed_emails` y *trigger* `before insert on auth.users` que rechaza correos no autorizados y los confirma automáticamente; quitar permisos a `anon`. En el navegador, `fetch` directo a `/auth/v1` y `/rest/v1` (sin librerías), guardado con control de versión (`PATCH ...?rev=eq.N`) y fusión por `id` si dos dispositivos guardan a la vez.
- Pedir a Kike en el panel de Supabase: **Authentication → URL Configuration → Site URL** = la dirección de la app (para los correos de «he olvidado la contraseña») y desactivar **Confirm email** si se usa la lista de correos autorizados.

## 3. Lo que lleva toda app de gestión

- **Acceso privado**: pantalla de entrada con la imagen corporativa y solo los usuarios del cliente. Sin textos de «demo» ni contraseñas visibles.
- **Empieza a cero**: la app del cliente sin datos de ejemplo; como mucho su tarifa o catálogo de base.
- **Datos personales fuera del repositorio** (aunque el repo sea privado): NIF, dirección, IBAN, correos… se meten en Ajustes, en la base de datos o con un enlace personal `#datos=` que solo se manda al cliente.
- **Documentos PDF** con la imagen corporativa: fechas en texto, importes con punto de miles, IVA, forma de pago, número de página y firma.
- **Enviar por WhatsApp o correo** con el PDF adjunto mediante el menú «Compartir» del sistema (Web Share API con archivos), con el mensaje ya escrito, y marcar el documento como enviado.
- **Agenda del móvil**: Contact Picker en Android y archivo `.vcf` en iPhone/ordenador.
- **Asistente con IA** cuando ayude (presupuestos, informes): llamada a Claude desde una Edge Function.
- **Copia de seguridad** descargable y restaurable en Ajustes.

## 4. Publicar

- Repositorio y subdominio según la skill **krea-repos** (`krea-<proyecto>`, `<cliente>.kreadigitalstudio.es`, HTTPS obligatorio).
- **Service worker** limitado a las páginas de la app (no cachear `/demo/`, `/portafolio/` ni otras apps del mismo subdominio) y con nombre de caché versionado. Si el subdominio venía de otra plataforma, el SW nuevo debe sustituir al anterior y recargar.
- Varias apps del mismo cliente: `/<proyecto>/` en el mismo subdominio.

## 4b. Blindaje: repositorio privado y protección anticopia (todos los proyectos)

Desde octubre de 2026 todo proyecto de KREA (apps, webs, portafolios y la web de KREA) va **blindado**, como Gastobra y Gastoticket:

- **Repositorio privado** en GitHub: el código no se enseña. Kike lo crea privado (o lo cambia en Settings → General → Danger Zone → Change visibility).
- **Publicación en el hosting de OVH** (ya pagado), no en GitHub Pages: multisitio `<cliente>.kreadigitalstudio.es` → carpeta propia, y un workflow `.github/workflows/publicar-ovh.yml` que sube por FTP solo los archivos de la web (secreto `OVH_FTP_PASSWORD`, que teclea Kike). Servidor `ftp.cluster131.hosting.ovh.net`.
- **`.htaccess`** en la raíz publicada: https obligatorio, `Options -Indexes`, `X-Frame-Options SAMEORIGIN` y `frame-ancestors 'self'` (nadie la mete dentro de otra web), `nosniff`, y bloquear README y archivos internos.
- **Aviso legal de propiedad intelectual** en el pie y en la página legal: diseño, código, textos, fotos y capturas de KREA o del cliente; prohibida la copia total o parcial sin autorización por escrito.
- **Imágenes protegidas**: sin menú de guardar imagen ni arrastrar (`contextmenu`/`dragstart` en `img`, `-webkit-user-drag:none`). Sin bloquear la selección de texto ni el teclado: no debe estorbar al cliente ni a la accesibilidad.
- Apps privadas: pantalla de acceso con cuenta y RLS; webs en presentación: acceso con código (como JP Fútbol).
- Decirlo claro a Kike: lo que el navegador muestra siempre se puede ver y guardar; el blindaje evita el acceso al código del repositorio, dificulta la copia y deja constancia legal de la autoría.

## 5. Entregar

- **Demo pública** en `/demo/` con su propio acceso: empieza vacía y en Ajustes tiene «Cargar datos de ejemplo» y «Empezar de cero». Claves de sesión separadas de la app real.
- **Portafolio** en `/portafolio/` (caso de estudio con capturas reales de ordenador y móvil y botones «Entrar en la app») y su **PDF** con todos los enlaces absolutos y clicables, listo para Drive y WhatsApp.
- **Pie con el distintivo de KREA, siempre**, en el portafolio web, en su PDF y en el pie de toda web de cliente: `© <año> KREA Digital Studio · Diseño y desarrollo · Todos los derechos reservados`, con enlace a https://kreadigitalstudio.es. En las apps, «Desarrollado por KREA Digital Studio» en la pantalla de acceso o en Ajustes.
- **Mensaje de WhatsApp** listo para el cliente: enlace, crear contraseña, instalar en móvil y ordenador, qué rellenar en Ajustes.

## 6. Forma de trabajar con Kike (igual en apps, webs y portafolios)

1. Primera versión completa y **enlace para verla** (artifact o subdominio) cuanto antes; Kike entra, prueba y pide cambios en el mismo hilo.
2. Cada proyecto en **su repositorio privado** y **su subdominio** de kreadigitalstudio.es (skill **krea-repos** y apartado 4b). Kike crea el repositorio en GitHub y el multisitio en OVH; Claude publica y comprueba desde fuera el candado y la redirección de http a https antes de decir que está listo.
3. Guiar a Kike en paneles (Supabase, OVH, GitHub) **paso a paso y con capturas**: qué botón, qué escribir exactamente y qué debe verse después.
4. Al cerrar: comprobar todas las direcciones (app, demo, portafolio, direcciones antiguas), dejar el portafolio y su PDF al día y preparar el **mensaje de WhatsApp** para el cliente.
5. Lo aprendido en cada proyecto se añade a estas skills.

## Comprobación antes de dar el enlace

- [ ] Entra en móvil y ordenador con la misma cuenta y ve los mismos datos.
- [ ] Se instala con icono en Android, iPhone y ordenador.
- [ ] PDF correcto y envío por WhatsApp/correo probado en un móvil real.
- [ ] HTTPS activo y verificado con certificado válido en todas las direcciones.
- [ ] Sin datos personales del cliente en el repositorio.
- [ ] Repositorio privado, publicado en OVH con `.htaccess`, aviso de propiedad intelectual e imágenes protegidas (apartado 4b).
- [ ] Demo y portafolio actualizados, con el © de KREA Digital Studio al pie de la web y del PDF.
