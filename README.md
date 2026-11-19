# KREA Skills

Skills, comandos y códigos de prompting de KREAVANCE para Claude Code.
Copia la carpeta `.claude/` en cualquier proyecto para tenerlos disponibles.

## Skills

- `krea-apps`: estándar y forma de trabajar para apps, webs y portafolios de clientes (móvil y ordenador, datos sincronizados en la nube, PDF, envío por WhatsApp, demo, portafolio, © de KREA al pie y blindaje: repo privado, publicación en OVH y protección anticopia).
- `codigos-secretos`: códigos de prompting.
- `krea-auditoria-seguridad`: auditoría de seguridad de 25 puntos (comando `/seguridad`), con revisión automática del código (`scripts/auditar_codigo.py`), de la app publicada (`scripts/revisar_web.py`), bloque `.htaccess` de seguridad y workflow de GitHub Actions (`plantillas/`). **Obligatoria desde enero de 2027 en toda app que se comercialice, antes de activar el cobro.**

## Instalar en el ordenador (todos los proyectos)

En la carpeta de `krea-skills`: `powershell -ExecutionPolicy Bypass -File .\instalar.ps1` (Windows) o `bash instalar.sh` (Mac/Linux). Copia las skills y comandos a tu usuario de Claude Code, así sirven en cualquier proyecto sin copiar nada. Para actualizar: `git pull` y volver a ejecutarlo.
