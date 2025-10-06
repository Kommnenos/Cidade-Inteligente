import random
import time
import math
from simulador_base import posta_para_iot, carrega_config

#TODO: importar uma query do orion para pegar valores de trafego reais

def modelo_co2(intensidade_trafego: float, base: float, alpha: float) -> float:
    """Modelo de CO2 a partir da intensidade de trafego. Correlação linear com ruído médio."""
    return base + alpha * intensidade_trafego + random.uniform(-10, 10)

def run():
    cfg = carrega_config()["qualidade_ar"]
    intervalo = cfg.get("intervalo_segundos", 5)
    # Entrada de trafego mockada
    t = 0

    while True:
        trafego = 30 + 60 * (math.sin(2 * math.pi * t / 24) ** 2)
        co2 = modelo_co2(trafego, cfg["base_co2"], cfg["alpha"])
        posta_para_iot(cfg["device_id"], {"co2": round(co2, 1)})
        time.sleep(intervalo)
        t = (t + intervalo / 3600) % 24

if __name__ == "__main__":
    run()
