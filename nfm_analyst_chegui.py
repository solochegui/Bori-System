#!/usr/bin/env python3
import os
import sys
import time
import requests
from datetime import datetime

# ======================================================================
# 💠 NFM PRECISION ANALYST v2.4 - Anti-Crash Edition
# ======================================================================

MI_CARTERA = {
    "bitcoin": 0.00045, "ethereum": 0.05, "solana": 1.2,
    "cardano": 150, "avalanche-2": 5, "polkadot": 10,
    "matic-network": 100, "cosmos": 8, "pepe": 5000000
}

CRYPTOS_IDS = ",".join(MI_CARTERA.keys())
API_URL = "https://api.coingecko.com/api/v3/coins/markets"
LOG_FILE = "oportunidades_nfm.txt"

def format_p(val):
    if val is None: return "$0.00"
    return f"${val:,.2f}" if val >= 1 else f"${val:,.6f}"

def registrar_log(mensaje):
    try:
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 1024 * 1024:
            with open(LOG_FILE, "w") as f: f.write(f"--- Log Reset {datetime.now()} ---\n")
        with open(LOG_FILE, "a") as f: f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {mensaje}\n")
    except: pass

def analizar_precision(coin):
    price = coin.get('current_price') or 0
    c24h = coin.get('price_change_percentage_24h_in_currency') or 0
    low_24h = coin.get('low_24h') or price
    
    probable_rebound = low_24h * 0.985 
    if probable_rebound < (price * 0.5): probable_rebound = price * 0.95

    if c24h > 6.0: return "🔴 DISTRIBUIR (VENTA)"
    if c24h < -7.0: return f"🟢 CARGAR (COMPRA) -> {format_p(probable_rebound)}"
    if c24h < -1.5: return f"🟡 ESPERAR -> {format_p(probable_rebound)}"
    return "⚖️ MANTENER / RANGO"

def get_market_data():
    params = {"vs_currency": "usd", "ids": CRYPTOS_IDS, "price_change_percentage": "24h"}
    try:
        response = requests.get(API_URL, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except: return None

def main():
    while True:
        os.system("clear")
        print(f"--- 💠 NFM PRECISION ANALYST v2.4 | {datetime.now().strftime('%H:%M:%S')} ---")
        print("Repo: Bori-System | Estado: Protegido contra NoneType")
        print("=" * 110)

        data = get_market_data()
        if data:
            total_usd = 0
            print(f"{'SYM':<6} | {'BALANCE':<12} | {'VALOR USD':<12} | {'24h%':<8} | {'PREDICCIÓN NFM'}")
            print("-" * 110)

            for coin in data:
                # SOLUCIÓN AL ERROR: Usamos .get() con un valor por defecto de 0
                price = coin.get('current_price')
                if price is None: price = 0 
                
                sym = coin.get('symbol', '???').upper()
                c24h = coin.get('price_change_percentage_24h_in_currency') or 0
                cant = MI_CARTERA.get(coin['id'], 0)
                
                # Ahora esta multiplicación es segura
                valor = cant * price
                total_usd += valor
                
                prediccion = analizar_precision(coin)
                print(f"{sym:<6} | {cant:<12.4f} | {format_p(valor):<12} | {c24h:>7.2f}% | {prediccion}")

            print("-" * 110)
            print(f"💰 CAPITAL TOTAL NFM: {format_p(total_usd)}")
        else:
            print("\n⚠️ ERROR: Datos no recibidos. Reintentando...")

        time.sleep(60)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: sys.exit(0)
