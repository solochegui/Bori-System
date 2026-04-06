# 🌀 Bori-System: Módulo AI-Chat

Este módulo integra la potencia de **Gemini 1.5/2.0/2.5 Flash** directamente en la terminal de Termux para el desarrollo de la red **Solana** y el ecosistema **BoriCoin**.

## 🛠️ Instalación Rápida
Para configurar el entorno de IA en un nuevo dispositivo, navega a esta carpeta y ejecuta el instalador:

\`\`\`bash
cd modules/aichat
./install.sh
\`\`\`

## 🔐 Seguridad (Bori-Shield)
Este módulo está protegido por un sistema de **Zero-Leak**. 
- Las llaves API se almacenan localmente en \`~/.config/aichat/config.yaml\`.
- El archivo \`.gitignore\` interno bloquea cualquier intento de subir credenciales reales al repositorio público.
- Se incluye un \`config/config.example.yaml\` como referencia de estructura.

## 🚀 Comandos Útiles en REPL
Una vez dentro de \`aichat\`, puedes usar estos comandos avanzados:

| Comando | Acción |
| :--- | :--- |
| \`.file <ruta>\` | Carga un script de Rust/Python para análisis. |
| \`.role\` | Cambia entre perfiles (ej. Programador Rust, Analista Cripto). |
| \`.session\` | Guarda el contexto de la conversación actual. |
| \`.edit config\` | Modifica el modelo o la API Key rápidamente. |

## 🦀 Especialización en Solana
Este asistente está optimizado para trabajar con:
- **Rust & Anchor Framework**
- **Optimización de Compute Units (CU)**
- **Análisis de Smart Contracts** en la red Solana.

---
**Desarrollado por:** Chegui (Bori-System)  
**Entorno:** Termux (Android)
