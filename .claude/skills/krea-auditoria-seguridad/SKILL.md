---
name: krea-auditoria-seguridad
description: Auditoría de seguridad de KREAVANCE (25 puntos) para apps y webs con backend (PHP + MySQL de OVH, Supabase, APIs de IA, Stripe, formularios). Usar SIEMPRE antes de publicar o comercializar una app, tras cambios grandes, y cuando Kike diga «auditoría», «seguridad», «que no me hackeen la app» o /seguridad. Obligatoria desde enero de 2027 en todas las apps que se vayan a vender.
---

# Auditoría de seguridad KREA · revisar como un atacante

Objetivo: que ninguna app de KREA llegue a un cliente filtrando datos, claves o saldo de IA.

**Regla de KREA (desde enero de 2027):** toda app que se comercialice (Gastoticket, YouManager, MiVet, KREA Clients, las de Ingenios KREA Apps y las de clientes) pasa esta auditoría **antes de abrir el cobro** y **después de cada cambio grande**. Sin los 25 puntos en OK o «no aplica», no se activa `sk_live` de Stripe.

## Cómo se hace (Claude Code)

1. **Revisión automática del código** (desde la raíz del repo de la app):
   ```bash
   python3 ~/.claude/skills/krea-auditoria-seguridad/scripts/auditar_codigo.py .
   ```
   (Si la skill está dentro del proyecto: `.claude/skills/krea-auditoria-seguridad/scripts/…`.) Saca avisos ALTO / MEDIO / INFO con archivo y línea. Son pistas: confirmar cada una leyendo el código.
2. **Revisión de la app publicada** (cabeceras, HTTPS, archivos expuestos, CORS):
   ```bash
   python3 ~/.claude/skills/krea-auditoria-seguridad/scripts/revisar_web.py https://<app>.kreavance.es
   ```
   Si la sesión no llega a la web (sesiones en la nube con red cerrada), se hace con el workflow `auditoria-seguridad.yml` de GitHub Actions (plantilla en `plantillas/`), que corre en GitHub y deja el informe en la pestaña Actions.
3. **Las 5 puertas** (abajo) y **revisión a mano** de los 25 puntos, sobre todo los que ningún script ve: permisos por usuario, precios, rutas de admin, IA.
4. **Ataque guiado**: «Atácala como un hacker: lee datos de otro usuario, busca claves, sáltate el login y gasta la IA sin cuenta». Con `curl` contra la API (sin cookie, con la cookie de otro usuario, con Origin falso) y con Playwright/DevTools mirando red y consola.
5. **Entrega**: tabla en español claro con las 5 puertas y los 25 puntos (OK / riesgo / no aplica), dónde y arreglo. Los arreglos se **proponen** a Kike y se aplican cuando dé el OK; después se publica y se le pasa el enlace.

## Las 5 puertas · comprobación rápida obligatoria (regla fija desde el 24-11-2026)

En **toda** web o app de KREAVANCE, nueva o cambiada, y en cada proyecto nuevo, antes incluso de los 25 puntos, se cierran estas 5 puertas (las más comunes en apps hechas con IA). Se comprueban **con curl contra la API**, no solo leyendo el código:

1. **Quién ve cada fila** (punto 4). PHP + MySQL: toda consulta lleva `WHERE usuario = <id de la sesión>`. Supabase (solo apps antiguas): RLS activado en todas las tablas.
2. **Claves en el navegador** (puntos 6-9). Buscar en el HTML/JS publicado `sk_`, `sk-ant-`, `AIza`, `service_role`, `sb_publishable`, tokens largos. También códigos de acceso escritos en el JS (aunque vayan en base64): solo valen para demos de presentación, nunca para proteger datos reales. Claves que ya no se usan, fuera.
3. **Rutas sin login** (puntos 3 y 16). Cada `.php` o ruta de la API, llamado sin sesión, responde 401/403. Probar también con `-H "Origin: https://<app>"` falso: **la cabecera Origin no es un login**. Las acciones que borran o cambian mucho (borrar todo, reset, importar) nunca sin sesión o sin un código guardado solo en el servidor, con bloqueo tras 5 fallos.
4. **Límite de uso** (punto 18). Todo lo que se puede llamar sin ser el dueño (formularios de contacto, reservas, enlaces públicos, IA, login) lleva límite por conexión y, si cuesta dinero o llena el correo, tope global al día. Al pasarse: 429 y la web ofrece otra salida (p. ej. abrir el correo con el mensaje preparado). Patrón KREA sin base de datos: ventana deslizante en archivos fuera de la carpeta pública con la IP resumida en hash (`limitar()` de krea-alvarovelasco `server/api/lib.php`, `contacto.php` de krea-web).
5. **Datos de otros cambiando un número** (IDOR, punto 4). Con la sesión del usuario A, pedir el id de un registro de B (en la URL o en el JSON): tiene que dar 403/404, nunca los datos.

La tabla de entrega empieza siempre por estas 5 (Sí / Falta / No aplica). Lo que falte se arregla en un PR por repo, con capturas, y se publica con el OK de Kike.

## Los 25 puntos

