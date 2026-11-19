#!/usr/bin/env bash
# KREAVANCE · instala las skills y comandos de krea-skills para todos los proyectos de Claude Code (Mac/Linux o sesiones en la nube).
# Uso: bash instalar.sh      (para actualizar: git pull y volver a ejecutarlo)
set -e
cd "$(dirname "$0")"
mkdir -p ~/.claude/skills ~/.claude/commands
cp -R .claude/skills/. ~/.claude/skills/
cp .claude/commands/*.md ~/.claude/commands/
echo "Listo: skills y comandos de KREA en ~/.claude. Prueba /seguridad en cualquier proyecto."
