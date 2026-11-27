# KREAVANCE · Skills y códigos

Herramientas de trabajo de KREA (no pertenecen a ningún cliente).

## Códigos secretos

Si un mensaje empieza o contiene un código de prompting (L99, ULTRATHINK, HARDMODE, PERSONA, Anti-slop, Mindmap…), aplica la skill `codigos-secretos` (`.claude/skills/codigos-secretos/`). Los códigos con barra (`/ghost`, `/redteam`, `/autoprompt`, `/infografia`…) son comandos en `.claude/commands/`. Guía rápida: `.claude/CODIGOS.md`.

## Seguridad (obligatoria desde enero de 2027)

Toda app que se vaya a comercializar pasa la skill `krea-auditoria-seguridad` (comando `/seguridad`) antes de activar el cobro (`sk_live`) y después de cada cambio grande. Los arreglos se proponen a Kike y se aplican con su OK.

Las **5 puertas** (quién ve cada fila, claves en el navegador, rutas sin login, límite de uso y datos de otros cambiando un número) se comprueban en **todos** los proyectos, nuevos y existentes, en cada cambio; están al principio de la skill `krea-auditoria-seguridad` (regla fija de Kike, 24-11-2026).

## Webs y páginas nuevas: Hallmark

Para diseñar webs, landings o páginas nuevas se usa la skill `hallmark` (`.claude/skills/hallmark/`, de nutlope/hallmark, licencia MIT, añadida el 28-11-2026 a petición de Kike): propone direcciones de diseño distintas, revisa la página en 8 tamaños de pantalla con `sloplint` y hace una revisión final como un cliente. Se aplica junto a `krea-apps` y `krea-legal-apps`. Si el proyecto ya tiene identidad (la de KREAVANCE o la del cliente), esa identidad manda: se le pasa como `DESIGN.md` o `.hallmark/brand-spec.md`.
