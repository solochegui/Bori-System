#!/bin/bash
echo "🌀 Bori-System: Iniciando Integración de Inteligencia Artificial..."

# 1. Dependencias
pkg update && pkg upgrade -y
pkg install clang cmake git make python wget -y

# 2. Compilación de Llama.cpp (Motor de Bori-AI)
cd ~
if [ ! -d "llama.cpp" ]; then
    git clone https://github.com/ggerganov/llama.cpp
fi
cd llama.cpp && mkdir -p build && cd build
cmake .. && cmake --build . --config Release -j 4

# 3. Descarga del Cerebro (Modelo Qwen 0.5B)
wget --continue https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf -O model.gguf

echo "✅ Bori-AI integrada con éxito en Bori-System."
