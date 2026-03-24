#!/usr/bin/env python3
import os
import sys
import time
import requests
from datetime import datetime

# ======================================================================
# 💠 NFM PRECISION ANALYST v2.3 - Sincronizado con Bori-System
# ======================================================================

# --- CARTERA REAL DE CHEGUI (NFM) ---
MI_CARTERA = {
    "bitcoin": 0.00045,
    "ethereum": 0.05,
    "solana": 1.2,
    "cardano": 150,
    "avalanche-2": 5,
    "polkadot": 10,
    "matic-network": 100,
    "cosmos": 8,
    "pepe": 5000000
}

CRYPTOS_IDS = ",".join(MI_CARTERA.keys())
API_URL = "https://api.coingecko.com/api/v3/coins/markets"
LOG_FILE = "oportunidades_nfm.txt"

def format_p(val):
    """Formateo inteligente de precios"""
    if val is None: return "$0.00"
    if val >= 1:
        return f"${val:,.2f}"
    return f"${val:,.6f}"

def registrar_log(mensaje):
    """Manejo eficiente de logs: Evita saturar el almacenamiento de Termux"""
    try:
        # Si el archivo supera 1MB, lo reiniciamos (mantenimiento preventivo)
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 1024 * 1024:
            with open(LOG_FILE, "w") as f:
                f.write(f"--- Log Reiniciado por Tamaño [{datetime.now()}] ---\n")
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {mensaje}\n")
    except Exception:
        pass

def analizar_precision(coin):
    """Lógica NFM Senior: Suelo Dinámico Realista (Punto 1 y 3)"""
    price = coin.get('current_price', 0)
    c24h = coin.get('price_change_percentage_24h_in_currency', 0) or 0
    low_24h = coin.get('low_24h') or price

    # 1. CÁLCULO DE SUELO DINÁMICO (Margen del 1.5% bajo el mínimo diario)
    # Esto evita el error de $1.79 al basarse en datos recientes de 24h
    probable_rebound = low_24h * 0.985 

    # 2. FILTRO DE SEGURIDAD (Validación de anomalías)
    # Si la predicción es absurda (ej. 50% menos que el precio actual), se ajusta al 5%
    if probable_rebound < (price * 0.5):
        probable_rebound = price * 0.95

    # 3. GENERAR PREDICCIÓN BASADA EN PRESIÓN
    if c24h > 6.0:
        msg = "🔴 DISTRIBUIR (VENTA)"
    elif c24h < -7.0:
        msg = f"🟢 CARGAR (COMPRA) -> {format_p(probable_rebound)}"
        registrar_log(f"OPORTUNIDAD DE COMPRA: {coin['symbol'].upper()} en {format_p(price)}")
    elif c24h < -1.5:
        msg = f"🟡 ESPERAR -> {format_p(probable_rebound)}"
    else:
        msg = "⚖️ MANTENER / RANGO"

    return msg

def get_market_data():
    """Obtención de datos con manejo de errores de red (Punto 2)"""
    params = {
        "vs_currency": "usd",
        "ids": CRYPTOS_IDS,
        "sparkline": "false", # Desactivado para mayor velocidad y menos errores
        "price_change_percentage": "24h"
    }
    try:
        # Timeout de 15s para evitar que el script se congele en micro-cortes
        response = requests.get(API_URL, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, Exception) as e:
        registrar_log(f"Fallo de conexión: {e}")
        return None

def main():
    while True:
        os.system("clear")
        ahora = datetime.now().strftime('%H:%M:%S')
        print(f"--- 💠 NFM PRECISION ANALYST v2.3 | {ahora} ---")
        print("Repo: Bori-System | Estado: Monitoreando Red...")
        print("=" * 110)

        data = get_market_data()

        if data:
            total_usd = 0
            print(f"{'SYM':<6} | {'BALANCE':<12} | {'VALOR USD':<12} | {'24h%':<8} | {'PREDICCIÓN NFM'}")
            print("-" * 110)

            for coin in data:
                price = coin.get('current_price', 0)
                sym = coin.get('symbol', '???').upper()
                c24h = coin.get('price_change_percentage_24h_in_currency', 0) or 0
                
                # Gestión de Cartera
                cant = MI_CARTERA.get(coin['id'], 0)
                valor = cant * price
                total_usd += valor
                
                # Análisis de Precisión
                prediccion = analizar_precision(coin)

                print(f"{sym:<6} | {cant:<12.4f} | {format_p(valor):<12} | {c24h:>7.2f}% | {prediccion}")

            print("-" * 110)
            print(f"💰 CAPITAL TOTAL NFM: {format_p(total_usd)}")
        else:
            print("\n⚠️  ERROR DE CONEXIÓN: Reintentando en 60 segundos...")
            print("   (Verifica tus datos móviles o Wi-Fi en Termux)")

        print("\n(Actualizando cada 60s... Ctrl+C para salir)")
        time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Script detenido por el usuario. Sincronizando logs...")
        sys.exit(0)
