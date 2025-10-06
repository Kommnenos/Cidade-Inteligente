import random
import time
import math
import os
import requests
from simulador_base import posta_para_iot, carrega_config

def modelo_co2(intensidade_trafego: float, base: float, alpha: float) -> float:
    """Modelo de CO2 a partir da intensidade de trafego. Correlação linear com ruído médio."""
    return base + alpha * intensidade_trafego + random.uniform(-10, 10)

def pega_trafego_atual() -> float:
    """Pega o trafego atual do IoT Agent"""
    url = "http://orion:1026/v2/entities/urn:ngsi-ld:FluxoTrafegoObservado:001"
    headers = {
        "fiware-service": "openiot",
        "fiware-servicepath": "/"
    }
    try:
        resposta = requests.get(url, headers=headers, timeout=3)
        if resposta.status_code == 200:
            dados = resposta.json()
            return float(dados["intensidade"]["value"])
    except Exception as exc:
        print(f"[WARN] Erro ao obter trafego: {exc}")
    return 0.0


def run():
    cfg = carrega_config()["qualidade_ar"]
    intervalo = cfg.get("intervalo_segundos", 5)
    device_id = os.getenv("DEVICE_ID", cfg["device_id"])
    t = 0.0

    while True:
        trafego = pega_trafego_atual()
        if trafego == 0.0:
            trafego = 30
        co2 = modelo_co2(trafego, cfg["base_co2"], cfg["alpha"])
        posta_para_iot(device_id, {"co2": round(co2, 1)})
        time.sleep(intervalo)
        t = (t + intervalo / 3600) % 24

if __name__ == "__main__":
    run()