### Acceso
1. **Login sólido**: contraseñas de 8+ caracteres, correo confirmado, límite de intentos por IP y por correo, sesión en cookie `HttpOnly` (no en localStorage), cerrar sesión borra la sesión en el servidor.
2. **Contraseñas con hash**: `password_hash`/`password_verify` en PHP o Supabase Auth. Nunca en texto ni con md5/sha1.
3. **Rutas de admin blindadas**: el servidor comprueba el rol en cada petición (dueño del equipo, admin…). Ocultar el botón no vale.
4. **Base de datos protegida**: PHP → **toda** consulta filtra por el usuario de la sesión (`WHERE user_id = ?`); Supabase → RLS activado en todas las tablas y `get_advisors` sin avisos. Probar a pedir el id de otro usuario.
5. **Consultas parametrizadas**: siempre `prepare` + `?`. Nada de texto del usuario pegado dentro del SQL.

### Claves y secretos
6. **Claves API fuera de la app**: en el navegador solo claves públicas (Stripe `pk_`, `anon` de Supabase). `sk_`, `sk-ant-`, `service_role`, contraseñas de base de datos y FTP → solo secretos de GitHub → `api/config.php` al publicar.
7. **Variables de entorno / config fuera del repo**: `config.php`, `clave.php`, `.env` en `.gitignore` y bloqueados en `.htaccess`.
8. **Secretos en Git**: buscar en todo el historial (`git log -p --all`), no solo en la versión actual.
9. **Revocar claves**: si una clave estuvo alguna vez en el repo o a la vista, se **anula en el panel del proveedor** (Anthropic, Stripe, OVH…) y se crea otra. Borrarla del código no basta.

### Entradas del usuario
10. **Validar en el servidor**: tipos, longitudes, formatos, número máximo de elementos. La validación del formulario es solo comodidad.
11. **Protección XSS**: todo texto del usuario pasa por `esc()` antes de `innerHTML`; mejor `textContent`. Nada de `eval` ni HTML del usuario sin limpiar.
12. **Límite de archivos**: tamaño máximo, tipo comprobado en el servidor (`getimagesize`/`finfo`, no la extensión), nombre generado por el servidor, guardado fuera de la carpeta pública y servido solo a su dueño.

### Navegador y conexión
13. **HTTPS forzado**: redirección 301 de http a https en `.htaccess` y HSTS.
14. **Cabeceras de seguridad** en `.htaccess` de la raíz: `Content-Security-Policy`, `X-Frame-Options: DENY` (o `frame-ancestors`), `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy`, `Strict-Transport-Security`. Plantilla en `plantillas/htaccess-seguridad.txt`.
15. **Cookies seguras**: `Secure`, `HttpOnly`, `SameSite=Lax` (o `Strict`).
16. **CORS restringido**: solo el subdominio de la app. Ojo: `Origin`/`Referer` se falsifican con curl, **no sustituyen al login**.
17. **Protección CSRF**: cookie `SameSite` + cabecera propia obligatoria (p. ej. `X-Gastoticket: 1`) o token; solo POST para cambiar datos.

### Lógica de negocio
18. **Límite de peticiones**: login, altas, correos y **sobre todo la IA** (por usuario y por IP). Cada endpoint de IA de pago exige sesión, límite por hora y tamaño máximo de lo que se manda.
19. **Precios en el servidor**: importes y planes salen del servidor/Stripe (`lookup_key`), nunca del navegador. El webhook comprueba la firma de Stripe.
20. **Enlaces que caducan**: confirmar correo (24 h), nueva contraseña (1 h), invitaciones (días). Enlaces permanentes (p. ej. de jugadores) se pueden anular y renovar.
21. **IA solo para quien tiene derecho**: en apps de pago, la IA comprueba que la prueba o la suscripción están activas antes de gastar.

### Publicación
22. **Sin modo depuración**: sin `display_errors`, sin `console.log` de datos, errores genéricos al usuario y el detalle solo en `error_log`. Puertas de diagnóstico/importación cerradas (404) si no hay clave.
23. **Archivos expuestos**: no se publican `.git`, `.env`, `*.sql`, `*.md`, copias, `herramientas/`, `supabase/`, source maps. La publicación copia solo lo necesario.
24. **Dependencias al día**: librerías de CDN en su última versión y con `integrity` (SRI) + `crossorigin`; `npm audit` si hay `package.json`.
25. **Fuera paquetes inútiles y vigilancia**: quitar librerías, archivos y endpoints que ya no se usan (versiones antiguas, Supabase de respaldo) y registrar actividad rara (muchos fallos de login, picos de IA, cambios de admin) con aviso a Kike.

## Particularidades KREA

- Backend estándar: PHP + MySQL de OVH en `api/`, claves en secretos de GitHub, publicación por FTP con GitHub Actions. Supabase solo en apps antiguas o de respaldo (no pausar ni borrar sin Kike).
- Stripe es común a varias apps: todo lleva `metadata.app` y el webhook ignora lo de otras apps.
- Datos de clientes y de menores (YouManager): nunca en el repo; el acceso de jugadores con código largo aleatorio, revocable y con consentimiento del tutor.
- No tocar datos «PRUEBA» ni datos reales sin permiso de Kike.
