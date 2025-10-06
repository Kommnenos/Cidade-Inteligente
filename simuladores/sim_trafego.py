import random
import time
import math
from simulador_base import posta_para_iot, carrega_config
import os

def curva_trafego(hora: float, base: float, amplitude: float) -> float:
    """Curva básica senoide com picos às 8 e 18."""
    return base + amplitude * (math.sin(2 * hora * math.pi / 24 ) ** 2)

def run():
    cfg = carrega_config()["trafego"]
    device_id = os.getenv("DEVICE_ID", cfg["device_id"])
    intervalo = cfg.get("intervalo_segundos", 5)

    while True:
        agora = time.localtime()
        hora = agora.tm_hour + agora.tm_min / 60
        valor = curva_trafego(hora, cfg["base"], cfg["amplitude"])
        valor += random.uniform(-cfg["ruido"], cfg["ruido"])
        payload = {"intensidade": round(valor, 2)}
        posta_para_iot(device_id ,payload)
        time.sleep(intervalo)

if __name__ == "__main__":
    run()
