---
name: krea-apps
description: Estándar de KREA Digital Studio para crear apps de clientes (gestión, presupuestos, fichajes, reservas, paneles). Usar SIEMPRE que se cree o mejore una app: toda app se entrega instalable en móvil y ordenador, con los mismos datos sincronizados en la nube, acceso privado, PDF y envío por WhatsApp/correo, demo aparte y portafolio.
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

## 3. Lo que lleva toda app de gestión

- **Acceso privado**: pantalla de entrada con la imagen corporativa y solo los usuarios del cliente. Sin textos de «demo» ni contraseñas visibles.
- **Empieza a cero**: la app del cliente sin datos de ejemplo; como mucho su tarifa o catálogo de base.
- **Datos personales fuera del repositorio** (los repos son públicos): NIF, dirección, IBAN, correos… se meten en Ajustes, en la base de datos o con un enlace personal `#datos=` que solo se manda al cliente.
- **Documentos PDF** con la imagen corporativa: fechas en texto, importes con punto de miles, IVA, forma de pago, número de página y firma.
- **Enviar por WhatsApp o correo** con el PDF adjunto mediante el menú «Compartir» del sistema (Web Share API con archivos), con el mensaje ya escrito, y marcar el documento como enviado.
- **Agenda del móvil**: Contact Picker en Android y archivo `.vcf` en iPhone/ordenador.
- **Asistente con IA** cuando ayude (presupuestos, informes): llamada a Claude desde una Edge Function.
- **Copia de seguridad** descargable y restaurable en Ajustes.

## 4. Publicar

- Repositorio y subdominio según la skill **krea-repos** (`krea-<proyecto>`, `<cliente>.kreadigitalstudio.es`, HTTPS obligatorio).
- **Service worker** limitado a las páginas de la app (no cachear `/demo/`, `/portafolio/` ni otras apps del mismo subdominio) y con nombre de caché versionado. Si el subdominio venía de otra plataforma, el SW nuevo debe sustituir al anterior y recargar.
- Varias apps del mismo cliente: `/<proyecto>/` en el mismo subdominio.

## 5. Entregar

- **Demo pública** en `/demo/` con su propio acceso: empieza vacía y en Ajustes tiene «Cargar datos de ejemplo» y «Empezar de cero». Claves de sesión separadas de la app real.
- **Portafolio** en `/portafolio/` (caso de estudio con capturas reales de ordenador y móvil y botones «Entrar en la app») y su **PDF** con todos los enlaces absolutos y clicables, listo para Drive y WhatsApp.
- **Mensaje de WhatsApp** listo para el cliente: enlace, crear contraseña, instalar en móvil y ordenador, qué rellenar en Ajustes.

## Comprobación antes de dar el enlace

- [ ] Entra en móvil y ordenador con la misma cuenta y ve los mismos datos.
- [ ] Se instala con icono en Android, iPhone y ordenador.
- [ ] PDF correcto y envío por WhatsApp/correo probado en un móvil real.
- [ ] HTTPS activo y verificado con certificado válido en todas las direcciones.
- [ ] Sin datos personales del cliente en el repositorio.
- [ ] Demo y portafolio actualizados.
