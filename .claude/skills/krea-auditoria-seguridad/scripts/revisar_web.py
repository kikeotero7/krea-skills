#!/usr/bin/env python3
"""KREA · revisión de seguridad de una app ya publicada (sin dependencias).

Uso:  python3 revisar_web.py https://<app>.kreadigitalstudio.es [ruta-api]
      ruta-api por defecto: api/  (para probar CORS y respuestas de error)
Comprueba HTTPS, cabeceras, cookies, archivos expuestos y CORS. Sale con 1 si hay algún ALTO.
"""
import ssl, sys, urllib.request, urllib.error
from urllib.parse import urljoin, urlparse

if len(sys.argv) < 2:
    sys.exit(__doc__)
BASE = sys.argv[1].rstrip('/') + '/'
API = urljoin(BASE, sys.argv[2] if len(sys.argv) > 2 else 'api/')
host = urlparse(BASE).hostname
avisos = []
def aviso(n, p, m): avisos.append((n, p, m))

class SinRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
abrir = urllib.request.build_opener(SinRedir, urllib.request.HTTPSHandler(context=ssl.create_default_context()))

def pedir(url, metodo='GET', cab=None, datos=None):
    req = urllib.request.Request(url, method=metodo, headers={'User-Agent': 'KREA-auditoria/1.0', **(cab or {})}, data=datos)
    try:
        r = abrir.open(req, timeout=20); return r.status, r.headers, r.read(4000)
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read(4000) if e.fp else b''
    except Exception as e:
        return None, {}, str(e).encode()

# 13 · HTTPS
st, h, _ = pedir('http://' + host + '/')
if st is None: aviso('INFO', 13, 'No se pudo probar http://')
elif st not in (301, 302, 307, 308) or not str(h.get('Location', '')).startswith('https://'):
    aviso('MEDIO', 13, f'http:// no redirige a https:// (responde {st})')

st, h, cuerpo = pedir(BASE)
if st is None:
    sys.exit(f'No se puede abrir {BASE}: {cuerpo.decode(errors="ignore")}')
print(f'{BASE} → {st}')

# 14 · Cabeceras
CABS = {'Strict-Transport-Security': 'MEDIO', 'Content-Security-Policy': 'MEDIO', 'X-Content-Type-Options': 'MEDIO',
        'Referrer-Policy': 'INFO', 'Permissions-Policy': 'INFO'}
for c, n in CABS.items():
    if not h.get(c): aviso(n, 14, f'Falta la cabecera {c}')
csp = h.get('Content-Security-Policy', '') or ''
if not h.get('X-Frame-Options') and 'frame-ancestors' not in csp:
    aviso('MEDIO', 14, 'Se puede meter la app dentro de otra web (falta X-Frame-Options o frame-ancestors)')
if h.get('Server') and any(ch.isdigit() for ch in h.get('Server', '')):
    aviso('INFO', 22, f'El servidor dice su versión: {h.get("Server")}')
if h.get('X-Powered-By'):
    aviso('INFO', 22, f'X-Powered-By enseña la tecnología: {h.get("X-Powered-By")}')

# 15 · Cookies de la API
st, ha, cuerpo = pedir(API + '?accion=sesion', 'POST', {'Content-Type': 'application/json'}, b'{}')
for ck in (ha.get_all('Set-Cookie') or []) if hasattr(ha, 'get_all') else []:
    low = ck.lower()
    for attr in ('secure', 'httponly', 'samesite'):
        if attr not in low: aviso('MEDIO', 15, f'Cookie sin {attr}: {ck.split("=")[0]}')

# 16 · CORS
st, hc, _ = pedir(API, 'OPTIONS', {'Origin': 'https://web-atacante.example', 'Access-Control-Request-Method': 'POST'})
acao = (hc.get('Access-Control-Allow-Origin') if hc else '') or ''
if acao == '*' or 'web-atacante' in acao:
    aviso('ALTO', 16, f'CORS acepta cualquier web ({acao})')

# 22 · Errores con detalles
st, he, cuerpo = pedir(API + '?accion=__prueba__', 'POST', {'Content-Type': 'application/json'}, b'{no es json')
txt = cuerpo.decode(errors='ignore')
if any(s in txt for s in ('Fatal error', 'Stack trace', 'Warning:', 'Notice:', 'PDOException', '/home/', 'on line')):
    aviso('ALTO', 22, 'La API enseña errores internos (rutas, líneas o excepciones)')

# 23 · Archivos que no deberían verse
RUTAS = ['.git/HEAD', '.git/config', '.env', '.htaccess', 'api/config.php', 'api/config.ejemplo.php', 'api/clave.php',
         'api/esquema.sql', 'README.md', 'CLAUDE.md', 'MIGRACION-OVH.md', 'composer.json', 'package.json',
         'herramientas/', 'supabase/', 'backup.zip', 'copia.zip', 'index.html.bak', 'phpinfo.php', 'info.php',
         '.github/workflows/', 'api/importar.html']
for r in RUTAS:
    st, _, c = pedir(urljoin(BASE, r))
    t = c.decode(errors='ignore')
    if st == 200 and t.strip():
        expuesto = not (r.endswith('.php') and not t.strip())  # un .php que no devuelve nada no enseña su código
        if r == 'api/config.php' and '<?php' not in t: expuesto = False
        if expuesto:
            n = 'ALTO' if any(k in r for k in ('.git', '.env', 'config', 'clave', '.sql', 'backup', 'copia', 'phpinfo', 'info.php', 'workflows')) else 'MEDIO'
            aviso(n, 23, f'Se puede abrir desde fuera: {r}')

# 24 · Source maps
if b'sourceMappingURL' in cuerpo:
    aviso('INFO', 23, 'La página enlaza source maps')

orden = {'ALTO': 0, 'MEDIO': 1, 'INFO': 2}
avisos.sort(key=lambda a: (orden[a[0]], a[1]))
print('=' * 60)
if not avisos: print('Sin avisos en la web publicada.')
for n, p, m in avisos: print(f'[{n:5}] punto {p:2} · {m}')
altos = sum(1 for a in avisos if a[0] == 'ALTO')
print('=' * 60 + f'\n{altos} ALTO · {sum(1 for a in avisos if a[0]=="MEDIO")} MEDIO · {sum(1 for a in avisos if a[0]=="INFO")} INFO')
sys.exit(1 if altos else 0)
