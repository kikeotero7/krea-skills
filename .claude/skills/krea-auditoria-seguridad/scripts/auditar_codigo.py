#!/usr/bin/env python3
"""KREA · revisión automática de seguridad del código de una app (sin dependencias).

Uso:  python3 auditar_codigo.py <carpeta-del-repo>
Saca avisos ALTO / MEDIO / INFO con archivo y línea. Son pistas: confirmar cada una leyendo el código.
Sale con código 1 si hay algún ALTO (sirve para GitHub Actions).
"""
import os, re, subprocess, sys

RAIZ = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
SALTAR = {'.git', 'node_modules', 'vendor', '__pycache__', 'pdfjs', 'videoteca', 'muestras'}
TEXTO = ('.html', '.htm', '.js', '.mjs', '.ts', '.php', '.py', '.json', '.yml', '.yaml', '.env', '.txt', '.md', '.sql', '.htaccess', '.webmanifest')
avisos = []

def aviso(nivel, punto, msg, donde=''):
    avisos.append((nivel, punto, msg, donde))

SECRETOS = [
    (r'sk_live_[A-Za-z0-9]{10,}', 'Clave secreta de Stripe (live)'),
    (r'sk_test_[A-Za-z0-9]{10,}', 'Clave secreta de Stripe (test)'),
    (r'rk_(live|test)_[A-Za-z0-9]{10,}', 'Clave restringida de Stripe'),
    (r'whsec_[A-Za-z0-9]{10,}', 'Secreto de webhook de Stripe'),
    (r'sk-ant-[A-Za-z0-9_-]{20,}', 'Clave de Anthropic'),
    (r'sk-(proj-)?[A-Za-z0-9]{32,}', 'Clave de OpenAI'),
    (r'AIza[0-9A-Za-z_-]{35}', 'Clave de Google'),
    (r'eyJhbGciOi[A-Za-z0-9._-]{40,}', 'Token JWT (¿service_role de Supabase?)'),
    (r'service_role', 'Mención a service_role de Supabase'),
    (r'-----BEGIN (RSA |EC )?PRIVATE KEY-----(\\n|\s)*[A-Za-z0-9+/]{40}', 'Clave privada'),
    (r'''(db_pass|DB_PASS|password|contrasena|ftp_pass)\s*[=:>]+\s*['"][^'"\s$]{6,}['"]''', 'Contraseña escrita en el código'),
]

def archivos():
    for base, dirs, fs in os.walk(RAIZ):
        dirs[:] = [d for d in dirs if d not in SALTAR]
        for f in fs:
            r = os.path.join(base, f)
            if f.endswith(TEXTO) or f in ('.htaccess', '.gitignore', '.env'):
                yield os.path.relpath(r, RAIZ), r

def leer(r):
    try:
        with open(r, encoding='utf-8', errors='ignore') as fh:
            return fh.read()
    except OSError:
        return ''

def linea(texto, pos):
    return texto.count('\n', 0, pos) + 1

contenidos = {rel: leer(r) for rel, r in archivos()}

# 6/7 · Secretos en los archivos actuales
for rel, t in contenidos.items():
    if 'ejemplo' in rel or rel.endswith('.md'):
        continue
    for pat, nombre in SECRETOS:
        for m in re.finditer(pat, t):
            nivel = 'INFO' if nombre.startswith('Mención') else 'ALTO'
            aviso(nivel, 6, nombre, f'{rel}:{linea(t, m.start())}')

# 8 · Secretos en el historial de git
if os.path.isdir(os.path.join(RAIZ, '.git')):
    try:
        if subprocess.run(['git', '-C', RAIZ, 'rev-parse', '--is-shallow-repository'], capture_output=True, text=True).stdout.strip() == 'true':
            aviso('INFO', 8, 'Repo clonado a medias (shallow): el historial completo no se ha revisado. Repetir con un clon completo.')
        log = subprocess.run(['git', '-C', RAIZ, 'log', '-p', '--all', '--no-color'], capture_output=True, text=True, errors='ignore', timeout=300).stdout
        for pat, nombre in SECRETOS:
            if nombre.startswith('Mención') or nombre.startswith('Contraseña'):
                continue
            for m in re.finditer(r'^\+.*' + pat, log, re.M):
                aviso('ALTO', 8, f'{nombre} en el historial de git: anularla en el proveedor (punto 9)', m.group(0)[:80])
                break
    except Exception as e:  # noqa
        aviso('INFO', 8, f'No se pudo leer el historial de git: {e}')

