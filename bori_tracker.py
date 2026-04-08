import pandas as pd
import numpy as np
import time
import os
import matplotlib.pyplot as plt
import sys
import random 
import requests 
import json
import warnings
from datetime import datetime

# Suprimir advertencias innecesarias
warnings.filterwarnings("ignore")

# --- Códigos ANSI para colores (Estética Non Fungible Metaverse) ---
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BORI = '\033[38;5;208m' # Color Naranja Bori

# -----------------------------------------------------------
# 📝 CONFIGURACIÓN DEL BOT Y PARÁMETROS
# -----------------------------------------------------------
class BotConfiguration:
    def __init__(self):
        self.INITIAL_USDC_BALANCE = 1000.00 
        self.LIVE_TRADING_ENABLED = False 
        self.COMMISSION_PCT = 0.003
        self.SLIPPAGE_PCT = 0.001
        
        # 🌐 ACTIVOS (30 ACTIVOS)
        self.ASSETS_TO_TRACK = [
            'BRCN', 'SOL', 'JUP', 'PYTH', 'ETH', 'LINK', 'DOGE', 'BTC', 'ADA', 'MATIC', 
            'XRP', 'LTC', 'BCH', 'DOT', 'NEAR', 'AVAX', 'OP', 'ARB', 'INJ', 'AAVE', 
            'LDO', 'MKR', 'FIL', 'ICP', 'SHIB', 'PEPE', 'FTM', 'UNI', 'SUI', 'APT'
        ]

        self.COINGECKO_IDS = {
            'SOL': 'solana', 'JUP': 'jupiter-exchange', 'PYTH': 'pyth-network',
            'ETH': 'ethereum', 'LINK': 'chainlink', 'DOGE': 'dogecoin',
            'BTC': 'bitcoin', 'ADA': 'cardano', 'MATIC': 'polygon',
            'XRP': 'ripple', 'LTC': 'litecoin', 'BCH': 'bitcoin-cash',
            'DOT': 'polkadot', 'NEAR': 'near-protocol', 'AVAX': 'avalanche-2',
            'OP': 'optimism', 'ARB': 'arbitrum', 'INJ': 'injective-protocol',
            'AAVE': 'aave', 'LDO': 'lido-dao', 'MKR': 'maker',
            'FIL': 'filecoin', 'ICP': 'internet-computer',
            'SHIB': 'shiba-inu', 'PEPE': 'pepe', 'FTM': 'fantom',
            'UNI': 'uniswap', 'SUI': 'sui', 'APT': 'aptos' 
        }

        self.TICK_INTERVAL_SECONDS = 15.0 # Un poco más lento para evitar Rate Limit
        self.RSI_PERIOD = 14             # Estándar técnico
        self.RSI_BUY_THRESHOLD = 30      # Nivel de sobreventa estándar
        self.MAX_CAPITAL_ALLOCATION_PCT = 0.95 
        self.CAPITAL_PER_ASSET = self.INITIAL_USDC_BALANCE / len(self.ASSETS_TO_TRACK)

# -----------------------------------------------------------
# 🔌 CONEXIÓN Y DATOS (LIVE FETCHER)
# -----------------------------------------------------------
class LiveFetcher:
    def __init__(self, assets: list):
        self.api_ids = [v for k, v in CONFIG.COINGECKO_IDS.items()]
        self.id_to_ticker = {v: k for k, v in CONFIG.COINGECKO_IDS.items()}
        self.current_prices = {ticker: 1.0 for ticker in CONFIG.ASSETS_TO_TRACK}
        self.previous_prices = self.current_prices.copy()
        self.market_index_history = [CONFIG.INITIAL_USDC_BALANCE]
        self.last_api_call_time = 0

    def fetch_latest_prices(self):
        now = time.time()
        if now - self.last_api_call_time < CONFIG.TICK_INTERVAL_SECONDS:
            return self._mock_visual_tick()

        self.last_api_call_time = now
        self.previous_prices = self.current_prices.copy()

        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {'ids': ','.join(self.api_ids), 'vs_currencies': 'usd'}
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 429:
                return self._fallback_simulated("RATE LIMIT")
            
            data = response.json()
            for coin_id, price_data in data.items():
                ticker = self.id_to_ticker.get(coin_id)
                if ticker: self.current_prices[ticker] = price_data['usd']
            
            # Simulación especial para BoriCoin (BRCN)
            brcn_current = self.current_prices.get('BRCN', 0.005)
            self.current_prices['BRCN'] = brcn_current * random.uniform(0.999, 1.001)
            
            self._update_benchmark()
            return self.current_prices
        except:
            return self._fallback_simulated("CONNECTION ERROR")

    def _update_benchmark(self):
        changes = []
        for t in CONFIG.ASSETS_TO_TRACK:
            if self.previous_prices[t] > 0:
                changes.append(self.current_prices[t] / self.previous_prices[t])
        avg_change = np.mean(changes) if changes else 1.0
        self.market_index_history.append(self.market_index_history[-1] * avg_change)

    def _mock_visual_tick(self):
        for t in CONFIG.ASSETS_TO_TRACK:
            self.current_prices[t] *= random.uniform(0.99999, 1.00001)
        return self.current_prices

    def _fallback_simulated(self, reason):
        for t in CONFIG.ASSETS_TO_TRACK:
            self.current_prices[t] *= random.uniform(0.998, 1.002)
        self._update_benchmark()
        return self.current_prices

