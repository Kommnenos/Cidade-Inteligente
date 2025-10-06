FROM python:3.11-slim
LABEL authors="Pedro Lealdini"
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY simulador_base.py sim_trafego.py sim_ar.py config.yml ./

CMD ["python", "-u", "sim_trafego.py"]
