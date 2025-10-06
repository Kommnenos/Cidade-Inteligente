import requests
import yaml
from datetime import datetime
import os

SERVICO_FIWARE = os.getenv("FIWARE_SERVICE", "openiot")
SERVICEPATH_FIWARE = os.getenv("FIWARE_SERVICEPATH", "/")
URL_IOT_AGENT = os.getenv("IOT_AGENT_URL", "http://localhost:7896/iot/d")
APIKEY = os.getenv("APIKEY", "1234")

HEADERS = {
    "fiware-service": SERVICO_FIWARE,
    "fiware-servicepath": SERVICEPATH_FIWARE
}

def carrega_config(path: str = "config.yml") -> dict:
    """Carrega a configuração YAML para todos os sensores"""
    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def posta_para_iot(device_id: str, dados: dict) -> None:
    """Manda uma payload JSON para o IoT Agent"""
    url = f"{URL_IOT_AGENT}?k={APIKEY}&i={device_id}"
    try:
        resposta = requests.post(url, headers=HEADERS, json=dados, timeout=5)
        resposta.raise_for_status()
        print(f"[{datetime.now().isoformat(timespec='seconds')}] "
              f"{device_id}: enviado {dados} -> {resposta.status_code} ")
    except Exception as exc:
        print(f"[{datetime.now().isoformat(timespec='seconds')}] "
              f"{device_id}: erro ao enviar {dados} -> {exc}")
