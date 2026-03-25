# 💠 Bori-System: NFM Precision Analyst v2.5

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![Platform](https://img.shields.io/badge/platform-Termux-orange.svg)](https://termux.dev)
[![Strategy](https://img.shields.io/badge/strategy-Panic%20Sell%20Detection-red.svg)](#-estrategia-de-clímax-de-ventas)

**Bori-System** es un ecosistema de trading algorítmico diseñado para ejecutarse 24/7 en **Termux**. Su motor principal, `nfm_analyst_chegui.py`, utiliza análisis de volatilidad intradía para cazar suelos reales durante pánicos de mercado.

---

## 🚀 Mejoras en la v2.5 (Professional Edition)

* **🔥 Detección de Clímax de Ventas:** Nuevo algoritmo que identifica el "Panic Sell" mediante la posición del precio en el rango de 24h.
* **🛡️ Blindaje NoneType:** Protección total contra fallos de la API de CoinGecko. El script ya no colapsa si recibe datos nulos.
* **⚡ Optimización de Latencia:** Se eliminó el uso de sparklines pesadas, reduciendo el consumo de datos y acelerando la respuesta.
* **🧹 Gestión de Almacenamiento:** Sistema de auto-limpieza de logs que mantiene el archivo `oportunidades_nfm.txt` por debajo de 1MB.

---

## 🧠 Estrategia de "Malicia" Técnica

A diferencia de otros bots que compran solo por caída porcentual, Bori-System analiza la **Posición del Rango**:



1.  **Zona de Acumulación:** Si el precio baja pero se mantiene estable, el bot sugiere `MANTENER`.
2.  **Buscando Suelo:** Si la caída es moderada, calcula un soporte dinámico un 1.5% por debajo del mínimo actual.
3.  **Clímax de Ventas:** Si la caída es >10% y el precio toca el fondo del día, se activa la alerta de `CARGAR (COMPRA)`.

---

## 🛠️ Instalación Rápida

```bash
# Instalar dependencias
pkg update && pkg upgrade
pkg install python git -y
pip install requests

# Clonar y Ejecutar
git clone [https://github.com/solochegui/Bori-System.git](https://github.com/solochegui/Bori-System.git)
cd Bori-System
python nfm_analyst_chegui.py
