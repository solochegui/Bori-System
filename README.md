# 💠 Bori-System v2.4

Sistema de monitoreo, análisis técnico y gestión de cartera de criptomonedas optimizado para **Termux**. Este repositorio contiene herramientas automatizadas para detectar oportunidades de mercado bajo la estrategia NFM (Suelo Dinámico).

## 🚀 Scripts Incluidos

* **`nfm_analyst_chegui.py`**: El motor principal. Analiza la presión de compra/venta, calcula el suelo dinámico y gestiona el valor total de la cartera en tiempo real.
* **`bori_tracker.py`**: Rastreador de movimientos específicos de activos.
* **`price_checker9che.py`**: Utilidad rápida para consulta de precios sin análisis profundo.

---

## 📊 Estrategia NFM (Precision Analyst)

El sistema utiliza un algoritmo de **Suelo Elástico** para evitar señales falsas:

1.  **Detección de Sobreventa:** Filtra activos con caídas superiores al 7% en 24h.
2.  **Suelo Dinámico:** Calcula niveles de rebote basados en el `low_24h` con un margen de seguridad del 1.5%.
3.  **Protección Anti-Crash:** Implementación de validación de datos `NoneType` para evitar cierres inesperados por fallos en la API.

---

## 🛠️ Instalación y Uso

### Prerrequisitos
Desde tu terminal de Termux, asegúrate de tener instaladas las dependencias:
```bash
pkg update && pkg upgrade
pkg install python git -y
pip install requests
