#!/bin/bash
# Bori-System: Terminal Dashboard v1.0
clear
echo -e "\e[1;34m==========================================\e[0m"
echo -e "\e[1;36m   🌀 BORI-SYSTEM: DASHBOARD OPERATIVO 🌀  \e[0m"
echo -e "\e[1;34m==========================================\e[0m"

# 1. Información de Sistema
echo -e "\e[1;33m[SISTEMA]\e[0m"
echo "📍 Ubicación: Trujillo Alto, PR"
echo "📅 Fecha: $(date)"
echo "💾 Espacio Libre: $(df -h /data | awk 'NR==2 {print $4}')"

# 2. Estado de GitHub
echo -e "\n\e[1;33m[ESTADO GITHUB]\e[0m"
cd ~/Bori-System
IF_CHANGES=$(git status --porcelain)
if [ -z "$IF_CHANGES" ]; then
    echo "✅ Repositorio Sincronizado"
else
    echo "⚠️ Tienes cambios pendientes por subir (Push)"
fi

# 3. Módulos Activos
echo -e "\n\e[1;33m[MÓDULOS CRÍTICOS]\e[0m"
[ -f "~/llama.cpp/build/model.gguf" ] && echo "🤖 IA Local: LISTA" || echo "❌ IA Local: MODELO NO ENCONTRADO"
[ -f "analizador.py" ] && echo "📈 Analizador: PRESENTE" || echo "❌ Analizador: FALTANTE"

echo -e "\e[1;34m==========================================\e[0m"
echo -e "Escribe \e[1;32mborichat\e[0m para hablar con el Ingeniero."