# -----------------------------------------------------------
# 💹 LÓGICA DE ACTIVO Y TRADING
# -----------------------------------------------------------
class TradingAsset:
    def __init__(self, ticker, initial_usdc):
        self.ticker = ticker
        self.usdc_balance = initial_usdc
        self.asset_balance = 0.0
        self.buy_price_avg = 0.0
        self.prices = []
        self.transaction_log = []
        self.total_commissions = 0.0

    def calculate_rsi(self):
        if len(self.prices) < CONFIG.RSI_PERIOD + 1: return 50.0
        deltas = np.diff(self.prices)
        seed = deltas[:CONFIG.RSI_PERIOD]
        up = seed[seed >= 0].sum() / CONFIG.RSI_PERIOD
        down = -seed[seed < 0].sum() / CONFIG.RSI_PERIOD
        rs = up / down if down != 0 else 0
        rsi = 100. - 100. / (1. + rs)
        return rsi

    def update(self, price, is_real_tick):
        self.prices.append(price)
        if len(self.prices) > 100: self.prices.pop(0)
        
        rsi = self.calculate_rsi()
        action_msg = f"RSI: {rsi:.2f}"

        if is_real_tick and rsi <= CONFIG.RSI_BUY_THRESHOLD and self.usdc_balance > 1.0:
            # Comprar el 10% del disponible para promediar (DCA)
            amount_to_spend = self.usdc_balance * 0.10
            commission = amount_to_spend * CONFIG.COMMISSION_PCT
            net_buy = amount_to_spend - commission
            
            qty = net_buy / price
            self.total_commissions += commission
            
            # Promediar precio de entrada
            total_cost = (self.buy_price_avg * self.asset_balance) + net_buy
            self.asset_balance += qty
            self.usdc_balance -= amount_to_spend
            self.buy_price_avg = total_cost / self.asset_balance
            
            self.transaction_log.append(f"BUY {self.ticker} @ {price:.4f}")
            action_msg = f"{Colors.OKGREEN}BUY DCA EXECUTED{Colors.ENDC}"
            
        return action_msg

# -----------------------------------------------------------
# 🏢 PORTFOLIO MANAGER & UI
# -----------------------------------------------------------
class PortfolioManager:
    def __init__(self):
        self.fetcher = LiveFetcher(CONFIG.ASSETS_TO_TRACK)
        self.assets = {t: TradingAsset(t, CONFIG.CAPITAL_PER_ASSET) for t in CONFIG.ASSETS_TO_TRACK}
        self.start_time = time.time()

    def display(self, opinions):
        os.system('cls' if os.name == 'nt' else 'clear')
        total_val = sum(a.usdc_balance + (a.asset_balance * self.fetcher.current_prices[a.ticker]) for a in self.assets.values())
        pnl_pct = ((total_val / CONFIG.INITIAL_USDC_BALANCE) - 1) * 100
        pnl_col = Colors.OKGREEN if pnl_pct >= 0 else Colors.FAIL

        print(f"{Colors.BORI}{'='*80}{Colors.ENDC}")
        print(f" {Colors.BOLD}BORITRACKER v6.5 - NON FUNGIBLE METAVERSE EDITION{Colors.ENDC}")
        print(f" Portfolio: ${total_val:,.2f} | Rendimiento: {pnl_col}{pnl_pct:,.2f}%{Colors.ENDC}")
        print(f"{Colors.BORI}{'='*80}{Colors.ENDC}")
        
        print(f"{'Asset':<10} | {'Price':<12} | {'Balance':<12} | {'Avg Entry':<12} | {'Status'}")
        print("-" * 80)
        
        for t in CONFIG.ASSETS_TO_TRACK[:15]: # Mostrar los primeros 15 por espacio
            a = self.assets[t]
            p = self.fetcher.current_prices[t]
            print(f"{t:<10} | {p:<12.4f} | {a.asset_balance:<12.4f} | {a.buy_price_avg:<12.4f} | {opinions[t]}")
        print(f"\n{Colors.OKCYAN}Info: Monitoreando {len(CONFIG.ASSETS_TO_TRACK)} activos en la red. Ctrl+C para reporte.{Colors.ENDC}")

    def run(self):
        try:
            while True:
                is_real = (time.time() - self.fetcher.last_api_call_time) >= CONFIG.TICK_INTERVAL_SECONDS
                prices = self.fetcher.fetch_latest_prices()
                ops = {}
                for t, a in self.assets.items():
                    ops[t] = a.update(prices[t], is_real)
                
                self.display(ops)
                time.sleep(1)
        except KeyboardInterrupt:
            self.final_report()

    def final_report(self):
        print(f"\n{Colors.HEADER}--- REPORTE FINAL DE ACUMULACIÓN ---{Colors.ENDC}")
        for t, a in self.assets.items():
            if a.asset_balance > 0:
                print(f"Token: {t} | Acumulado: {a.asset_balance:.4f} | Inversión: ${(CONFIG.CAPITAL_PER_ASSET - a.usdc_balance):.2f}")

# -----------------------------------------------------------
# INICIO DEL SISTEMA
# -----------------------------------------------------------
if __name__ == "__main__":
    CONFIG = BotConfiguration()
    manager = PortfolioManager()
    manager.run()
