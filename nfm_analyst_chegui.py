#!/usr/bin/env python3
import os
import sys
import time
import requests
from datetime import datetime

# ======================================================================
# 💠 NFM PRECISION ANALYST v2.5 - EXPERT STRATEGY (Bori-System)
# ======================================================================

# --- CARTERA REAL DE CHEGUI (NFM) ---
MI_CARTERA = {
    "bitcoin": 0.00045, "ethereum": 0.05, "solana": 1.2,
    "cardano": 150, "avalanche-2": 5, "polkadot": 10,
    "matic-network": 100, "cosmos": 8, "pepe": 5000000
}

CRYPTOS_IDS = ",".join(MI_CARTERA.keys())
API_URL = "https://api.coingecko.com/api/v3/coins/markets"
LOG_FILE = "oportunidades_nfm.txt"

def format_p(val):
    """Formateo profesional de moneda"""
    if val is None or val == 0: return "$0.00"
    return f"${val:,.2f}" if val >= 1 else f"${val:,.6f}"

def registrar_log(mensaje):
    """Gestión de logs con auto-limpieza (Punto 4)"""
    try:
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 1024 * 1024:
            with open(LOG_FILE, "w") as f: f.write(f"--- Log Reset {datetime.now()} ---\n")
        timestamp = datetime.now().strftime('%H:%M:%S')
        with open(LOG_FILE, "a") as f: f.write(f"[{timestamp}] {mensaje}\n")
    except: pass

def analizar_precision(coin):
    """Lógica Experta: Clímax de Ventas y Agotamiento (Punto 1 y 3)"""
    price = coin.get('current_price') or 0
    c24h = coin.get('price_change_percentage_24h_in_currency') or 0
    high_24h = coin.get('high_24h') or price
    low_24h = coin.get('low_24h') or price

    # --- MALICIA TÉCNICA: DETECCIÓN DE PÁNICO ---
    # Calculamos qué tan cerca estamos del mínimo del día (0.0 = fondo, 1.0 = tope)
    rango = high_24h - low_24h
    posicion_rango = (price - low_24h) / rango if rango > 0 else 0.5

    # 1. CLÍMAX DE VENTAS (Oportunidad de Oro)
    # Caída > 10% y precio pegado al mínimo diario (< 2% de distancia)
    if c24h < -10.0 and posicion_rango < 0.02:
        suelo_real = low_24h * 0.992 # Compramos un poco debajo del susto
        msg = f"🔥 CLÍMAX: CARGAR EN {format_p(suelo_real)}"
        registrar_log(f"ALERTA CRÍTICA: {coin['symbol'].upper()} en Clímax de Ventas.")
        return msg

    # 2. BUSCANDO SUELO (Caída moderada)
    if c24h < -4.0:
        suelo_espera = low_24h * 0.985
        return f"🟡 BUSCANDO SUELO -> {format_p(suelo_espera)}"

    # 3. DISTRIBUCIÓN (Venta técnica)
    if c24h > 7.0:
        return "🔴 SOBRECOMPRA (Vender/Distribuir)"

    return "⚖️ MANTENER / ACUMULAR"

def get_market_data():
    """Conexión robusta anti-microcortes (Punto 2)"""
    params = {"vs_currency": "usd", "ids": CRYPTOS_IDS, "price_change_percentage": "24h"}
    try:
        response = requests.get(API_URL, params=params, timeout=12)
        response.raise_for_status()
        return response.json()
    except: return None

def main():
    while True:
        os.system("clear")
        ahora = datetime.now().strftime('%H:%M:%S')
        print(f"--- 💠 NFM PRECISION ANALYST v2.5 | {ahora} ---")
        print("Estrategia: Clímax de Ventas + Blindaje NoneType | Repo: Bori-System")
        print("=" * 115)

        data = get_market_data()
        if data:
            total_usd = 0
            header = f"{'SYM':<6} | {'BALANCE':<12} | {'VALOR USD':<12} | {'24h%':<8} | {'PREDICCIÓN NFM'}"
            print(header)
            print("-" * 115)

            for coin in data:
                # Blindaje contra NoneType (Punto de falla v2.3 corregido)
                price = coin.get('current_price')
                if price is None: continue 
                
                sym = coin.get('symbol', '???').upper()
                c24h = coin.get('price_change_percentage_24h_in_currency') or 0
                cant = MI_CARTERA.get(coin['id'], 0)
                
                valor = cant * price
                total_usd += valor
                
                prediccion = analizar_precision(coin)
                print(f"{sym:<6} | {cant:<12.4f} | {format_p(valor):<12} | {c24h:>7.2f}% | {prediccion}")

            print("-" * 115)
            print(f"💰 CAPITAL TOTAL NFM: {format_p(total_usd)}")
        else:
            print("\n⚠️ ERROR DE RED: Reintentando conexión en 60s...")

        print("\n(Ctrl+C para salir | Logs activos en oportunidades_nfm.txt)")
        time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Sistema Bori-System cerrado correctamente.")
        sys.exit(0)
