#!/bin/bash

# Colores para la terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🌀 Bori-System: Configurando módulo aichat...${NC}"

# 1. Crear estructura interna
mkdir -p config scripts backups

# 2. Verificar dependencias
if ! command -v aichat &> /dev/null; then
    echo -e "${BLUE}📦 Instalando binario de aichat...${NC}"
    pkg install aichat -y
else
    echo -e "${GREEN}✅ aichat ya está instalado.${NC}"
fi

# 3. Crear el Escudo de Seguridad (.gitignore local)
# Esto evita que tus llaves API se suban al GitHub de Bitrex
echo "config.yaml" > .gitignore
echo "*.key" >> .gitignore
echo -e "${GREEN}🛡️ Escudo de seguridad activado (gitignore).${NC}"

# 4. Vincular configuración actual si existe
if [ -f ~/.config/aichat/config.yaml ]; then
    cp ~/.config/aichat/config.yaml ./config/config.example.yaml
    echo -e "${BLUE}📝 Se creó una plantilla basada en tu config actual.${NC}"
fi

echo -e "${GREEN}🚀 Módulo aichat listo en ~/Bori-System/modules/aichat${NC}"
