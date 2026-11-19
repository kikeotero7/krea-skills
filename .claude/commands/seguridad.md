---
description: Auditoría de seguridad KREA (25 puntos) de la app de este repositorio
---

Aplica la skill `krea-auditoria-seguridad` a este proyecto. $ARGUMENTS

1. Lee el CLAUDE.md del repo para saber la dirección publicada, el backend y cómo se publica.
2. Ejecuta `scripts/auditar_codigo.py .` de la skill (en `~/.claude/skills/` o en `.claude/skills/` del proyecto).
3. Ejecuta `scripts/revisar_web.py <dirección publicada>`. Si no hay red hasta la web, lanza el workflow «Auditoría de seguridad KREA» (`gh workflow run auditoria-seguridad.yml`) o di a Kike que lo lance en GitHub → Actions; si el repo no lo tiene, cópialo de `plantillas/auditoria-seguridad.yml`.
4. Revisa a mano los 25 puntos, sobre todo permisos por usuario, rutas de admin, precios, enlaces que caducan e IA de pago, y haz el ataque guiado con curl.
5. Entrega la tabla de 25 puntos (OK / riesgo / no aplica) en español claro, sin tecnicismos, con los arreglos propuestos por orden de gravedad. No cambies nada hasta que Kike dé el OK; después arregla, publica y pásale el enlace.