# 7 · .gitignore
gi = contenidos.get('.gitignore', '')
for f, usa in (('config.php', any(re.search(r"require[^;]*config\.php", t) for t in contenidos.values())),
               ('.env', os.path.exists(os.path.join(RAIZ, '.env')) or any(re.search(r"['\"]\.env['\"]|dotenv", t) for t in contenidos.values()))):
    if usa and f not in gi:
        aviso('MEDIO', 7, f'{f} se usa pero no está en .gitignore')

# 13/14 · .htaccess de la raíz
ht = contenidos.get('.htaccess', '')
if not ht:
    aviso('MEDIO', 13, 'No hay .htaccess en la raíz: sin redirección a HTTPS ni cabeceras de seguridad (ver plantillas/htaccess-seguridad.txt)')
else:
    if not re.search(r'HTTPS', ht):
        aviso('MEDIO', 13, '.htaccess sin redirección a HTTPS')
    for cab in ('Strict-Transport-Security', 'Content-Security-Policy', 'X-Frame-Options|frame-ancestors', 'X-Content-Type-Options', 'Referrer-Policy'):
        if not re.search(cab, ht):
            aviso('MEDIO', 14, f'.htaccess sin la cabecera {cab.split("|")[0]}')

# 24 · Librerías de CDN sin integrity
for rel, t in contenidos.items():
    if not rel.endswith(('.html', '.htm')):
        continue
    for m in re.finditer(r'<script[^>]+src="(https?://[^"]+)"[^>]*>', t):
        if 'integrity=' not in m.group(0):
            aviso('MEDIO', 24, f'Librería externa sin integrity (SRI): {m.group(1)}', f'{rel}:{linea(t, m.start())}')
        v = re.search(r'jspdf/(\d+)\.(\d+)', m.group(1))
        if v and (int(v.group(1)), int(v.group(2))) < (3, 0):
            aviso('MEDIO', 24, f'jsPDF {v.group(1)}.{v.group(2)} tiene fallos conocidos: subir a la 3.x', f'{rel}:{linea(t, m.start())}')

# 11 · XSS
sin_esc = []
for rel, t in contenidos.items():
    if not rel.endswith(('.html', '.js')):
        continue
    for m in re.finditer(r'\beval\s*\(|new Function\s*\(|document\.write\s*\(', t):
        aviso('MEDIO', 11, 'eval / new Function / document.write', f'{rel}:{linea(t, m.start())}')
    n = len(re.findall(r'innerHTML\s*[+]?=', t))
    if n and not re.search(r'(const|function|let|var)\s+(esc|escapar|escHtml|h)\b', t):
        aviso('MEDIO', 11, f'{n} innerHTML y ninguna función esc() para escapar texto', rel)
    elif n:
        sin_esc.append((rel, n))

if sin_esc:
    total = sum(n for _, n in sin_esc)
    aviso('INFO', 11, f'{total} innerHTML en {len(sin_esc)} archivos (con esc() disponible): revisar que el texto del usuario pasa por esc()', ', '.join(r for r, _ in sin_esc[:4]) + (' …' if len(sin_esc) > 4 else ''))

