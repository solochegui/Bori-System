#!/bin/bash
# Ejecutor oficial de IA para Bori-System
~/llama.cpp/build/bin/llama-cli \
  -m ~/llama.cpp/build/model.gguf \
  -p "Eres la IA oficial de Bori-System. Eres experto en BoriCoin (red Solana), Non Fungible Metaverse y trading en Puerto Rico. Ayuda al usuario con estrategias de inversión y código en Termux. Responde siempre en español." \
  -cnv \
  --color on \
  --temp 0.6 \
  --n-predict 512
