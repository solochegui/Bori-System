#!/usr/bin/env python3
import os, sys, time, requests
from datetime import datetime

# --- CARTERA REAL DE CHEGUI (NFM) ---
# He verificado los IDs exactos para que la API no falle
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

def format_p(val):
    if val is None: return "$0.00"
    return f"${val:,.2f}" if val >= 1 else f"${val:,.6f}"

def analizar_precision(coin):
    """Lógica NFM: Predicción de Presión y Suelo Dinámico"""
    price = coin.get('current_price')
    if price is None or price == 0: return "⚖️ ESPERANDO DATOS"
    
    c24h = coin.get('price_change_percentage_24h_in_currency') or 0
    c7d = coin.get('price_change_percentage_7d_in_currency') or 0
    high_24h = coin.get('high_24h') or price
    low_24h = coin.get('low_24h') or price
    spark = coin.get('sparkline_in_7d', {}).get('price', [])

    # 1. INDICADOR DE SOBREVENTA (RSI Simulado)
    is_oversold = (c24h < -5.0) and (c7d < -15.0)

    # 2. PRECIO SUELO DINÁMICO (-0.5% del mínimo semanal)
    min_spark = min(p for p in spark if p is not None) if spark else price
    probable_rebound = min_spark * 0.995

    # 3. FILTRO DE VOLATILIDAD (ATR > 8%)
    vol_pct = ((high_24h - low_24h) / price) * 100
    is_high_vol = vol_pct > 8.0

    # 4. GENERAR PREDICCIÓN
    if c24h > 5.0:
        msg = "🔴 DISTRIBUIR (VENTA)"
    elif is_oversold and (price <= probable_rebound * 1.01):
        msg = "🟢 CARGAR (COMPRA)"
    elif c24h < -1.0:
        msg = f"🟡 ESPERAR -> {format_p(probable_rebound)}"
    else:
        msg = "⚖️ MANTENER / RANGO"

    if is_high_vol:
        msg += " | ⚠️ VOLATILIDAD"
    
    return msg

def main():
    while True:
        os.system("clear")
        ahora = datetime.now().strftime('%H:%M:%S')
        print(f"--- 💠 NFM PRECISION ANALYST | {ahora} ---")
        print("Estrategia: Sobreventa + Suelo Dinámico + Gestión de Cartera")
        print("=" * 110)

        try:
            params = {
                "vs_currency": "usd",
                "ids": CRYPTOS_IDS,
                "sparkline": "true",
                "price_change_percentage": "24h,7d"
            }
            data = requests.get(API_URL, params=params, timeout=10).json()

            total_usd = 0
            print(f"{'SYM':<6} | {'BALANCE':<12} | {'VALOR USD':<12} | {'24h%':<8} | {'PREDICCIÓN NFM'}")
            print("-" * 110)

            for coin in data:
                sym = coin['symbol'].upper()
                price = coin['current_price']
                c24h = coin['price_change_percentage_24h_in_currency'] or 0
                
                # Cálculo de Cartera
                cant = MI_CARTERA.get(coin['id'], 0)
                valor = cant * price
                total_usd += valor

                # Obtener Predicción
                prediccion = analizar_precision(coin)

                print(f"{sym:<6} | {cant:<12.4f} | {format_p(valor):<12} | {c24h:>7.2f}% | {prediccion}")

            print("-" * 110)
            print(f"💰 CAPITAL TOTAL NFM: {format_p(total_usd)}")

        except Exception as e:
            print(f"⚠️ Nota: Actualizando... ({e})")

        print("\n(Actualizando cada 60s... Ctrl+C para salir)")
        time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
