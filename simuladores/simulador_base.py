import requests
import yaml
from datetime import datetime

URL_IOT_AGENT = "http://localhost:7896/iot/d"
HEADERS = {
    "fiware-service": "openiot",
    "fiware-servicepath": "/"
}

def carrega_config(path: str = "config.yml") -> dict:
    """Carrega a configuração YAML para todos os sensores"""
    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def posta_para_iot(device_id: str, dados: dict, chave_api: str = "1234") -> None:
    """Manda uma payload JSON para o IoT Agent"""
    url = f"{URL_IOT_AGENT}/device/{device_id}/attr"
    try:
        resposta = requests.post(url, headers=HEADERS, json=dados, timeout=5)
        resposta.raise_for_status()
        print(f"[{datetime.now().isoformat(timespec='seconds')}] "
              f"{device_id}: enviado {dados} -> {resposta.status_code} ")
    except Exception as exc:
        print(f"[{datetime.now().isoformat(timespec='seconds')}] "
              f"{device_id}: erro ao enviar {dados} -> {exc}")
