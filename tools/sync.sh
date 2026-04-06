#!/bin/bash
cd ~/Bori-System
echo "⬆️ Sincronizando..."
git add .
read -p "Mensaje: " msg
git commit -m "$msg"
git push origin main
echo "✅ OK"