# PHP: SQL, depuración, endpoints, CORS, cookies, archivos
for rel, t in contenidos.items():
    if not rel.endswith('.php'):
        continue
    for m in re.finditer(r'''(query|exec|prepare)\s*\(\s*["'][^"']*(SELECT|INSERT|UPDATE|DELETE)[^"']*["']\s*\.\s*\$''', t, re.I):
        aviso('ALTO', 5, 'SQL construido pegando una variable: usar prepare con ?', f'{rel}:{linea(t, m.start())}')
    for m in re.finditer(r'''\$_(GET|POST|REQUEST|COOKIE)\[[^\]]+\][^;]{0,40}(SELECT|INSERT|UPDATE|DELETE)''', t, re.I):
        aviso('ALTO', 5, 'Dato del usuario dentro de SQL', f'{rel}:{linea(t, m.start())}')
    for m in re.finditer(r'display_errors[\'"]?\s*,\s*[\'"]?(1|on|true)|error_reporting\s*\(\s*E_ALL\s*\)|var_dump\s*\(|print_r\s*\(', t, re.I):
        aviso('MEDIO', 22, 'Restos de depuración (display_errors / var_dump / print_r)', f'{rel}:{linea(t, m.start())}')
    if re.search(r'Access-Control-Allow-Origin:\s*\*', t):
        aviso('ALTO', 16, 'CORS abierto a cualquier web (*)', rel)
    if re.search(r'setcookie\(', t) and not re.search(r"httponly'?\"?\s*=>\s*true", t, re.I):
        aviso('MEDIO', 15, 'setcookie sin httponly', rel)
    if re.search(r'move_uploaded_file|\$_FILES', t) and not re.search(r'getimagesize|finfo_|mime_content_type', t):
        aviso('MEDIO', 12, 'Subida de archivos sin comprobar el tipo real', rel)
    # Endpoints que llaman a una IA sin comprobar sesión
    llama_ia = re.search(r'api\.anthropic\.com|generativelanguage\.googleapis|api\.openai\.com', t)
    if llama_ia:
        incluido = [o for o, ot in contenidos.items() if o.endswith('.php') and o != rel and re.search(r"require[^;]*" + re.escape(os.path.basename(rel)), ot)]
        protegido = re.search(r'exigir_usuario|usuario_actual|auth\.uid|getUser|session_start', t) or incluido
        if not protegido:
            aviso('ALTO', 18, 'Llama a una IA de pago sin comprobar la sesión: cualquiera con curl puede gastar el saldo (Origin/Referer se falsifican)', rel)
        elif not re.search(r'limitar\(|rate|intentos', t) and not incluido:
            aviso('MEDIO', 18, 'Llama a una IA sin límite de peticiones', rel)
    # Puertas de importación / diagnóstico
    if re.search(r'importar|diagnostico', rel + t[:400], re.I) and not re.search(r'hash_equals|http_response_code\(404\)', t):
        aviso('MEDIO', 22, 'Puerta de importación o diagnóstico sin clave', rel)

# api/.htaccess
for rel, t in contenidos.items():
    if rel.endswith('api/.htaccess') and 'sql' not in t:
        aviso('MEDIO', 23, 'api/.htaccess no bloquea .sql/.md/.json', rel)
if any(r.startswith('api/') and r.endswith('.php') for r in contenidos) and 'api/.htaccess' not in contenidos:
    aviso('MEDIO', 23, 'Hay api/ en PHP pero no api/.htaccess que bloquee archivos internos')

# 23 · Qué se publica
for rel, t in contenidos.items():
    if rel.startswith('.github/workflows/') and re.search(r'ftp|FTP', t):
        if re.search(r'local-dir:\s*\./?\s*$', t, re.M):
            aviso('ALTO', 23, 'La publicación sube TODO el repo (local-dir: ./): se publican .md, herramientas, supabase…', rel)
        if 'config.ejemplo' not in t and 'config.php' in t:
            aviso('INFO', 23, 'Comprobar que no se publica config.ejemplo.php ni copias', rel)

# 24 · npm
if 'package.json' in contenidos:
    aviso('INFO', 24, 'Hay package.json: ejecutar «npm audit» y quitar dependencias que no se usan')

# 25 · Restos
for d in ('supabase', 'traspaso-fabrica', 'herramientas'):
    if os.path.isdir(os.path.join(RAIZ, d)):
        aviso('INFO', 25, f'Carpeta {d}/ en el repo: comprobar que NO se publica en la web')

orden = {'ALTO': 0, 'MEDIO': 1, 'INFO': 2}
avisos.sort(key=lambda a: (orden[a[0]], a[1]))
print(f'\nAuditoría de seguridad KREA · {os.path.basename(RAIZ)}\n' + '=' * 60)
if not avisos:
    print('Sin avisos automáticos. Falta la revisión a mano de los 25 puntos.')
for nivel, punto, msg, donde in avisos:
    print(f'[{nivel:5}] punto {punto:2} · {msg}' + (f'\n         → {donde}' if donde else ''))
altos = sum(1 for a in avisos if a[0] == 'ALTO')
print('=' * 60 + f'\n{altos} ALTO · {sum(1 for a in avisos if a[0] == "MEDIO")} MEDIO · {sum(1 for a in avisos if a[0] == "INFO")} INFO')
print('Recuerda: los puntos 3, 4, 19, 20 y 21 (permisos, precios, enlaces, IA de pago) solo se ven leyendo el código.')
sys.exit(1 if altos else 0)
