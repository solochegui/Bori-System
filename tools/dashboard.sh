#!/bin/bash
echo -e "\e[1;34m--- BORI-DASH ---"
echo -e "\e[1;33mSISTEMA:\e[0m $(date +%H:%M) | PR | Free: $(df -h /data | awk 'NR==2 {print $4}')"
cd ~/Bori-System && git status -s || echo "❌ No Git"
[ -f ~/llama.cpp/model.gguf ] || [ -f ~/llama.cpp/build/model.gguf ] && echo "✅ IA: OK" || echo "❌ IA: OFF"
echo -e "\e[1;34m-----------------\e[0m"
